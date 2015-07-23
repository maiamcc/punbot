#!/usr/bin/env python

import nltk
from random import choice, random
import os
import re
import sys
import zulip

nltk.data.path.append('./nltk_data/')

PUN_CHANCE = 0.75  # number between 0 and 1 -- probability of making a pun off a valid msg
HELP_MSG = """Hi, I'm punbot, here for all of your annoying pun needs! (Well, actually, only a single, very specifiy annoying pun need. Sorry about that.) Here's how I work:\n\n

- if you post in a stream I'm subscribed to (`social`, `off-topic`, `Victory`, `Oops`), I miiiight make a stupid pun.\n
- PM me "help" or write "@pun bot help" for help\n
- if you want me to stop bothering you in a specific topic, write "@pun bot go away" or "@pun bot shut up" and I'll leave that topic FOREVER! :cry:\n
- but if you miss me, you can write "@pun bot come back" and it will be like I never left!\n
- if you need more puns, write "@pun bot more pun" (or less with "@pun bot less pun")\n

Contact Maia McCormick (Summer 2 2014) with any questions or problems, or [check out my code](github.com/maiamcc/punbot)."""

# defining all punctuation marks to be removed from msg strings
punctuation =  ".,?![]{}()'\"!@#$%^&*<>/-_+=;"

# list of topics in which punbot may post with pun_chance
topics_whitelist = {}

# list of topics where punbot is banned
banned_topics = []

# initializing a Zulip client
# if running from my machine, in terminal, `source environ` to set environmental var
client = zulip.Client(email="punbot-bot@students.hackerschool.com",
                      api_key=os.environ["punbot_api_key"])

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
    """Processes incoming messages and, if appropriate,sends response."""
    if msg["sender_email"] != "punbot-bot@students.hackerschool.com":
        response = None
        response_chance = 1.0  # defaults that a response will 100% happen
        if msg["content"].startswith("@**pun bot**"):
            msg_lower = msg["content"].lower().strip()
            msg_lower = msg_lower.replace("@**pun bot** ", "")
            msg_topic = msg["subject"]

            if msg_lower == "help":
                response = HELP_MSG
            elif msg_topic in banned_topics:
                if msg_lower in ["shut up", "go away",
                                 "shush", "hush", "shoo"]:
                    response = "Yeesh, what do you want from me? \
                                You've already banned me!"
                elif msg_lower == "come back":
                    response = "You want me back! Hooray! \
                                I knew we were friends! :smile:"
                    topics_whitelist.setdefault(msg_topic, PUN_CHANCE)
                    banned_topics.remove(msg_topic)
                else:
                    pass
            elif msg_lower in ["shut up", "go away", "shush", "hush", "shoo"]:
                response = "Aww, okay. :cry: \
                            Let me know if you ever want me back, \
                            with `@pun bot come back`. \
                            I'll just go away now."
                banned_topics.append(msg_topic)
                if msg_topic in topics_whitelist:
                    topics_whitelist.pop(msg_topic)
            elif msg_topic in topics_whitelist:
                if msg_lower in ["more", "more pun", "more puns"]:
                    pun_chance = topics_whitelist[msg_topic]
                    pun_chance = min(1.0, pun_chance + 0.1)
                    topics_whitelist[msg_topic] = pun_chance
                    response = "So much pun! (pun chance = %d%%)" \
                               % (pun_chance * 100)
                elif msg_lower in ["less", "less pun", "less puns",
                                   "fewer", "fewer pun", "fewer puns"]:
                    pun_chance = topics_whitelist[msg_topic]
                    pun_chance = max(0.0, pun_chance - 0.1)
                    topics_whitelist[msg_topic] = pun_chance
                    response = "Not so punny, eh? (pun chance = %d%%)" \
                               % (pun_chance * 100)
                else:
                    pass
            else:
                response = "Ohai! I'm paying attention now! :smile:"
                topics_whitelist.setdefault(msg_topic, PUN_CHANCE)
        elif msg["type"] == "private" and msg["content"] == "help":
            response = HELP_MSG
        elif msg["subject"] in topics_whitelist:
            msg_content = str(msg["content"]).translate(None, punctuation).lower().split()

            response = hardly_know_er(msg_content)
            response_chance = topics_whitelist[msg["subject"]]
        else:
            pass

        if response:
            send_response_msg(msg, "test: " + response, response_chance)

def send_response_msg(incoming_msg, outgoing_text, probability):
    randnum = random() # random chance of punning or not
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
        chosen_word = choice(punable)
        pun_word = chosen_word[:-2]
        # manipulations to make valid words
        if pun_word[-1] == "i": # e.g. ferrier --> ferry 'er
            if dictionary.get(pun_word[:-1]+"y"):
                pun_word = pun_word[:-1]+"y"
        elif dictionary.get(pun_word+"e") and chosen_word[-2] == "e":
            # e.g. parser --> parse 'er (but NOT vicar --> vice 'er)
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