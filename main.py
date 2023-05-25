import tkinter as tk
from tkinter import ttk

try:
    import wiringpi, sys
    from wiringpi import GPIO
    wiringpi.wiringPiSetup()
    for i in range(4):
        wiringpi.pinMode(i, GPIO.OUTPUT)
except ImportError:
    wiringpi = None

def relay_control(pin):
    if wiringpi is not None:
        try:
            while True:
                wiringpi.digitalWrite(pin, GPIO.HIGH)
        except KeyboardInterrupt:
            print(f"{pin} closed")
            wiringpi.digitalWrite(pin, GPIO.LOW)
            sys.exit(0)
    else:
        print("WiringPi library is not available.")

def button_click(button, pin):
    current_state = button["text"]
    new_state = "Open" if current_state == "Close" else "Close"
    button.configure(text=new_state)
    if new_state == "Open":
        button.configure(style="Green.TButton")
    else:
        button.configure(style="Red.TButton")
    relay_control(pin)

root = tk.Tk()
root.title("Gate Control GUI")

# Create a frame to hold the cards
frame = ttk.Frame(root, padding=20)
frame.pack(fill='both', expand=True)

# Create Label for title
header_label = tk.Label(frame, text="Gate Control GUI", font=("Helvetica", 16))
header_label.grid(row=0, column=0, columnspan=2, pady=5)

# Create four cards with buttons
for i in range(4):
    pin = i + 1
    
    card_frame = ttk.Frame(frame, relief="solid", padding=10)
    card_frame.grid(row=(i // 2) + 1, column=i % 2, padx=10, pady=10, sticky='nsew')
    frame.columnconfigure(i % 2, weight=1)
    frame.rowconfigure((i // 2) + 1, weight=1)
    
    label = tk.Label(card_frame, text=f"{'East' if i == 0 else 'West' if i == 1 else 'North' if i == 2 else 'South'} Lobby")
    label.pack(pady=5)

    button_style = ttk.Style()
    button_style.configure("Red.TButton", foreground="black", background="red")
    button_style.configure("Green.TButton", foreground="black", background="green")

    button = ttk.Button(card_frame, text="Close", style="Red.TButton")
    button.configure(command=lambda btn=button, pin=pin: button_click(btn, pin))
    button.pack(pady=5)

root.mainloop()
