// RGBLed.cpp
//
// The RGBLed class provides control over the a red, greed, blue
// LED. 
//
#include "RGBLed.h"


void RGBLed::initialize(uint8_t _redPin, uint8_t _greenPin, uint8_t _bluePin) { 
    redPin = _redPin;
    greenPin = _greenPin;
    bluePin = _bluePin;
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin,LOW); 
    digitalWrite(bluePin,LOW);
}

void RGBLed::setRGB(bool red, bool green, bool blue) {
    // Set red led
    if (red) {
        digitalWrite(redPin, HIGH);
    }
    else {
        digitalWrite(redPin, LOW);
    }
    // Set green led
    if (green) {
        digitalWrite(greenPin, HIGH);
    }
    else {
        digitalWrite(greenPin, LOW);
    }
    // Set blue led
    if (blue) {
        digitalWrite(bluePin, HIGH);
    }
    else {
        digitalWrite(bluePin, LOW);
    }
}

void RGBLed::setRed() {
    setRGB(true,false,false);
}

void RGBLed::setGreen() {
    setRGB(false,true,false);
}

void RGBLed::setBlue() {
    setRGB(false,false,true);
}

void RGBLed::setOff() {
    setRGB(false,false,false);
}

void RGBLed::setWhite() {
    setRGB(true,true,true);
}
