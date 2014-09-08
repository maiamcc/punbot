#!/usr/bin/env python

import zulip
import sys

# Keyword arguments 'email' and 'api_key' are not required if you are using ~/.zuliprc
client = zulip.Client(email="punbot-bot@students.hackerschool.com",
                      api_key="FgrSqwnEu0MM3XyEpdwcpeINkC95cyw4")

# Send a stream message
# client.send_message({
#     "type": "stream",
#     "to": "Denmark",
#     "subject": "Castle",
#     "content": "Something is rotten in the state of Denmark."
# })

# Send a private message
client.send_message({
    "type": "private",
    "to": "maia.mcc@gmail.com",
    "content": "Did you hear the one about the three holes in the ground?"
})

def respond(msg):
    if msg["type"] == "private":
        pass
    elif msg["type"] == "stream":
        pass

# Parse each message that the user receives
# This is a blocking call that will run forever
client.call_on_each_message(respond)