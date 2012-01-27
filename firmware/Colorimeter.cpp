#include <math.h>
#include "Colorimeter.h"
#include "io_pins.h"
#include "EEPROMAnything.h"


const uint8_t EERPOM_CAL_RED = 0; 
const uint8_t EEPROM_CAL_GREEN = 4; 
const uint8_t EEPROM_CAL_BLUE = 8;
const uint8_t EEPROM_CAL_WHITE = 12;


Colorimeter::Colorimeter() {
    numSamples = DEFAULT_NUM_SAMPLES;
    // Dummy values - later we will grab these values from eeprom
    calibration.red = 100000;
    calibration.green = 100000; 
    calibration.blue = 100000;
    calibration.white = 100000;
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

void Colorimeter::setNumSamples(uint16_t _numSamples) {
    numSamples = _numSamples;
}

uint16_t Colorimeter::getNumSamples() {
    return numSamples;
}

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


FrequencyData Colorimeter::getFrequencyAll() {
    FrequencyData data;
    data.red = getFrequencyRed();
    data.green = getFrequencyGreen();
    data.blue = getFrequencyBlue();
    data.white = getFrequencyWhite();
    return data;
}

float Colorimeter::getTransmissionRed() {
    uint32_t sampleFreq;
    sampleFreq = getFrequencyRed();
    return freq2trans(calibration.red,sampleFreq);
}

float Colorimeter::getTransmissionGreen() {
    uint32_t sampleFreq;
    sampleFreq = getFrequencyGreen();
    return freq2trans(calibration.green,sampleFreq);
}

float Colorimeter::getTransmissionBlue() {
    uint32_t sampleFreq;
    sampleFreq = getFrequencyBlue();
    return freq2trans(calibration.blue,sampleFreq);
}

float Colorimeter::getTransmissionWhite() {
    uint32_t sampleFreq;
    sampleFreq = getFrequencyWhite();
    return freq2trans(calibration.white,sampleFreq);
}

TransmissionData Colorimeter::getTransmissionAll() {
    TransmissionData data;
    data.red = getTransmissionRed();
    data.green = getTransmissionGreen();
    data.blue = getTransmissionBlue();
    data.white = getTransmissionWhite();
    return data;
}

float Colorimeter::getAbsorbanceRed() {
    float trans;
    trans = getTransmissionRed();
    return trans2absorb(trans);
}

float Colorimeter::getAbsorbanceGreen() {
    float trans;
    trans = getTransmissionGreen();
    return trans2absorb(trans);
}

float Colorimeter::getAbsorbanceBlue() {
    float trans;
    trans = getTransmissionBlue();
    return trans2absorb(trans);
}

float Colorimeter::getAbsorbanceWhite() {
    float trans;
    trans = getTransmissionWhite();
    return trans2absorb(trans);
}

AbsorbanceData Colorimeter::getAbsorbanceAll() {
    AbsorbanceData data;
    data.red = getAbsorbanceRed();
    data.green = getAbsorbanceGreen();
    data.blue = getAbsorbanceBlue();
    data.white = getAbsorbanceWhite();
    return data;
}

void Colorimeter::calibrateRed() {
    uint32_t sampleFreq;
    sampleFreq = getFrequencyRed();

}

float freq2trans(uint32_t calFreq, uint32_t sampleFreq) {
    float trans;
    trans = calFreq/sampleFreq;
    if (trans > 1.0) {
        trans = 1.0;
    }
    return trans;
}

float trans2absorb(float transmission) { 
    return  (float)log10( 1.0/((double) transmission));
}

