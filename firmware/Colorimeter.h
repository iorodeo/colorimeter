#ifndef _COLORIMETER_H_
#define _COLORIMETER_H_
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include "ColorSensor.h"
#include "RGBLed.h"

enum SensorMode {
    COLOR_SPECIFIC=0,
    COLOR_INDEPENDENT,
};

extern const unsigned int DEFAULT_NUM_SAMPLES; 
extern const SensorMode DEFAULT_SENSOR_MODE; 

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

        uint32_t getFrequencyRed();
        uint32_t getFrequencyGreen();
        uint32_t getFrequencyBlue();
        uint32_t getFrequencyWhite();

        void getMeasurement();
        void getMeasurementRed();
        void getMeasurementGreen();
        void getMeasurementBlue();
        void getMeasurementWhite();

        void calibrate();
        void calibrateRed();
        void calibrateGreen();
        void calibrateBlue();
        void calibrateWhite();

        bool checkCalibration();
        bool checkCalibrationRed();
        bool checkCalibrationGreen();
        bool checkCalibrationBlue();
        bool checkCalibrationWhite();

        void EEPROM_saveCalibration();
        void EEPROM_saveCalibrationRed();
        void EEPROM_saveCalibrationGreen();
        void EEPROM_saveCalibrationBlue();
        void EEPROM_saveCalibrationWhite();
        void EEPROM_loadCalibration();

        void setSensorMode(SensorMode mode);

        RGBLed led;
        ColorSensor sensor;
        uint16_t numSamples;
        SensorMode sensorMode;

        ColorimeterData<uint32_t> calibration;
        ColorimeterData<uint32_t> frequency; 
        ColorimeterData<float> transmission;
        ColorimeterData<float> absorbance;
};

float freq2trans(uint32_t calFreq, uint32_t sampleFreq);

float trans2absorb(float transmission);
#endif
