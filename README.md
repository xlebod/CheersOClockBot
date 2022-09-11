# Cheers'O Clock Bot

Originally intended to encourage collective alcoholism in Virtual Reality, this extremely simple bot allows syncing of 
multiple clients based on the timestamp of a single discord message.

The premise is simple: 
- Host (first person to launch program) sends a message initiating a drinking party
- Members retrieve this message and sync their clock to the that message
- Send OSC (Open Sound Control) messages to a desired ip (local by default) with a given frequency
- ???
- The rest is just darkness....


### *!! This is a PROTOTYPE !!*
Certain restriction apply:
- The channel which hosts this bot has to have no other messages!
- To reset the bot to a new binging session, delete the message posted by the previous host

## How to use it

1. Create dedicated channel in Discord
2. Copy channel id to CHANNEL_ID in main.py
3. Set PLATFORM, DRINKIES_FREQUENCY, START_MESSAGE, etc. to desired values
4. *Optional* Run `pyinstaller --onefile main.py` and create `dist\main.exe`
5. Run program