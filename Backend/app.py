from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Restrict for production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods.
    allow_headers=["*"],  # Allow all headers.
)

# Serve HTML templates
templates = Jinja2Templates(directory="templates")

# Static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the sequence of Lagnas
LAGNAS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo",
    "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Pydantic model for input validation
class CalculateTimeRequest(BaseModel):
    dob: str
    lagna: str

# Route to display the HTML form
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request, 
        "app_title": os.getenv("APP_TITLE", "Birth Time Estimator"),
        "app_description": os.getenv("APP_DESCRIPTION", "Estimate your birth time based on Lagna"),
        "enable_dark_mode": os.getenv("ENABLE_DARK_MODE", "false").lower() == "true"
    })

# Route to handle the calculation
@app.post("/calculate_time")
async def calculate_time(data: CalculateTimeRequest):
    try:
        birth_date = datetime.strptime(data.dob, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    if data.lagna not in LAGNAS:
        return {"error": "Invalid Lagna. Please select a valid Lagna."}

    sunrise = datetime.combine(birth_date, datetime.min.time()) + timedelta(hours=6, minutes=15)
    lagna_duration = timedelta(hours=2, minutes=30)

    for i, current_lagna in enumerate(LAGNAS):
        lagna_start = sunrise + i * lagna_duration
        lagna_end = lagna_start + lagna_duration
        if current_lagna == data.lagna:
            estimated_time = f"Between {lagna_start.strftime('%I:%M %p')} and {lagna_end.strftime('%I:%M %p')}"
            return {"result": estimated_time}

    return {"error": "Unable to calculate time for the given Lagna."}
