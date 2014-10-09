#!/usr/bin/env python

import nltk
from random import choice, random
import re
import sys
import zulip

PUN_CHANCE = 1 # probabiltiy of making a pun off a valid msg

# defining all punctuation marks to be removed from msg strings
punctuation =  ".,?![]{}()'\"!@#$%^&*<>/-_+=;"

# initializing a Zulip client
client = zulip.Client(email="punbot-bot@students.hackerschool.com",
                      api_key="FgrSqwnEu0MM3XyEpdwcpeINkC95cyw4")

# pronunciation dictionary
dictionary = nltk.corpus.cmudict.dict()

def get_word_stress(word):
    """Returns a list of 0s and 1s indicating the stress
        pattern of given word. If the word is not a valid
        English word, returns [0,0]--since punbot will only
        pun on words of 2+ syllables, and we want to treat
        any non-recognized word as punnable."""
    pronounce = dictionary.get(word.lower())
    if pronounce: # if word in the dictionary
        pronounce = choice(pronounce) # in case of multiple
            # pronunciations, pick one at random
        phonemes = [letter for phoneme in pronounce for letter in phoneme]
        results = [char for char in phonemes if char.isdigit()]
        return results
    else:
        return [0,0]

def valid_her_word(word):
    """Returns True if word can be turned into a "I hardly
        know 'er" pun and False otherwise."""
    pronounce = dictionary.get(word.lower())
    if pronounce: # if word in the dictionary
        for pronunciation in pronounce:
            # Check to see that word is >1 syllable and ends
                # in unstressed "ER" phoneme
            if pronunciation[-1] == "ER0" and len(get_word_stress(word))>1:
                return True
        else:
            return False
    elif re.search(".*(?=er$)", word):
        # If word not in the dictionary, we approximate by
            # checking if it ends in "er"
        return True

def respond(msg):
    """Processes incoming messages and, if appropriate,
        sends response."""
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
    """Checks text for punnable words, picks one at random
        and returns a pun statement for that word."""
    punable = []
    for word in text:
        if valid_her_word(word):
            punable.append(word)
    if len(punable) > 0:
        pun_word = choice(punable)[:-2]
        # manipulations to make valid words
        if pun_word[-1] == "i": # e.g. ferrier --> ferry 'er
            if dictionary.get(pun_word[:-1]+"y"):
                pun_word = pun_word[:-1]+"y"
        elif dictionary.get(pun_word+"e"): # e.g. parser --> parse 'er
            pun_word = pun_word+"e"
        elif not dictionary.get(pun_word): # e.g. stirrer --> stir 'er
            if dictionary.get(pun_word[:-1]):
                pun_word = pun_word[:-1]
        randnum = random()
        # random chance of punning or not
        if randnum <= PUN_CHANCE:
            return adjust_case(pun_word) + " 'er? I hardly KNOW 'er!"
    else:
        return

def adjust_case(word):
    """Title cases the word, unless it starts with ':' (i.e. it's an emoji)."""
    if word.startswith(":"):
        return word
    else:
        return word.title()

# Parse each message that the user receives
# This is a blocking call that will run forever
client.call_on_each_message(respond)

# for him: IH0 M // AH0 M