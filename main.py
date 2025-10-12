from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import db

app = FastAPI()
app.mount("/static", StaticFiles(directory=".", html=True), name="static")
# Pydantic-модели
class NoteBase(BaseModel):
    text: str


class Note(NoteBase):
    id: int


# Инициализация БД при старте
@app.on_event("startup")
def startup_event():
    db.init_db()

# получить все заметки
@app.get("/notes", response_model=List[Note])
def get_notes():
    rows = db.get_all_notes()
    return rows

# создать заметку — принимаем JSON тело
@app.post("/notes", response_model=Note)
def create_note(payload: NoteBase):
    # Accept JSON only
    content = payload.text
    new = db.create_note(content)
    return new

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    ok = db.delete_note(note_id)
    if ok:
        return {"result": "deleted"}
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, payload: NoteBase):
    content = payload.text
    updated = db.update_note(note_id, content)
    if updated is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/notes-page")
def notes_page():
    return FileResponse("notes.html")