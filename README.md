punbot
======
A bot for Zulip that makes ridiculous puns.

### Zulip commands

* `**@ pun bot** help` (or PM `help` to pun bot) - displays help text
* `**@ pun bot** shut up` or `**@ pun bot** go away` - bans pun bot from the current topic (not to be confused with the current thread)
* `**@ pun bot** come back` - un-bans punbot from the current topic
* `**@ pun bot** more pun` - increases pun frequency
* `**@ pun bot** less pun` - decreases pun frequency
* `**@ pun bot** pun me` - returns a pun

### Fiddly bits
Change `PUN_CHANCE` to any value between 0 and 1 to change the frequency with which pun bot puns (e.g. a value of `.3` means if presented with a punnable message, pun bot puns 30% of the time). Note that pun bot will always pun on anything sent to it via PM.

### I want my own pun bot!
1. make a Zulip bot
2. make its API key an evironmental variable (so that the API key isn't floating around on the interwebs)
    - from terminal, run `export punbot_api_key=[api key goes here]`
    - if using Heroku to host, you'll need to set this in the Heroku environment too: from terminal, run `heroku config:set punbot_api_key=[api key goes here]
    - consider putting a file (I called mine `environ`) in your project director and also in your .gitignore. It should contain only "export punbot_api_key=[api key goes here]". (Run `echo export punbot_api_key=[api key goes here] > environ`.) Then you can run `source environ` from terminal to automatically set that environment variable locally.
3. subscribe it to any streams you want it to haunt (via your own `Subscriptions` page)
4. adjust pun frequency if desired
5. run the script on your machine or on Heroku
6. ????
7. Profit!

(If anyone figures out what step 6 involves, please let me know.)

### Punbot in Action
Good old-fashioned punning:

![Screenshot 0](/Screenshots/driver.png)

Punbot crashing someone else's blog test, and `**@ pun bot** go away` in action:

![Screenshot 1](/Screenshots/weather0.png)
![Screenshot 2](/Screenshots/weather1.png)
