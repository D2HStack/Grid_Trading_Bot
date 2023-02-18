# Display messages to user
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from interface.styling import *
import logging

logger = logging.getLogger()

class Messages(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._messages = []
        # Display
        self._messages_text = Text(self, state=DISABLED, font=FONT)
        self._messages_text.pack(side=BOTTOM)

    # Update the messages
    def update_msg(self):
        for message in self._messages:
            if not message['displayed']:
                msg = message['msg']
                self._messages_text.configure(state=NORMAL)
                self._messages_text.insert("1.0", datetime.utcnow().strftime("%a %H:%M:%S ::") + msg + "\n")
                self._messages_text.configure(state=DISABLED)
                message['displayed'] = True

    # Add a message to messages
    def add_msg(self, msg: str):
        self._messages.append({"msg": msg, "displayed": False})


