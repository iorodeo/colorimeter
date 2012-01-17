#include "Colorimeter.h"
#include "io_pins.h"

const uint8_t red = 1;
const uint8_t blue = 2;
const uint8_t green = 3;

Colorimeter::Colorimeter() {
    // Dummy values - later we will grab these values from eeprom
    calibration.red = 100000;
    calibration.green = 100000; 
    calibration.blue = 100000;
}

Colorimeter::initialize() {

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

Colorimeter::setNumSamples(uint16_t _numSamples) {
    numSamples = _numSamples;
}

uint16_t Colorimeter::getNumSamples() {
    return numSamples;
}

Colorimeter::getFrequencyRed() {
    led.setBlue();
    sensor.setChannelBlue();
    return sensor.getFrequency(numSamples);
}

Colorimeter::getFrequencyGreen() {
    led.setGreen();
    sensor.setChannelGreen();
    return sensor.getFrequency(numSamples);
}

Colorimeter::getFrequencyBlue() {
    led.setBlue();
    sensor.setChannelBlue();
    return sensor.getFrequency(numSamples);
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
        return 2.0;
    }
    else {
        transmission = freq2transmission(calibration.red,sampleFreq);
        return transmission;
    }
}

float Colorimeter::getTransimissionRed() {
    return getTransmission(red);
}

float Colorimeter::getTransmissionGreen() {
    return getTransmission(green);
}

float Colorimeter::getTransmissionBlue() {
    return getTransmission(blue);
}

float freq2transmission(uint32_t calFreq, uint32_t sampleFreq) {
    float trans;
    trans = calFreq/sampleFreq;
    if (trans > 1.0) {
        trans = 1.0;
    }
    return trans;
}
