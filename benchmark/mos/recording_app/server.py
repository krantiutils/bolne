"""NepTTS-Bench Recording App — collects native speaker recordings for MOS evaluation."""

import json
import os
import sqlite3
import uuid
import secrets
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
AUDIO_DIR = DATA_DIR / "audio"
DB_PATH = DATA_DIR / "recordings.db"
SENTENCES_PATH = APP_DIR.parent / "sentences.json"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")

app = FastAPI(title="NepTTS-Bench Recording App")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
security = HTTPBasic()


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if not secrets.compare_digest(credentials.password, ADMIN_PASSWORD):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# ---------------------------------------------------------------------------
# Database initialization (Task 2)
# ---------------------------------------------------------------------------

def init_db():
    """Create tables and load sentences from sentences.json on startup."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    try:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS speakers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                ethnicity TEXT,
                age_range TEXT,
                gender TEXT,
                device_info TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                speaker_id TEXT REFERENCES speakers(id),
                sentence_id TEXT,
                audio_path TEXT NOT NULL,
                duration_ms INTEGER,
                created_at TEXT NOT NULL,
                flagged INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS sentences (
                sent_id TEXT PRIMARY KEY,
                text_dev TEXT NOT NULL,
                text_roman TEXT,
                word_count INTEGER,
                category TEXT,
                phonetic_targets TEXT,
                contrast_word TEXT,
                pair_id TEXT
            );

            CREATE TABLE IF NOT EXISTS speaker_assignments (
                speaker_id TEXT,
                sentence_id TEXT,
                is_pair INTEGER DEFAULT 0,
                pair_group TEXT,
                PRIMARY KEY (speaker_id, sentence_id)
            );
        """)

        # Only load sentences if the table is empty
        row = db.execute("SELECT COUNT(*) AS cnt FROM sentences").fetchone()
        if row["cnt"] > 0:
            db.close()
            return

        with open(SENTENCES_PATH, "r", encoding="utf-8") as f:
            all_sentences = json.load(f)

        # Filter to short sentences (word_count <= 11)
        short = [s for s in all_sentences if s["word_count"] <= 11]

        # Identify minimal pairs: source starts with phonological_minimal_pairs/
        # and exactly 2 sentences share the same source
        pair_sources = defaultdict(list)
        for s in short:
            if s["source"].startswith("phonological_minimal_pairs/"):
                pair_sources[s["source"]].append(s["sent_id"])

        # Build a lookup: sent_id -> pair_id (source) for valid pairs (exactly 2)
        pair_lookup = {}
        for source, ids in pair_sources.items():
            if len(ids) == 2:
                for sid in ids:
                    pair_lookup[sid] = source

        for s in short:
            pair_id = pair_lookup.get(s["sent_id"])
            # Category is the top-level part of source (before first /)
            category = s["source"].split("/")[0]
            phonetic_targets_str = json.dumps(s.get("phonetic_targets", []))
            db.execute(
                """INSERT INTO sentences
                   (sent_id, text_dev, text_roman, word_count, category,
                    phonetic_targets, contrast_word, pair_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    s["sent_id"],
                    s["text_devanagari"],
                    s.get("text_romanized", ""),
                    s["word_count"],
                    category,
                    phonetic_targets_str,
                    s.get("contrast_word", ""),
                    pair_id,
                ),
            )

        db.commit()
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Sentence assignment algorithm (Task 3)
# ---------------------------------------------------------------------------

def assign_sentences(db: sqlite3.Connection, speaker_id: str) -> list[str]:
    """Assign 20 regular + all 20 minimal-pair sentences to a speaker.

    Returns the list of 20 selected regular sentence IDs.
    """
    # 1. Get all non-pair sentences with their recording counts
    rows = db.execute("""
        SELECT s.sent_id, s.category,
               COUNT(r.id) AS rec_count
        FROM sentences s
        LEFT JOIN recordings r ON r.sentence_id = s.sent_id
        WHERE s.pair_id IS NULL
        GROUP BY s.sent_id
    """).fetchall()

    # 2. Group by top-level category
    groups: dict[str, list] = defaultdict(list)
    for row in rows:
        groups[row["category"]].append(
            {"sent_id": row["sent_id"], "rec_count": row["rec_count"]}
        )

    # 3. Sort each group by recording count ascending
    for cat in groups:
        groups[cat].sort(key=lambda x: x["rec_count"])

    # 4. Round-robin pick from groups until 20 selected
    selected: list[str] = []
    category_names = sorted(groups.keys())
    # Track position within each category
    indices = {cat: 0 for cat in category_names}

    while len(selected) < 20:
        picked_this_round = False
        for cat in category_names:
            if len(selected) >= 20:
                break
            idx = indices[cat]
            if idx < len(groups[cat]):
                selected.append(groups[cat][idx]["sent_id"])
                indices[cat] = idx + 1
                picked_this_round = True
        if not picked_this_round:
            break  # No more sentences available

    # 5. Also assign ALL minimal pair sentences (pair_id IS NOT NULL)
    pair_rows = db.execute(
        "SELECT sent_id, pair_id FROM sentences WHERE pair_id IS NOT NULL"
    ).fetchall()

    # 6. Save to speaker_assignments table
    now = datetime.now(timezone.utc).isoformat()
    for sid in selected:
        db.execute(
            """INSERT OR IGNORE INTO speaker_assignments
               (speaker_id, sentence_id, is_pair, pair_group)
               VALUES (?, ?, 0, NULL)""",
            (speaker_id, sid),
        )

    for row in pair_rows:
        db.execute(
            """INSERT OR IGNORE INTO speaker_assignments
               (speaker_id, sentence_id, is_pair, pair_group)
               VALUES (?, ?, 1, ?)""",
            (speaker_id, row["sent_id"], row["pair_id"]),
        )

    db.commit()

    # 7. Return list of selected regular sentence IDs
    return selected


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class SpeakerCreate(BaseModel):
    name: str
    ethnicity: str | None = None
    age_range: str | None = None
    gender: str | None = None
    device_info: str | None = None


# ---------------------------------------------------------------------------
# API endpoints (Task 4)
# ---------------------------------------------------------------------------

@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/speakers")
def create_speaker(body: SpeakerCreate, db: sqlite3.Connection = Depends(get_db)):
    speaker_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc).isoformat()

    # Create audio directory for this speaker
    speaker_audio_dir = AUDIO_DIR / speaker_id
    speaker_audio_dir.mkdir(parents=True, exist_ok=True)

    db.execute(
        """INSERT INTO speakers (id, name, ethnicity, age_range, gender, device_info, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (speaker_id, body.name, body.ethnicity, body.age_range, body.gender, body.device_info, now),
    )
    db.commit()

    # Assign sentences
    regular_ids = assign_sentences(db, speaker_id)

    # Fetch regular sentence details
    placeholders = ",".join("?" for _ in regular_ids)
    regular_rows = db.execute(
        f"SELECT * FROM sentences WHERE sent_id IN ({placeholders})",
        regular_ids,
    ).fetchall()
    regular_sentences = [dict(r) for r in regular_rows]

    # Fetch pair sentences grouped by pair_id
    pair_rows = db.execute(
        """SELECT s.* FROM sentences s
           JOIN speaker_assignments sa ON sa.sentence_id = s.sent_id
           WHERE sa.speaker_id = ? AND sa.is_pair = 1
           ORDER BY s.pair_id, s.sent_id""",
        (speaker_id,),
    ).fetchall()

    pairs_grouped: dict[str, list] = defaultdict(list)
    for r in pair_rows:
        pairs_grouped[r["pair_id"]].append(dict(r))

    pairs = [
        {"pair_id": pid, "sentences": sents}
        for pid, sents in sorted(pairs_grouped.items())
    ]

    return {
        "speaker_id": speaker_id,
        "regular_sentences": regular_sentences,
        "pairs": pairs,
    }


@app.post("/api/recordings")
def upload_recording(
    speaker_id: str = Form(...),
    sentence_id: str = Form(...),
    duration_ms: int = Form(...),
    audio: UploadFile = File(...),
    db: sqlite3.Connection = Depends(get_db),
):
    # Verify speaker exists
    speaker = db.execute("SELECT id FROM speakers WHERE id = ?", (speaker_id,)).fetchone()
    if not speaker:
        raise HTTPException(status_code=404, detail="Speaker not found")

    # Verify sentence is assigned to this speaker
    assignment = db.execute(
        "SELECT * FROM speaker_assignments WHERE speaker_id = ? AND sentence_id = ?",
        (speaker_id, sentence_id),
    ).fetchone()
    if not assignment:
        raise HTTPException(status_code=400, detail="Sentence not assigned to this speaker")

    # Determine file extension
    content_type = audio.content_type or ""
    ext = "wav" if "wav" in content_type else "webm"

    # If re-recording, delete old file and DB row
    existing = db.execute(
        "SELECT id, audio_path FROM recordings WHERE speaker_id = ? AND sentence_id = ?",
        (speaker_id, sentence_id),
    ).fetchone()
    if existing:
        old_path = Path(existing["audio_path"])
        if old_path.exists():
            old_path.unlink()
        db.execute("DELETE FROM recordings WHERE id = ?", (existing["id"],))

    # Save the audio file
    filename = f"{sentence_id}.{ext}"
    speaker_audio_dir = AUDIO_DIR / speaker_id
    speaker_audio_dir.mkdir(parents=True, exist_ok=True)
    file_path = speaker_audio_dir / filename

    content = audio.file.read()
    file_path.write_bytes(content)

    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        """INSERT INTO recordings (speaker_id, sentence_id, audio_path, duration_ms, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (speaker_id, sentence_id, str(file_path), duration_ms, now),
    )
    db.commit()

    return {"status": "ok", "filename": filename}


@app.get("/api/progress/{speaker_id}")
def get_progress(speaker_id: str, db: sqlite3.Connection = Depends(get_db)):
    # Verify speaker exists
    speaker = db.execute("SELECT id FROM speakers WHERE id = ?", (speaker_id,)).fetchone()
    if not speaker:
        raise HTTPException(status_code=404, detail="Speaker not found")

    total_assigned = db.execute(
        "SELECT COUNT(*) AS cnt FROM speaker_assignments WHERE speaker_id = ?",
        (speaker_id,),
    ).fetchone()["cnt"]

    recorded_rows = db.execute(
        "SELECT sentence_id FROM recordings WHERE speaker_id = ?",
        (speaker_id,),
    ).fetchall()
    recorded_ids = [r["sentence_id"] for r in recorded_rows]

    return {
        "total_assigned": total_assigned,
        "total_recorded": len(recorded_ids),
        "recorded_ids": recorded_ids,
    }
