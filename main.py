from flask import Flask, render_template, request, redirect
import wiringpi as wp
import sqlite3

app = Flask(__name__)
db_path = 'pins.db'  # Path to the SQLite database file

# Set up WiringOPi
wp.wiringPiSetup()

# Create the pins table if it doesn't exist
def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pins
                 (odd_pin INTEGER PRIMARY KEY, even_pin INTEGER, name TEXT, odd_state INTEGER, even_state INTEGER)''')
    conn.commit()
    conn.close()

# Get all pins from the database
def get_pins():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM pins')
    pins = c.fetchall()
    conn.close()
    return pins

# Update the state of a pin in the database
def update_pin_state(odd_pin, even_pin, odd_state, even_state):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE pins SET odd_state=? AND even_state=? WHERE odd_pin=? AND even_pin=?', (odd_state, even_state, odd_pin, even_pin))
    conn.commit()
    conn.close()

# Add a new pin to the database
def add_pin(odd_pin, even_pin, name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO pins (odd_pin, even_pin, name, state) VALUES (?, ?, ?, 1, 1)', (odd_pin, even_pin, name))
    conn.commit()
    conn.close()

# Delete a pin from the database
def delete_pin(odd_pin, even_pin):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM pins WHERE odd_pin=? AND even_pin=?', (odd_pin, even_pin,))
    conn.commit()
    conn.close()

# Set each pin as an output and initialize it to low
def setup_pins():
    pins = get_pins()
    for pin in pins:
        wp.pinMode(pin[0], 1)
        wp.digitalWrite(pin[0], 1)
        wp.pinMode(pin[1], 1)
        wp.digitalWrite(pin[1], 1)

# Function to turn on an odd pin
def turn_on_odd_pin(odd_pin):
    wp.digitalWrite(odd_pin, pin[3])
    update_pin_state(odd_pin, None, 0, None)

# Function to turn off an odd pin
def turn_off_odd_pin(odd_pin):
    wp.digitalWrite(odd_pin, 1)
    update_pin_state(odd_pin, None, 1, None)

# Function to turn on an even pin
def turn_on_even_pin(even_pin):
    wp.digitalWrite(even_pin, 0)
    update_pin_state(None, even_pin, None, 0)

# Function to turn off an even pin
def turn_off_even_pin(even_pin):
    wp.digitalWrite(even_pin, 1)
    update_pin_state(None, even_pin, None, 1)

# Route for the home page
@app.route('/')
def home():
    pins = get_pins()
    return render_template('main.html', pins=pins)

# @app.route('/toggle_pin/<int:pin_number>', methods=['POST'])
# def toggle_pin(pin_number):
#     state = int(request.form['state'])
#     if state == 2:
#         # Handle stop action
#         # Stop even pin operation
#         turn_off_even_pin(pin_number)
#         # Stop odd pin operation
#         turn_off_odd_pin(pin_number)
#     else:
#         # Handle open/close actions
#         if pin_number % 2 == 0:
#             # Control even pin
#             if state == 1:
#                 turn_on_even_pin(pin_number)
#             elif state == 0:
#                 turn_off_even_pin(pin_number)
#         else:
#             # Control odd pin
#             if state == 1:
#                 turn_on_odd_pin(pin_number)
#             elif state == 0:
#                 turn_off_odd_pin(pin_number)
#     return redirect("/")

# Function to handle on/off button
@app.route('/turn_on_pin/<int:pin_number>', methods=['POST'])
def turn_on_pin_route(pin_number):
    if pin_number % 2 == 0:
        turn_on_even_pin(pin_number)
    else:
        turn_on_odd_pin(pin_number)
    return redirect("/")


@app.route('/turn_off_pin/<int:pin_number>', methods=['POST'])
def turn_off_pin_route(pin_number):
    if pin_number % 2 == 0:
        turn_off_even_pin(pin_number)
    else:
        turn_off_odd_pin(pin_number)
    return redirect("/")

# Route for stopping pin operation
@app.route('/stop_pin/<int:odd_pin>/<int:even_pin>', methods=['POST'])
def stop_pin_route(odd_pin, even_pin):
    turn_off_odd_pin(odd_pin)
    turn_off_even_pin(even_pin)
    return redirect("/")

# Route for adding a pin
@app.route('/add_pin', methods=['POST'])
def add_pin_route():
    odd_pin = int(request.form['odd_pin'])
    even_pin = int(request.form['even_pin'])
    name = request.form['name']
    add_pin(odd_pin, even_pin, name)
    return redirect("/")

# Route for deleting a pin
@app.route('/delete_pin/<int:odd_pin>/<int:even_pin>', methods=['POST'])
def delete_pin_route(odd_pin, even_pin):
    delete_pin(odd_pin, even_pin)
    return redirect("/")

# Function to run on app startup
def startup():
    create_table()
    setup_pins()

if __name__ == '__main__':
    startup()
    app.run(host='0.0.0.0', port=8000, debug=True)
