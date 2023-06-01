from flask import Flask, render_template, request, redirect, url_for
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

# Update the even pin in the database


def update_open_pin(pin_number, state):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE pins SET even_state=? WHERE even_pin=?', (state, pin_number))
    conn.commit()
    conn.close()

# Update the odd pin in the database


def update_close_pin(pin_number, state):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE pins SET odd_state=? WHERE odd_pin=?', (state, pin_number))
    conn.commit()
    conn.close()

# Add a new pin to the database


def add_pin(odd_pin, even_pin, name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO pins (odd_pin, even_pin, name, odd_state, even_state) VALUES (?, ?, ?, 1, 1)',
              (odd_pin, even_pin, name))
    conn.commit()
    conn.close()

# Delete a pin from the database


def delete_pin(odd_pin, even_pin):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM pins WHERE odd_pin=? AND even_pin=?',
              (odd_pin, even_pin,))
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

# Route for the home page


@app.route('/')
def home():
    pins = get_pins()
    return render_template('main.html', pins=pins)

# Function to handle on/off button


@app.route('/toggle_open_pin/<int:pin_number>', methods=['POST'])
def toggle_open_pin(pin_number):
    state = int(request.form['state'])
    update_open_pin(pin_number, state)
    wp.digitalWrite(pin_number, state)
    return redirect(url_for('home'), code=302)

@app.route('/toggle_close_pin/<int:pin_number>', methods=['POST'])
def toggle_close_pin(pin_number):
    state = int(request.form['state'])
    update_close_pin(pin_number, state)
    wp.digitalWrite(pin_number, state)
    return redirect(url_for('home'), code=302)


# Route for stopping pin operation


@app.route('/stop_pin/<int:odd_pin>/<int:even_pin>', methods=['POST'])
def stop_pin_route(odd_pin, even_pin):
    state = int(request.form['state'])
    update_close_pin(odd_pin, state)
    update_open_pin(even_pin, state)
    wp.digitalWrite(odd_pin, state)
    wp.digitalWrite(even_pin, state)
    return redirect(url_for('home'), code=302)


# Route for adding a pin


@app.route('/add_pin', methods=['POST'])
def add_pin_route():
    odd_pin = int(request.form['odd_pin'])
    even_pin = int(request.form['even_pin'])
    name = request.form['name']
    add_pin(odd_pin, even_pin, name)
    setup_pins()
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
