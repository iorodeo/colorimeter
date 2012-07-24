// ColorSensor.h
//
// Interface to ??? rgb color sensor.
#ifndef _COLORSENSOR_H_
#define _COLORSENSOR_H_
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

//const uint32_t DFLT_PULSE_IN_WAIT = 250000;
const uint32_t DFLT_PULSE_IN_WAIT = 50000;
const uint16_t DFLT_TIMEOUT_COUNT_MAX = 10;

class ColorSensor {
    public:
        uint8_t S0; // Control Pins
        uint8_t S1;
        uint8_t S2;
        uint8_t S3;
        uint8_t FO; // Frequency output
        uint32_t pulseInWait; 
        uint32_t timeoutCountMax;
        void initialize(uint8_t _S0, uint8_t _S1, uint8_t _S2, uint8_t _S3, uint8_t FO);
        uint32_t getFrequency(uint16_t  numSamples);
        void setChannelRed();
        void setChannelGreen();
        void setChannelBlue();
        void setChannelClear();
};
#endif

