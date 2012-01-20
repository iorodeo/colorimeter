#include <math.h>
#include "Colorimeter.h"
#include "io_pins.h"

const uint8_t red = 1;
const uint8_t blue = 2;
const uint8_t green = 3;

Colorimeter::Colorimeter() {
    numSamples = DEFAULT_NUM_SAMPLES;
    // Dummy values - later we will grab these values from eeprom
    calibration.red = 100000;
    calibration.green = 100000; 
    calibration.blue = 100000;
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

uint8_t Colorimeter::getFrequency(uint8_t colorNum) {

}

FrequencyData Colorimeter::getFrequencyAll() {
    FrequencyData data;
    data.red = getFrequencyRed();
    data.green = getFrequencyGreen();
    data.blue = getFrequencyBlue();
    return data;
}

float Colorimeter::getTransmission(uint8_t colorNum) {
    uint32_t sampleFreq;
    float trans;
    bool error = false;
    switch (colorNum) {
        case red:
            sampleFreq = getFrequencyRed();
            break;
        case green:
            sampleFreq = getFrequencyGreen();
            break;
        case blue:
            sampleFreq = getFrequencyBlue();
            break;
        default:
            error = true;
            break;
    }
    if (error) {
        return -1.0;
    }
    else {
        return freq2trans(calibration.red,sampleFreq);
    }
}

float Colorimeter::getTransmissionRed() {
    return getTransmission(red);
}

float Colorimeter::getTransmissionGreen() {
    return getTransmission(green);
}

float Colorimeter::getTransmissionBlue() {
    return getTransmission(blue);
}

TransmissionData Colorimeter::getTransmissionAll() {
    TransmissionData data;
    data.red = getTransmissionRed();
    data.green = getTransmissionGreen();
    data.blue = getTransmissionBlue();
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

float Colorimeter::getAbsorbance(uint8_t colorNum) {
    float absorb;
    switch (colorNum) {
        case red:
            absorb = getAbsorbanceRed();
            break;

        case green:
            absorb = getAbsorbanceGreen();
            break;

        case blue:
            absorb = getAbsorbanceBlue();
            break;

        default:
            absorb = -1.0;
            break;
    }
    return absorb;
}

AbsorbanceData Colorimeter::getAbsorbanceAll() {
    AbsorbanceData data;
    data.red = getAbsorbanceRed();
    data.green = getAbsorbanceGreen();
    data.blue = getAbsorbanceBlue();
    return data;
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

