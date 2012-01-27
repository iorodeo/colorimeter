#ifndef _COLORIMETER_H_
#define _COLORIMETER_H_
#include "WProgram.h"
#include "ColorSensor.h"
#include "RGBLed.h"

#define DEFAULT_NUM_SAMPLES 5000

class FrequencyData {
    public:
        uint32_t red;
        uint32_t green;
        uint32_t blue;
        uint32_t white;
};

class TransmissionData {
    public:
        float red;
        float green;
        float blue;
        float white;
};

class AbsorbanceData {
    public:
        float red;
        float green;
        float blue;
        float white;
};


class Colorimeter {
    public:
        Colorimeter();
        void initialize();

        void setNumSamples(uint16_t _numSamples);
        uint16_t getNumSamples();

        uint32_t getFrequencyRed();
        uint32_t getFrequencyGreen();
        uint32_t getFrequencyBlue();
        uint32_t getFrequencyWhite();
        FrequencyData getFrequencyAll();

        float getTransmissionRed();
        float getTransmissionGreen();
        float getTransmissionBlue();
        float getTransmissionWhite();
        TransmissionData getTransmissionAll();

        float getAbsorbanceRed();
        float getAbsorbanceGreen();
        float getAbsorbanceBlue();
        float getAbsorbanceWhite();
        AbsorbanceData getAbsorbanceAll();

        void calibrateRed();
        void calibrateGreen();
        void calibrateBlue();
        void calibrateWhite();
        void calibrate();

    private:
        RGBLed led;
        ColorSensor sensor;
        FrequencyData calibration;
        uint16_t numSamples;

};

float freq2trans(uint32_t calFreq, uint32_t sampleFreq);

float trans2absorb(float transmission);
#endif
