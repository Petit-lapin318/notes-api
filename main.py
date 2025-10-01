from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключаем отдачу статики (включая index.html)
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# Твои API-эндпоинты
notes = [{"id": 1, "text": "Первая заметка"}]

@app.get("/notes")
def get_notes():
    return notes

@app.post("/notes")
def create_note(text: str):
    new_id = max(note["id"] for note in notes) + 1 if notes else 1
    notes.append({"id": new_id, "text": text})
    return {"id": new_id, "text": text}