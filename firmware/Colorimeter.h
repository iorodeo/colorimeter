#include "ColorSensor.h"
#include "RGBLed.h"

class CalibrationData {
    public:
        uint32_t red;
        uint32_t green;
        uint32_t blue;
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

        float getTransmissionRed();
        float getTransmissionGreen();
        float getTransmissionBlue();
        float getTransmission(uint8_t colorNum);

        float getAbsorbanceRed();
        float getAbsorbanceGreen();
        float getAbsorbanceBlue();
        float getAbsorbance(uint8_t colorNum);

        void calibrateRed();
        void calibrateGreen();
        void calibrateBlue();
        void calibrate();

    private:
        uint16_t numSamples;
        RGBLed led;
        ColorSensor sensor;
        CalibrationData calibration;

};

