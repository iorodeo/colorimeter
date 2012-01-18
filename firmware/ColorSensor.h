// ColorSensor.h
//
// Interface to ??? rgb color sensor.
#ifndef _COLORSENSOR_H_
#define _COLORSENSOR_H_

#define PULSE_IN_WAIT 250000

class ColorSensor {
    public:
        uint8_t S0; // Control Pins
        uint8_t S1;
        uint8_t S2;
        uint8_t S3;
        uint8_t FO; // Frequency output
        void initialize(uint8_t _S0, uint8_t _S1, uint8_t _S2, uint8_t _S3, uint8_t FO);
        uint32_t getFrequency(uint16_t  numSamples);
        void setChannelRed();
        void setChannelGreen();
        void setChannelBlue();
        void setChannelClear();
};
#endif

