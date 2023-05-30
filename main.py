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
                 (odd_pin INTEGER PRIMARY KEY, even_pin INTEGER, name TEXT, state INTEGER)''')
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
def update_pin_state(odd_pin, even_pin, state):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE pins SET state=? WHERE odd_pin=? AND even_pin=?', (state, odd_pin, even_pin))
    conn.commit()
    conn.close()

# Add a new pin to the database
def add_pin(odd_pin, even_pin, name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO pins (odd_pin, even_pin, name, state) VALUES (?, ?, ?, 0)', (odd_pin, even_pin, name))
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
        if pin[0] != 0:
            wp.pinMode(pin[0], wp.GPIO.OUTPUT)
            wp.digitalWrite(pin[0], wp.GPIO.LOW)
        if pin[1] != 0:
            wp.pinMode(pin[1], wp.GPIO.OUTPUT)
            wp.digitalWrite(pin[1], wp.GPIO.LOW)

# Function to turn on an odd pin
def turn_on_odd_pin(odd_pin):
    wp.digitalWrite(odd_pin, wp.GPIO.HIGH)
    update_pin_state(odd_pin, None, 1)

# Function to turn off an odd pin
def turn_off_odd_pin(odd_pin):
    wp.digitalWrite(odd_pin, wp.GPIO.LOW)
    update_pin_state(odd_pin, None, 0)

# Function to turn on an even pin
def turn_on_even_pin(even_pin):
    wp.digitalWrite(even_pin, wp.GPIO.HIGH)
    update_pin_state(None, even_pin, 1)

# Function to turn off an even pin
def turn_off_even_pin(even_pin):
    wp.digitalWrite(even_pin, wp.GPIO.LOW)
    update_pin_state(None, even_pin, 0)

# Route for the home page
@app.route('/')
def home():
    pins = get_pins()
    return render_template('index.html', pins=pins)

# Route for toggling a pin
@app.route('/toggle_pin/<int:pin_number>', methods=['POST'])
def toggle_pin(pin_number):
    state = request.form['state']
    if pin_number % 2 == 0:
        # Control even pin
        if int(state) == 1:
            turn_on_even_pin(pin_number)
        elif int(state) == 0:
            turn_off_even_pin(pin_number)
    else:
        # Control odd pin
        if int(state) == 1:
            turn_on_odd_pin(pin_number)
        elif int(state) == 0:
            turn_off_odd_pin(pin_number)
    return redirect("/")

# Route for adding a pin
@app.route('/add_pin', methods=['POST'])
def add_pin_route():
    odd_pin = int(request.form['odd_pin'])
    even_pin = int(request.form['even_pin'])
    name = request.form['name']
    add_pin(odd_pin, even_pin, name)
    setup_pins()  # Set up the newly added pin
    return redirect("/")

# Route for deleting a pin
@app.route('/delete_pin/<int:odd_pin>/<int:even_pin>', methods=['POST'])
def delete_pin_route(odd_pin, even_pin):
    delete_pin(odd_pin, even_pin)
    return redirect("/")

if __name__ == '__main__':
    create_table()
    setup_pins()
    app.run(host='0.0.0.0', port=8000, debug=True)
