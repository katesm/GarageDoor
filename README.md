# GarageDoor - *In progress
Garage door opener for Raspberry Pi

This is a simple garage door opener application for the Raspberry Pi. After seeing a couple of YouTube videos of others creating garage door apps with for their Raspberry Pi, I figured I would give it a go as well. I’m full-time .NET developer so I figured this would give me the opportunity to learn Python since it seems to be the go to language for development on the Pi. 
The code is wrote for only one garage door, but this could be modified easily for multiple doors. 

## What you need

1. Raspberry Pi
2. USB WiFi dongle
3. Relay Module - SainSmart
4. Magnetic Contact Switch 
5. 2-conductor electrical wire

##Getting Started

Make sure you have [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) installed and python package manager `python get-pip.py`

1. Install CherryPy `$ pip install cherrypy`
2. Configure the json.config with SMTP settings and set GPIO pin numbers used
