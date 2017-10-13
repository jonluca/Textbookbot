# TextbookBot

A bot that links you to textbooks based on the ISBN you provide it

## Requirements

Install using `pip install -r requirements.txt`

Python 3 required.

## Installation

Create a file titles `slackbot_settings.py` that is modeled after slackbot_settings_sample.py. Make sure that, for "errors_to" you have at least one message sent to the bot from that account 

## Usage

The bot listens to channels it's been added to and to direct messages.

To invoke from a channel, type `textbook isbn ##########`

To invoke from a DM, type `isbn ##########`

## Screenshots

<img src="https://i.imgur.com/f2Aco0o.png">