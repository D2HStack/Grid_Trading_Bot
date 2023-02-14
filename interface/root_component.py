# Root
# Display the interface

import tkinter as tk

class Root(tk.Tk):
    def __init__(self, strategy, api, websocket):
        super().__init__()
        print("Hello from Root")