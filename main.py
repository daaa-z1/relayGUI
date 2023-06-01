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
        wp.pinMode(pin[0], 1)
        wp.digitalWrite(pin[0], 1)
        wp.pinMode(pin[1], 1)
        wp.digitalWrite(pin[1], 1)

# Function to turn on an odd pin
def turn_on_odd_pin(odd_pin):
<<<<<<< HEAD
    wp.digitalWrite(odd_pin, 0)
    update_pin_state(odd_pin, None, 0)

# Function to turn off an odd pin
def turn_off_odd_pin(odd_pin):
    wp.digitalWrite(odd_pin, 1)
    update_pin_state(odd_pin, None, 1)

# Function to turn on an even pin
def turn_on_even_pin(even_pin):
    wp.digitalWrite(even_pin, 0)
    update_pin_state(None, even_pin, 0)

# Function to turn off an even pin
def turn_off_even_pin(even_pin):
    wp.digitalWrite(even_pin, 1)
    update_pin_state(None, even_pin, 1)
=======
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
>>>>>>> parent of 9bc8153 (y)

# Route for the home page
@app.route('/')
def home():
    pins = get_pins()
    return render_template('main.html', pins=pins)

<<<<<<< HEAD
@app.route('/toggle_pin/<int:pin_number>/<int:even_number>', methods=['POST'])
def toggle_pin(pin_number, even_number):
    state = int(request.form['state'])
    if pin_number % 2 == 0:
        # Control even pin
        if state == 1:
            turn_on_even_pin(even_number)
        elif state == 0:
            turn_off_even_pin(even_number)
    else:
        # Control odd pin
        if state == 1:
            turn_on_odd_pin(pin_number)
        elif state == 0:
            turn_off_odd_pin(pin_number)

=======
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
>>>>>>> parent of 9bc8153 (y)
    return redirect("/")

# Route for adding a pin
@app.route('/add_pin', methods=['POST'])
def add_pin_route():
    odd_pin = int(request.form['odd_pin'])
    even_pin = int(request.form['even_pin'])
    name = request.form['name']
    add_pin(odd_pin, even_pin, name)
    return redirect("/")

@app.route('/delete_pin/<int:odd_pin>/<int:even_pin>', methods=['POST'])
def delete_pin_route(odd_pin, even_pin):
    delete_pin(odd_pin, even_pin)
    return redirect("/")

@app.route('/stop_pin/<int:odd_pin>/<int:even_pin>', methods=['POST'])
def stop_pin_route(odd_pin, even_pin):
    if odd_pin:
        turn_off_odd_pin(odd_pin)
    if even_pin:
        turn_off_even_pin(even_pin)
    return redirect("/")

if __name__ == '__main__':
    create_table()
    setup_pins()
    app.run(host='0.0.0.0', port=8000, debug=True)
