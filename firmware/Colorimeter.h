#ifndef _COLORIMETER_H_
#define _COLORIMETER_H_
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include "ColorSensor.h"
#include "RGBLed.h"

#define DEFAULT_NUM_SAMPLES 5000

template <class T>
class ColorimeterData {
    public:
        T red;
        T green;
        T blue;
        T white;
};
            
class Colorimeter {
    public:

        Colorimeter();
        void initialize();

        RGBLed led;
        ColorSensor sensor;

        uint32_t getFrequencyRed();
        uint32_t getFrequencyGreen();
        uint32_t getFrequencyBlue();
        uint32_t getFrequencyWhite();
        void getMeasurement();

        void calibrate();
        void EEPROM_saveCalibration();
        void EEPROM_loadCalibration();

        uint16_t numSamples;
        ColorimeterData<uint32_t> calibration;
        ColorimeterData<uint32_t> frequency; 
        ColorimeterData<float> transmission;
        ColorimeterData<float> absorbance;
};

float freq2trans(uint32_t calFreq, uint32_t sampleFreq);

float trans2absorb(float transmission);
#endif
