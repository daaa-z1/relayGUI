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
                 (pin_number INTEGER PRIMARY KEY, name TEXT, state INTEGER)''')
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


def update_pin_state(pin_number, state):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE pins SET state=? WHERE pin_number=?', (state, pin_number))
    conn.commit()
    conn.close()

# Add a new pin to the database


def add_pin(pin_number, name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'INSERT INTO pins (pin_number, name, state) VALUES (?, ?, 0)', (pin_number, name))
    conn.commit()
    conn.close()

# Delete a pin from the database


def delete_pin(pin_number):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM pins WHERE pin_number=?', (pin_number,))
    conn.commit()
    conn.close()

# Set each pin as an output and initialize it to low


def setup_pins():
    pins = get_pins()
    for pin in pins:
        wp.pinMode(pin[0], wp.OUTPUT)
        wp.digitalWrite(pin[0], wp.LOW)


@app.route('/')
def home():
    pins = get_pins()
    return render_template('index.html', pins=pins)


@app.route('/toggle_pin/<int:pin_number>', methods=['POST'])
def toggle_pin(pin_number):
    state = request.form['state']
    wp.digitalWrite(pin_number, int(state))
    update_pin_state(pin_number, int(state))
    return redirect('/')


@app.route('/add_pin', methods=['POST'])
def add_pin_route():
    pin_number = int(request.form['pin_number'])
    name = request.form['name']
    add_pin(pin_number, name)
    setup_pins()  # Set up the newly added pin
    return redirect('/')


@app.route('/delete_pin/<int:pin_number>', methods=['POST'])
def delete_pin_route(pin_number):
    delete_pin(pin_number)
    return redirect('/')


if __name__ == '__main__':
    create_table()
    setup_pins()
    app.run(host='0.0.0.0', port=8000, debug=True)
