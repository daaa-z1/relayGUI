import tkinter as tk
from tkinter import ttk

try:
    import wiringpi, time, sys
    from wiringpi import GPIO
except:
    pass

try:
    wiringpi.wiringPiSetup()
    for i in range(3):
        wiringpi.pinMode(i, GPIO.OUTPUT)
        pin = i+1
except:
    pass
    
def relay1():
    try:
        while True:
            wiringpi.digitalWrite(pin, GPIO.HIGH)
    except KeyboardInterrupt:
        print(f"relay1 {pin}")
        wiringpi.digitalWrite(pin, GPIO.LOW)
        sys.exit(0)
        
def relay2():
    try:
        while True:
            wiringpi.digitalWrite(pin, GPIO.HIGH)
    except KeyboardInterrupt:
        print("relay2 {pin}")
        wiringpi.digitalWrite(pin, GPIO.LOW)
        sys.exit(0)
        
def relay3():
    try:
        while True:
            wiringpi.digitalWrite(pin, GPIO.HIGH)
    except KeyboardInterrupt:
        print("relay3 {pin}")
        wiringpi.digitalWrite(pin, GPIO.LOW)
        sys.exit(0)


def button_click(button, card_number):
    current_state = button["text"]
    new_state = "Open" if current_state == "Close" else "Close"
    button.configure(text=new_state)
    if card_number == 'relay1':
        print("relay1 {card_number}")
        relay1()
    elif card_number == 'relay2':
        print("relay2 {card_number}")
        relay2()
    elif card_number == 'relay3':
        print("relay3 {card_number}")
        relay3()

root = tk.Tk()
root.title("Card GUI")

# Create a frame to hold the cards
frame = ttk.Frame(root, padding=20)
frame.pack()

# Create five cards with buttons
for i in range(3):
    card_number = i+1
    
    card_frame = ttk.Frame(frame, relief="solid", padding=10)
    card_frame.grid(row=i // 2, column=i % 2, padx=10, pady=10)
    
    label = tk.Label(card_frame, text=f"Relay {i+1}").pack(pady=5)

    button = ttk.Button(card_frame, text="Close")
    button.configure(command=lambda btn=button, num=card_number: button_click(btn, f'relay{num}'))
    button.pack(pady=5)

root.mainloop()
