// RGBLed.h 
//
// The RGBLed class provides control over the a red, greed, blue
// LED. 
#ifndef _RGBLED_H_
#define _RGBLED_H_
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

class RGBLed {
    public:
        uint8_t redPin;
        uint8_t greenPin;
        uint8_t bluePin;
        void initialize(uint8_t _redPin, uint8_t _greenPin, uint8_t _bluePin);
        void setRGB(bool red, bool green, bool blue);
        void setRed();
        void setGreen();
        void setBlue();
        void setWhite();
        void setOff();
};

#endif
