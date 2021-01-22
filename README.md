# Telegram analysis script

A quick and dirty Python script to extract stats from Telegram conversations.

## Features
- Print:
  - Number of messages
  - Number of words
  - Number of emoji
  - Number of stickers
  - Average message length (w & w/o emoji)
  - Most common words
  - Most common emoji  
    <br/>
- Plot:
  - number of messages (donut)
  - number of words (donut)
  - number of emoji (donut)
  - number of stickers (donut)
  - daily distribution (bar/line plot)
  - average message length (bar plot)
  - most used emoji (bar plot)

## Quick guide

- Currently works only for conversations between two people (no group support)
- Reads JSON-files that can be exported from [Telegram Desktop](https://desktop.telegram.org/ 'Telegram Desktop')
- Uncomment lines in run() to print stats and draw plots
- Daily distribution shows line plot instead of bar plot if there are over 700 days

## Issues
- Emoji distribution doesn't show the emoji at the moment :D
- Emoji distribution might miss some emojis


Credit for inspiration to [this person in Reddit](https://www.reddit.com/r/Telegram/comments/9yssu0/oc_i_built_a_web_app_to_analyze_telegram_chats/ 'Link to the Reddit post').

