from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook működik!"

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Webhook elindult")

    try:
        # Bejövő adat kisbetűsítése
        data = {k.lower(): v for k, v in request.json.items()}
        print("Kapott adat:", data)

        # Dátumbélyeg
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Kulcs betöltése a fájlból
        print("Google kulcs betöltése indul...")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        keyfile_dict = json.loads(open("key.json").read())
        creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)
        client = gspread.authorize(creds)
        print("Kulcs betöltve")

        # Google Sheet megnyitása
        sheet = client.open("AsesaTesztSheet").worksheet("alap")
        print("Táblázat elérve")

        # Sor összeállítása és beírás
        new_row = [timestamp, data.get("email", ""), data.get("név", ""), data.get("pontszám", "")]
        sheet.append_row(new_row)
        print("Beírva a Google Sheet-be:", new_row)

    except Exception as e:
        print("HIBA A SHEET-NÉL:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)