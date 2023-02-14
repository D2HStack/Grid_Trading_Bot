# Display messages to user
import tkinter as tk
from datetime import datetime
from interface.styling import *
import logging

logger = logging.getLogger()

class Messages(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._messages = []
        # Display
        self._messages_text = tk.Text(self, height=10, width=60, state=tk.DISABLED, bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self._messages_text.pack(side=tk.TOP)

    # Update the messages
    def update_msg(self):
        for message in self._messages:
            if not message['displayed']:
                msg = message['msg']
                self._messages_text.configure(state=tk.NORMAL)
                self._messages_text.insert("1.0", datetime.utcnow().strftime("%a %H:%M:%S ::") + msg + "\n")
                self._messages_text.configure(state=tk.DISABLED)
                message['displayed'] = True


    # Add a message to messages
    def add_msg(self, msg: str):
        self._messages.append({"msg": msg, "displayed": False})


