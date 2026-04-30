#include <Wire.h>
#include "Adafruit_VL53L0X.h"
#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

SoftwareSerial mp3Serial(12, 11);
DFRobotDFPlayerMini mp3;

// Pins
const int red1Pin = 8;
const int red2Pin = 9;
const int greenPin = 10;
const int uvPin = 7;

// Timing
const unsigned long activeTime = 150000UL;   // 2 min 30 sec
const unsigned long phase2Time = 33000UL;    // 33 sec
const unsigned long uvOffTime = 100000UL;     // 1 min 33 sec

unsigned long triggerStart = 0;

bool activeMode = false;
bool readyToTrigger = true;
bool phase2Started = false;
bool uvTurnedOff = false;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  pinMode(red1Pin, OUTPUT);
  pinMode(red2Pin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(uvPin, OUTPUT);

  // Idle state
  digitalWrite(red1Pin, HIGH);
  digitalWrite(red2Pin, LOW);
  digitalWrite(greenPin, HIGH);
  digitalWrite(uvPin, LOW);

  if (!lox.begin()) {
    Serial.println("VL53L0X not found. Check wiring.");
  }

  mp3Serial.begin(9600);
  delay(1000);

  if (!mp3.begin(mp3Serial)) {
    Serial.println("MP3 module not found. Check wiring or SD card.");
  } else {
    mp3.volume(25);
    Serial.println("MP3 ready.");
  }

  Serial.println("System ready.");
}

void loop() {
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false);

  int distanceCm = -1;

  if (measure.RangeStatus != 4) {
    distanceCm = measure.RangeMilliMeter / 10;
    Serial.print("Distance: ");
    Serial.println(distanceCm);
  } else {
    Serial.println("Out of range");
  }

  if (distanceCm >= 6 || distanceCm == -1) {
    readyToTrigger = true;
  }

  if (!activeMode && readyToTrigger && distanceCm > 0 && distanceCm < 6) {
    activeMode = true;
    readyToTrigger = false;
    phase2Started = false;
    uvTurnedOff = false;
    triggerStart = millis();

    digitalWrite(red1Pin, HIGH);
    digitalWrite(red2Pin, HIGH);
    digitalWrite(greenPin, LOW);
    digitalWrite(uvPin, LOW);

    mp3.play(1);

    Serial.println("START: red1 ON, UV OFF");
  }

  if (activeMode) {
    unsigned long elapsed = millis() - triggerStart;

    Serial.print("Elapsed: ");
    Serial.println(elapsed);

    // Phase 2 starts at 33 seconds
    if (!phase2Started && elapsed >= phase2Time) {
      digitalWrite(red1Pin, LOW);
      digitalWrite(uvPin, HIGH);
      phase2Started = true;

      Serial.println("PHASE 2: red1 OFF, UV ON");
    }

    // UV turns off at 1 min 8 sec
    if (!uvTurnedOff && elapsed >= uvOffTime) {
      digitalWrite(red1Pin, LOW);
      digitalWrite(uvPin, LOW);
      uvTurnedOff = true;

      Serial.println("UV OFF: red1 still OFF");
    }

    // End presentation
    if (elapsed >= activeTime) {
      activeMode = false;

      digitalWrite(red1Pin, HIGH);
      digitalWrite(red2Pin, LOW);
      digitalWrite(greenPin, HIGH);
      digitalWrite(uvPin, LOW);

      mp3.stop();

      Serial.println("END: back to idle, red1 ON");
    }
  }

  delay(250);
}
