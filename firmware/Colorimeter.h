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
        FrequencyData calibration;
        FrequencyData frequency;
        TransmissionData transmission;
        AbsorbanceData absorbance;
};

float freq2trans(uint32_t calFreq, uint32_t sampleFreq);

float trans2absorb(float transmission);
#endif
