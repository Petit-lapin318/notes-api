from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Статика теперь доступна по /static
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

notes = [{"id": 1, "text": "Первая заметка"}]

@app.get("/notes")
def get_notes():
    return notes

@app.post("/notes")
def create_note(text: str):
    new_id = max(note["id"] for note in notes) + 1 if notes else 1
    notes.append({"id": new_id, "text": text})
    return {"id": new_id, "text": text}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            notes.pop(i)
            return {"result": "deleted"}
    raise HTTPException(status_code=404, detail="Note not found")

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/notes-page")
def notes_page():
    return FileResponse("notes.html")