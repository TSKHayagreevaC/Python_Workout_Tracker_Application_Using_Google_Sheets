import requests
from datetime import datetime
import os

GENDER = input("Please enter Your Gender Here:")
WEIGHT_KG = input("Enter Your Weight Here:")
HEIGHT_CM = input("Enter Your Height Here:")
AGE = input("Enter Your Age Here:")

APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_APP_KEY"]

exercise_endpoint = "https://trackap.mutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]

exercise_text = input("Tell Me Which Exercise You Did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

authorization_headers = {
    "Authorization": f"Basic {os.environ['TOKEN']}"
}

for exercise in result["exercise"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        sheet_endpoint, 
        json=sheet_inputs,
        auth=(
            "USERNAME",
            "PASSWORD",
        )
    )

    print(sheet_response.text())

