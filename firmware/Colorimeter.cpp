#include <math.h>
#include "Colorimeter.h"
#include "io_pins.h"
#include "EEPROMAnything.h"
#include "Streaming.h"


const uint8_t EEPROM_CAL_RED = 0; 
const uint8_t EEPROM_CAL_GREEN = 4; 
const uint8_t EEPROM_CAL_BLUE = 8;
const uint8_t EEPROM_CAL_WHITE = 12;


Colorimeter::Colorimeter() {
    numSamples = DEFAULT_NUM_SAMPLES;
    calibration.red = 1;
    calibration.green = 1; 
    calibration.blue = 1;
    calibration.white = 1;
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
    sensor.setChannelRed();
    return sensor.getFrequency(numSamples);
}

uint32_t Colorimeter::getFrequencyGreen() {
    led.setGreen();
    sensor.setChannelGreen();
    return sensor.getFrequency(numSamples);
}

uint32_t Colorimeter::getFrequencyBlue() {
    led.setBlue();
    sensor.setChannelBlue();
    return sensor.getFrequency(numSamples);
}

uint32_t Colorimeter::getFrequencyWhite() {
    led.setWhite();
    sensor.setChannelClear();
    return sensor.getFrequency(numSamples);
}


void Colorimeter::getMeasurement() {
    frequency.red = getFrequencyRed();
    frequency.green = getFrequencyGreen();
    frequency.blue = getFrequencyBlue();
    frequency.white = getFrequencyWhite();
    led.setOff();

    transmission.red = freq2trans(calibration.red, frequency.red);
    transmission.green = freq2trans(calibration.green, frequency.green);
    transmission.blue = freq2trans(calibration.blue, frequency.blue);
    transmission.white = freq2trans(calibration.white, frequency.white);

    absorbance.red = trans2absorb(transmission.red);
    absorbance.green = trans2absorb(transmission.green);
    absorbance.blue = trans2absorb(transmission.blue); 
    absorbance.white = trans2absorb(transmission.white);
}

// Calibration methods // ----------------------------------------------------------------------------
void Colorimeter::calibrate() {
    calibration.red = getFrequencyRed();
    calibration.green = getFrequencyGreen();
    calibration.blue = getFrequencyBlue();
    calibration.white = getFrequencyWhite();
    led.setOff();
}

void Colorimeter::EEPROM_saveCalibration() {
    EEPROM_writeAnything(EEPROM_CAL_RED,calibration.red);
    EEPROM_writeAnything(EEPROM_CAL_GREEN,calibration.green);
    EEPROM_writeAnything(EEPROM_CAL_BLUE,calibration.blue);
    EEPROM_writeAnything(EEPROM_CAL_WHITE,calibration.white);
}

void Colorimeter::EEPROM_loadCalibration() {
    EEPROM_readAnything(EEPROM_CAL_RED,calibration.red);
    EEPROM_readAnything(EEPROM_CAL_GREEN,calibration.green);
    EEPROM_readAnything(EEPROM_CAL_BLUE,calibration.blue);
    EEPROM_readAnything(EEPROM_CAL_WHITE,calibration.white);
}


// Utility functions
// ----------------------------------------------------------------------------
float freq2trans(uint32_t calFreq, uint32_t sampleFreq) {
    float trans;
    trans = ((float) sampleFreq)/((float) calFreq);
    if (trans > 1.0) {
        trans = 1.0;
    }
    return trans;
}

float trans2absorb(float transmission) { 
    return  (float)log10( 1.0/((double) transmission));
}

