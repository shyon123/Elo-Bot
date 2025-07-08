from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
import pytesseract
from PIL import Image

from my_database import init_db, get_connection
from search import show_top_players
from reset import reset_db
from elo_calc import process_match

# Optional: Use this if tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "elo.db"

# Initialize DB on API start
init_db(DB_FILE)

@app.post("/compute")
async def compute(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8").splitlines()
    reader = csv.reader(text)

    reset_db(DB_FILE)

    for row in reader:
        if len(row) == 3:
            player1, player2, result = row
            process_match(player1.strip(), player2.strip(), int(result), DB_FILE)

    leaderboard = show_top_players(DB_FILE)
    return {"leaderboard": leaderboard}


@app.post("/parse-image")
async def parse_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    raw_text = pytesseract.image_to_string(image)

    matches = []
    for line in raw_text.splitlines():
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 3 and parts[2] in {'0', '1', '2'}:
            matches.append({
                "player1": parts[0],
                "player2": parts[1],
                "result": parts[2]
            })

    return {"matches": matches}
