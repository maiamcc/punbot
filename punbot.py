#!/usr/bin/env python

import nltk
from random import choice, random
import re
import sys
import zulip

PUN_CHANCE = 1 # number between 0 and 1 -- probabiltiy of making a pun off a valid msg
HELP_MSG = """Hi, I'm punbot, here for all of your annoying pun needs! (Well, actually, only a single, very specifiy annoying pun need. Sorry about that.) Here's how I work:\n\n

- if you post in a stream I'm subscribed to (`social`, `off-topic`, `Victory`, `Oops`), I miiiight make a stupid pun.\n
- PM me "help" or write "@pun bot help" in a stream I'm subcribed to for help\n
- if you want me to stop bothering you in a specific topic, write "@pun bot go away" or "@pun bot shut up" and I'll leave that topic FOREVER! :cry:\n
- but if you miss me, you can write "@pun bot come back" and it will be like I never left!\n

Contact Maia McCormick (Summer 2 2014) with any questions or problems, or [check out my code](github.com/maiamcc/punbot)."""

# defining all punctuation marks to be removed from msg strings
punctuation =  ".,?![]{}()'\"!@#$%^&*<>/-_+=;"

# list of topics in which punbot should not post
banned_topics = []

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
    print msg
    if msg["sender_email"] != "punbot-bot@students.hackerschool.com":
        if msg["content"].startswith("@**pun bot**"):
            msg_lower = msg["content"].lower()
            msg_lower = msg_lower.replace("@**pun bot** ", "")
            if msg_lower == "help":
                send_response_msg(msg, HELP_MSG, definitely_respond=True)
            elif msg_lower == "shut up" or msg_lower == "go away":
                if msg["subject"] in banned_topics:
                    send_response_msg(msg, "Yeesh, what do you want from me? You've already banned me!", definitely_respond=True)
                else:
                    send_response_msg(msg, "Aww, okay. :cry: Let me know if you ever want me back, with `@pun bot come back`. I'll just go away now.", definitely_respond=True)
                    banned_topics.append(msg["subject"])
            elif msg_lower == "come back":
                send_response_msg(msg, "You want me back! Horray! I knew we were friends! :smile:")
                banned_topics.remove(msg["subject"])
            else:
                pass
        elif msg["type"] == "private" and msg["content"] == "help":
            send_response_msg(msg, HELP_MSG, definitely_respond=True)
        elif msg["subject"] not in banned_topics:
            msg_content = str(msg["content"]).translate(None, punctuation).lower().split()

            pun_msg = hardly_know_er(msg_content)

            if pun_msg:
                send_response_msg(msg, pun_msg)

def send_response_msg(incoming_msg, outgoing_text, probability=PUN_CHANCE, definitely_respond=False):
    randnum = random() # random chance of punning or not
    if definitely_respond:
        probability = 1
    if incoming_msg["type"] == "private":
        client.send_message({
            "type": "private",
            "to": incoming_msg["sender_email"],
            "content": outgoing_text
        })
    elif incoming_msg["type"] == "stream" and randnum <= probability:
        client.send_message({
            "type": "stream",
            "subject": incoming_msg["subject"],
            "to": incoming_msg['display_recipient'],
            "content": outgoing_text
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