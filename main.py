import tkinter as tk
from tkinter import ttk

try:
    import wiringpi, time, sys
    from wiringpi import GPIO
    wiringpi.wiringPiSetup()
    for i in range(3):
        wiringpi.pinMode(i, GPIO.OUTPUT)
except ImportError:
    wiringpi = None

def relay_control(pin):
    if wiringpi is not None:
        try:
            while True:
                wiringpi.digitalWrite(pin, GPIO.HIGH)
        except KeyboardInterrupt:
            print(f"relay{pin} closed")
            wiringpi.digitalWrite(pin, GPIO.LOW)
            sys.exit(0)
    else:
        print("WiringPi library is not available.")

def button_click(button, pin):
    current_state = button["text"]
    new_state = "Open" if current_state == "Close" else "Close"
    button.configure(text=new_state)
    relay_control(pin)

root = tk.Tk()
root.title("Card GUI")

# Create a frame to hold the cards
frame = ttk.Frame(root, padding=20)
frame.pack()

# Create three cards with buttons
for i in range(3):
    pin = i + 1
    
    card_frame = ttk.Frame(frame, relief="solid", padding=10)
    card_frame.grid(row=i // 2, column=i % 2, padx=10, pady=10)
    
    label = tk.Label(card_frame, text=f"Relay {i+1}")
    label.pack(pady=5)

    button = ttk.Button(card_frame, text="Close")
    button.configure(command=lambda btn=button, pin=pin: button_click(btn, pin))
    button.pack(pady=5)

root.mainloop()
