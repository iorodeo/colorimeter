#include <math.h>
#include "Colorimeter.h"
#include "io_pins.h"
#include "EEPROMAnything.h"
#include "Streaming.h"


const uint8_t EEPROM_CAL_RED = 0; 
const uint8_t EEPROM_CAL_GREEN = 4; 
const uint8_t EEPROM_CAL_BLUE = 8;
const uint8_t EEPROM_CAL_WHITE = 12;

const unsigned int DEFAULT_NUM_SAMPLES = 500;
const SensorMode DEFAULT_SENSOR_MODE = COLOR_SPECIFIC;

Colorimeter::Colorimeter() {
    numSamples = DEFAULT_NUM_SAMPLES;
    calibration.red = 1;
    calibration.green = 1; 
    calibration.blue = 1;
    calibration.white = 1;
    sensorMode = DEFAULT_SENSOR_MODE;
}

void Colorimeter::initialize() {

    led.initialize(
            LED_RED_PIN, 
            LED_GRN_PIN, 
            LED_BLU_PIN
            );

    sensor.initialize( 
            COLOR_SENSOR_S0, 
            COLOR_SENSOR_S1, 
            COLOR_SENSOR_S2, 
            COLOR_SENSOR_S3, 
            COLOR_SENSOR_FO
            );
}

// Sample frequency methods 
// ----------------------------------------------------------------------------
uint32_t Colorimeter::getFrequencyRed() {
    led.setRed();
    if (sensorMode == COLOR_SPECIFIC) {
        sensor.setChannelRed();
    }
    else {
        sensor.setChannelClear();
    }
    return sensor.getFrequency(numSamples);
}

uint32_t Colorimeter::getFrequencyGreen() {
    led.setGreen();
    if (sensorMode == COLOR_SPECIFIC) {
        sensor.setChannelGreen();
    }
    else {
        sensor.setChannelClear();
    }
    return sensor.getFrequency(numSamples);
}

uint32_t Colorimeter::getFrequencyBlue() {
    led.setBlue();
    if (sensorMode == COLOR_SPECIFIC) {
        sensor.setChannelBlue();
    }
    else {
        sensor.setChannelClear();
    }
    return sensor.getFrequency(numSamples);
}

uint32_t Colorimeter::getFrequencyWhite() {
    led.setWhite();
    sensor.setChannelClear();
    return sensor.getFrequency(numSamples);
} 

void Colorimeter::getMeasurement() {
    getMeasurementRed();
    getMeasurementGreen();
    getMeasurementBlue();
    getMeasurementWhite();
}

void Colorimeter::getMeasurementRed() {
    frequency.red = getFrequencyRed();
    led.setOff();
    transmission.red = freq2trans(calibration.red, frequency.red);
    absorbance.red = trans2absorb(transmission.red);
}

void Colorimeter::getMeasurementGreen() {
    frequency.green = getFrequencyGreen();
    led.setOff();
    transmission.green = freq2trans(calibration.green, frequency.green);
    absorbance.green = trans2absorb(transmission.green);
}

void Colorimeter::getMeasurementBlue() {
    frequency.blue = getFrequencyBlue();
    led.setOff();
    transmission.blue = freq2trans(calibration.blue, frequency.blue);
    absorbance.blue = trans2absorb(transmission.blue); 
}

void Colorimeter::getMeasurementWhite() {
    frequency.white = getFrequencyWhite();
    led.setOff();
    transmission.white = freq2trans(calibration.white, frequency.white);
    absorbance.white = trans2absorb(transmission.white);
}

// Calibration methods // ----------------------------------------------------------------------------
void Colorimeter::calibrate() {
    calibrateRed();
    calibrateGreen();
    calibrateBlue();
    calibrateWhite();
}

void Colorimeter::calibrateRed() {
    calibration.red = getFrequencyRed();
    led.setOff();
}

void Colorimeter::calibrateGreen() {
    calibration.green = getFrequencyGreen();
    led.setOff();
}

void Colorimeter::calibrateBlue() {
    calibration.blue = getFrequencyBlue();
    led.setOff();
}

void Colorimeter::calibrateWhite() {
    calibration.white = getFrequencyWhite();
    led.setOff();
}

void Colorimeter::EEPROM_saveCalibration() {
    EEPROM_saveCalibrationRed();
    EEPROM_saveCalibrationGreen();
    EEPROM_saveCalibrationBlue();
    EEPROM_saveCalibrationWhite();
}

void Colorimeter::EEPROM_saveCalibrationRed() {
    EEPROM_writeAnything(EEPROM_CAL_RED,calibration.red);
}

void Colorimeter::EEPROM_saveCalibrationGreen() {
    EEPROM_writeAnything(EEPROM_CAL_GREEN,calibration.green);
}

void Colorimeter::EEPROM_saveCalibrationBlue() {
    EEPROM_writeAnything(EEPROM_CAL_BLUE,calibration.blue);
}

void Colorimeter::EEPROM_saveCalibrationWhite() {
    EEPROM_writeAnything(EEPROM_CAL_WHITE,calibration.white);
}
void Colorimeter::EEPROM_loadCalibration() {
    EEPROM_readAnything(EEPROM_CAL_RED,calibration.red);
    EEPROM_readAnything(EEPROM_CAL_GREEN,calibration.green);
    EEPROM_readAnything(EEPROM_CAL_BLUE,calibration.blue);
    EEPROM_readAnything(EEPROM_CAL_WHITE,calibration.white);
}

bool Colorimeter::checkCalibration() {
    bool flag = true;
    flag &= checkCalibrationRed();
    flag &= checkCalibrationGreen();
    flag &= checkCalibrationBlue();
    flag &= checkCalibrationWhite();
    return flag;
}

bool Colorimeter::checkCalibrationRed() {
    bool flag = true;
    if (calibration.red == 0) {
        flag = false;
    }
    return flag;
}

bool Colorimeter::checkCalibrationGreen() {
    bool flag = true;
    if (calibration.green == 0) {
        flag = false;
    }
    return flag;
}

bool Colorimeter::checkCalibrationBlue() {
    bool flag = true;
    if (calibration.blue == 0) {
        flag = false;
    }
    return flag;
}

bool Colorimeter::checkCalibrationWhite() {
    bool flag = true;
    if (calibration.white == 0) {
        flag = false;
    }
    return flag;
}

void Colorimeter::setSensorMode(SensorMode mode) {
    sensorMode = mode;
}

// Utility functions
// ----------------------------------------------------------------------------
float freq2trans(uint32_t calFreq, uint32_t sampleFreq) {
    float trans;
    if (calFreq == 0) {
        trans = -1.0;
    }
    else {
        trans = ((float) sampleFreq)/((float) calFreq);
        if (trans > 1.0) {
            trans = 1.0;
        }
    }
    return trans;
}

float trans2absorb(float transmission) { 
    float absorb;
    if (transmission > 0) {
        absorb = (float)log10( 1.0/((double) transmission));
    }
    else {
        absorb = -1.0;
    }
    return absorb;
}

