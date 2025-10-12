import sqlite3
from typing import List, Dict, Optional

DB_PATH = 'notes.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_notes() -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, text FROM notes ORDER BY id')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_note(text: str) -> Dict:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (text) VALUES (?)', (text,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {'id': new_id, 'text': text}

def delete_note(note_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0

def update_note(note_id: int, text: str) -> Optional[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE notes SET text = ? WHERE id = ?', (text, note_id))
    if cur.rowcount == 0:
        conn.close()
        return None
    conn.commit()
    conn.close()
    return {'id': note_id, 'text': text}
