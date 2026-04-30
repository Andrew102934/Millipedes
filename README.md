# Millipedes
Project Overview

This project runs an interactive museum exhibit. When a visitor presses a button, UV lights turn on and an audio file plays to explain the millipedes.

The system is built to be simple and reliable so it can run all day without breaking or needing supervision.

Features
Button triggers the experience
UV lights turn on for ~2 minutes
Audio plays from SD card (MP3 module)
Cooldown so people can’t spam the button
Runs automatically
System Architecture

The system uses an Arduino to control everything.

Basic flow:

Button → Arduino → Lights + Audio → Cooldown → Ready again

Hardware setup:

Button → digital input pin
UV lights → output pin (through relay/transistor)
MP3 module (TF card) → serial (TX/RX)
Key Components
Arduino Sketch

Main code that handles button input, timing, and cooldown.

Button

Triggers the system. Simple digital input with basic debounce.

UV Lights

Turn on when the button is pressed and stay on for a fixed time.

MP3 Module (TF card)

Plays the audio file stored on the SD card when triggered.

Cooldown Logic

Stops the system from being triggered again right away.

Getting Started
Requirements
Arduino (Uno or similar)
Button
UV lights + relay/transistor
MP3-TF-16P module + SD card
Jumper wires + breadboard
Setup
Upload the Arduino code to the board
Put your audio file on the SD card (ex: 0001.mp3)
Wire everything correctly (button, lights, MP3 module)
Run
Power the Arduino
Press the button to trigger the exhibit
Design Notes
Kept everything simple so it’s easy to fix if something breaks
Cooldown is important so people don’t mash the button
Timing is handled in the Arduino (no external control needed)
Built for real use in a museum setting
Assumptions
System stays powered on
Audio file is already loaded on SD card
Wiring is correct
For Future Developers
Keep it simple
Test with the actual hardware
If you add features, just plug them into the main loop
Put detailed logic explanations in the code, not here
