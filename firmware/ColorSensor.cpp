// ColorSensor.cpp
//
// Interface to ??? rgb color sensor
#include "ColorSensor.h"

void ColorSensor::initialize(uint8_t _S0, uint8_t _S1, uint8_t _S2, uint8_t _S3, uint8_t _FO) {

    S0 = _S0;
    S1 = _S1;
    S2 = _S2;
    S3 = _S3;
    FO = _FO;

    // Set correct pin modes
    pinMode(S0, OUTPUT); 
    pinMode(S1, OUTPUT); 
    pinMode(S2, OUTPUT); 
    pinMode(S3, OUTPUT); 
    pinMode(FO, INPUT);

    setOutputFreqScale(OUTPUT_FREQSCALE_100);

    timeoutCountMax = DFLT_TIMEOUT_COUNT_MAX;
    pulseInWait = DFLT_PULSE_IN_WAIT;
}

uint32_t ColorSensor::getFrequency(uint16_t numSamples) {
    uint32_t dt;
    uint32_t freq = 0;
    uint16_t _numSamples = numSamples;
    uint16_t timeoutCount = 0;

    for(uint16_t j=0; j<numSamples; j++) {
        dt = pulseIn(FO, HIGH, pulseInWait);
        if (dt > 0) {
            freq+= 500000/dt;
        }
        else {
            _numSamples -= 1;
            timeoutCount += 1;
        }
        if (timeoutCount > timeoutCountMax) {
            freq = 0;
            _numSamples = 1;
            break;
        }
    }
    return freq/_numSamples;
}

void ColorSensor::setChannelBlue() {
    digitalWrite(S2,LOW);
    digitalWrite(S3,HIGH);
}

void ColorSensor::setChannelGreen() {
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
}

void ColorSensor::setChannelRed() {
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
}

void ColorSensor::setChannelClear() {
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
}

void ColorSensor::setOutputFreqScale(FreqScale value) {
    switch (value)
    {
        case OUTPUT_FREQSCALE_0:
            digitalWrite(S0,LOW); 
            digitalWrite(S1,LOW);
            break;
            
        case OUTPUT_FREQSCALE_2:
            digitalWrite(S0,LOW); 
            digitalWrite(S1,HIGH);
            break;

        case OUTPUT_FREQSCALE_20:
            digitalWrite(S0,HIGH);
            digitalWrite(S1,LOW);
            break;

        default:
            digitalWrite(S0,HIGH);
            digitalWrite(S1,HIGH);
            break;
    }
}
