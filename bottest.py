#!/usr/bin/env python

import zulip
import sys
import re
from random import choice, random
import nltk

PUN_CHANCE = 0.25 # probabiltiy of making a pun off a valid msg
# defining all punctuation marks to be removed from msg strings
punctuation =  ".,?![]{}()'\"!@#$%^&*<>/-_+=;"

# Keyword arguments 'email' and 'api_key' are not required if you are using ~/.zuliprc
client = zulip.Client(email="punbot-bot@students.hackerschool.com",
                      api_key="FgrSqwnEu0MM3XyEpdwcpeINkC95cyw4")

dictionary = nltk.corpus.cmudict.dict()

def get_word_stress(word):
    pronounce = dictionary.get(word.lower())
    if pronounce:
        pronounce = choice(pronounce)
        phonemes = [letter for phoneme in pronounce for letter in phoneme]
        results = [char for char in phonemes if char.isdigit()]
        return results
    else:
        return [0,0]

def valid_her_word(word):
    pronounce = dictionary.get(word.lower())
    if pronounce:
        for pronunciation in pronounce:
            if pronunciation[-1] == "ER0" and len(get_word_stress(word))>1:
                return True
        else:
            return False
    elif re.search(".*(?=er$)", word):
        return True

def respond(msg):
    if msg["sender_email"] != "punbot-bot@students.hackerschool.com":
        msg_content = str(msg["content"]).translate(None, punctuation).lower().split()
        pun_msg = hardly_know_er(msg_content)
        if pun_msg:
            if msg["type"] == "private":
                client.send_message({
                    "type": "private",
                    "to": msg["sender_email"],
                    "content": pun_msg
                })
            elif msg["type"] == "stream":
                client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg['display_recipient'],
                    "content": pun_msg
                })

def hardly_know_er(text):
    punable = []
    for word in text:
        if valid_her_word(word):
            punable.append(word)
    if len(punable) > 0:
        pun_word = choice(punable)[:-2]
        if pun_word[-1] == "i": # e.g. ferrier --> ferry 'er
            print "your word ends in i"
            if dictionary.get(pun_word[:-1]+"y"):
                pun_word = pun_word[:-1]+"y"
        elif not dictionary.get(pun_word): # e.g. stirrer --> stir 'er
            print "your word maybe has too many letters"
            if dictionary.get(pun_word[:-1]):
                pun_word = pun_word[:-1]
        elif word[-2] == "e": # e.g. parser --> parse 'er
            print "your word maybe should end in e"
            print "your word now is", pun_word
            if dictionary.get(pun_word+"e"):
                print "lets modify the thing"
                pun_word = pun_word+"e"
        randnum = random()
        if randnum <= PUN_CHANCE:
            return pun_word.title() + " 'er? I hardly KNOW 'er!"
    else:
        return

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

# for him: IH0 M // AH0 M