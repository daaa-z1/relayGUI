import wiringpi
from flask import Flask, render_template, request
app = Flask(__name__)

wiringpi.wiringPiSetup()

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    0: {'name': 'GPIO 0', 'state': 0},
    1: {'name': 'GPIO 1', 'state': 0}
}

# Set each pin as an output and make it low:
for pin in pins:
    wiringpi.pinMode(pin, 1)
    wiringpi.digitalWrite(pin, 0)


@app.route("/")
def main():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = wiringpi.digitalRead(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pins
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:


@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        wiringpi.digitalWrite(changePin, 1)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        wiringpi.digitalWrite(changePin, 0)
        message = "Turned " + deviceName + " off."

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = wiringpi.digitalRead(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins': pins
    }

    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
