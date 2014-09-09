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
# client.send_message({
#     "type": "private",
#     "to": "maia.mcc@gmail.com",
#     "content": "Did you hear the one about the three holes in the ground?"
# })

def respond(msg):
    if (msg["type"] == "private") and (msg["sender_email"] != "punbot-bot@students.hackerschool.com"):
        print "Punbot got a message from not-punbot!"
        print msg
        client.send_message({
            "type": "private",
            "to": msg["sender_email"],
            "content": "You just sent me this message: " + msg["content"]
        })
    elif msg["type"] == "stream" and (msg["sender_email"] != "punbot-bot@students.hackerschool.com"):
        print "Look, a stream message from not-punbot!"
        print msg
        client.send_message({
            "type": "stream",
            "subject": msg["subject"],
            "to": msg['display_recipient'],
            "content": "@**"+ msg["sender_full_name"] + "** just sent this message: " + msg["content"]
        })

# Parse each message that the user receives
# This is a blocking call that will run forever
client.call_on_each_message(respond)

"""
A SAMPLE PRIVATE MESSAGE:
{u'recipient_id': 36100,
u'sender_email': u'maia.mcc@gmail.com',
u'timestamp': 1410277376,
u'display_recipient':
    [{u'domain': u'students.hackerschool.com',
    u'short_name': u'maia.mcc',
    u'email': u'maia.mcc@gmail.com',
    u'is_mirror_dummy': False,
    u'full_name': u"Maia McCormick (S'14)",
    u'id': 6175},
    {u'domain': u'students.hackerschool.com',
    u'short_name': u'punbot-bot',
    u'id': 6458,
    u'is_mirror_dummy': False,
    u'full_name': u'pun bot',
    u'email': u'punbot-bot@students.hackerschool.com'}],
u'sender_id': 6175,
u'sender_full_name': u"Maia McCormick (S'14)",
u'sender_domain': u'students.hackerschool.com',
u'content': u'whoo',
u'gravatar_hash': u'068432e2e1839c64c05323d419c78762',
u'avatar_url': u'https://humbug-user-avatars.s3.amazonaws.com/47ec406248244f0cf1171700f2be783279ac6e13?x=x',
u'client': u'desktop app Mac 0.4.4',
u'content_type': u'text/x-markdown',
u'subject_links': [],
u'sender_short_name': u'maia.mcc',
u'type': u'private',
u'id': 27441124,
u'subject': u''}
"""

"""
A SAMPLE STREAM MESSAGE:
{u'recipient_id': 35576,
u'sender_email': u'maia.mcc@gmail.com',
u'timestamp': 1410278114,
u'display_recipient': u'bot-test',
u'sender_id': 6175,
u'sender_full_name': u"Maia McCormick (S'14)",
u'sender_domain': u'students.hackerschool.com',
u'content': u'what do you call a thing?',
u'gravatar_hash': u'068432e2e1839c64c05323d419c78762',
u'avatar_url': u'https://humbug-user-avatars.s3.amazonaws.com/47ec406248244f0cf1171700f2be783279ac6e13?x=x',
u'client': u'desktop app Mac 0.4.4',
u'content_type': u'text/x-markdown',
u'subject_links': [],
u'sender_short_name': u'maia.mcc',
u'type': u'stream',
u'id': 27441699,
u'subject': u'i\u2019m a test'}
"""