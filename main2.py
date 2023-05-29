import wiringpi
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
wiringpi.wiringPiSetup()

# Database configuration
DB_PATH = "pins.db"

# Create a dictionary to store the pin information
pins = {}


@app.route("/")
def index():
    # Retrieve pin information from the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pins")
        rows = cursor.fetchall()

    # Populate the pins dictionary
    pins.clear()
    for row in rows:
        pin_number, pin_name, pin_state = row
        pins[pin_number] = {"name": pin_name, "state": pin_state}

    return render_template("index.html", pins=pins)


@app.route("/toggle_pin/<int:pin_number>", methods=["POST"])
def toggle_pin(pin_number):
    # Get the current state of the pin
    pin_state = pins[pin_number]["state"]

    # Toggle the pin state
    new_state = 0 if pin_state == 1 else 1
    wiringpi.digitalWrite(pin_number, new_state)

    # Update the pin state in the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE pins SET state = ? WHERE number = ?", (new_state, pin_number))
        conn.commit()

    return redirect(url_for("index"))


@app.route("/delete_pin/<int:pin_number>", methods=["POST"])
def delete_pin(pin_number):
    # Delete the pin from the pins dictionary
    del pins[pin_number]

    # Delete the pin from the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pins WHERE number = ?", (pin_number,))
        conn.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    # Set each pin as an output and make it low
    for pin_number in pins:
        wiringpi.pinMode(pin_number, 1)
        wiringpi.digitalWrite(pin_number, 0)

    app.run(host="0.0.0.0", port=8000, debug=True)
