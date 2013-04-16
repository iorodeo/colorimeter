#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include "SerialHandler.h"
#include "Streaming.h"

// Constants
// ----------------------------------------------------------------------------
const int CMD_CALIBRATE=0;
const int CMD_GET_MEASUREMENT=1;
const int CMD_SET_NUM_SAMPLES=2;
const int CMD_GET_NUM_SAMPLES=3;
const int CMD_GET_CALIBRATION=4;

const int CMD_CALIBRATE_RED=5;
const int CMD_CALIBRATE_GREEN=6;
const int CMD_CALIBRATE_BLUE=7;
const int CMD_CALIBRATE_WHITE=8;

const int CMD_GET_MEASUREMENT_RED=9;
const int CMD_GET_MEASUREMENT_GREEN=10;
const int CMD_GET_MEASUREMENT_BLUE=11;
const int CMD_GET_MEASUREMENT_WHITE=12;

const int CMD_SET_MODE_COLOR_SPECIFIC=13;
const int CMD_SET_MODE_COLOR_INDEPENDENT=14;
const int CMD_GET_SENSOR_MODE = 15;

const int RSP_ERROR = 0;
const int RSP_SUCCESS = 1;

const uint8_t DBL_STR_LEN = 30;
const uint8_t DBL_PREC = 12;



// Methods
// ----------------------------------------------------------------------------
void SerialHandler::processInput() { 
    while (Serial.available() > 0) {
        process(Serial.read());
        if (messageReady()) {
            switchYard();
            reset();
        }
    }
}

void SerialHandler::switchYard() { 
    uint8_t cmdId;

    cmdId = readInt(0); 

    switch (cmdId) {

        case CMD_CALIBRATE:
            calibrate();
            break;

        case CMD_GET_MEASUREMENT:
            sendMeasurement();
            break;

        case CMD_SET_NUM_SAMPLES:
            setNumSamples();
            break;

        case CMD_GET_NUM_SAMPLES:
            sendNumSamples();
            break;

        case CMD_GET_CALIBRATION:
            sendCalibration();
            break;

        case CMD_CALIBRATE_RED:
            calibrateRed();
            break;

        case CMD_CALIBRATE_GREEN:
            calibrateGreen();
            break;

        case CMD_CALIBRATE_BLUE:
            calibrateBlue();
            break;

        case CMD_CALIBRATE_WHITE:
            calibrateWhite();
            break;

        case CMD_GET_MEASUREMENT_RED:
            sendMeasurementRed();
            break;

        case CMD_GET_MEASUREMENT_GREEN:
            sendMeasurementGreen();
            break;

        case CMD_GET_MEASUREMENT_BLUE:
            sendMeasurementBlue();
            break;

        case CMD_GET_MEASUREMENT_WHITE:
            sendMeasurementWhite();
            break;

        case CMD_SET_MODE_COLOR_SPECIFIC:
            setModeColorSpecific();
            break;

        case CMD_SET_MODE_COLOR_INDEPENDENT:
            setModeColorIndependent();
            break;

        case CMD_GET_SENSOR_MODE:
            sendSensorMode();
            break;

        default:
            unknownCmd();
            break;
    }
}

void SerialHandler::calibrate() { 
    colorimeter.calibrate();
    if (colorimeter.checkCalibration() ) {
        colorimeter.EEPROM_saveCalibration();
        Serial << '[' << RSP_SUCCESS << ']' << endl;
    } 
    else {
        Serial << '[' << RSP_ERROR; 
        Serial << ',' << "calibration failed";
        Serial << ']' << endl;
    }
}

void SerialHandler::calibrateRed() {
    colorimeter.calibrateRed();
    if (colorimeter.checkCalibrationRed()) {
        colorimeter.EEPROM_saveCalibrationRed();
        Serial << '[' << RSP_SUCCESS << ']' << endl;
    }
    else {
        Serial << '[' << RSP_ERROR; 
        Serial << ',' << "calibration failed";
        Serial << ']' << endl;
    }
}

void SerialHandler::calibrateGreen() {
    colorimeter.calibrateGreen();
    if (colorimeter.checkCalibrationGreen()) {
        colorimeter.EEPROM_saveCalibrationGreen();
        Serial << '[' << RSP_SUCCESS << ']' << endl;
    }
    else {
        Serial << '[' << RSP_ERROR; 
        Serial << ',' << "calibration failed";
        Serial << ']' << endl;
    }
}

void SerialHandler::calibrateBlue() {
    colorimeter.calibrateBlue();
    if (colorimeter.checkCalibrationBlue()) {
        colorimeter.EEPROM_saveCalibrationBlue();
        Serial << '[' << RSP_SUCCESS << ']' << endl;
    }
    else {
        Serial << '[' << RSP_ERROR; 
        Serial << ',' << "calibration failed";
        Serial << ']' << endl;
    }
}

void SerialHandler::calibrateWhite() {
    colorimeter.calibrateWhite();
    if (colorimeter.checkCalibrationWhite()) {
        colorimeter.EEPROM_saveCalibrationWhite();
        Serial << '[' << RSP_SUCCESS << ']' << endl;
    }
    else {
        Serial << '[' << RSP_ERROR; 
        Serial << ',' << "calibration failed";
        Serial << ']' << endl;
    }
}

void SerialHandler::sendMeasurement() { 
    char valueStr[DBL_STR_LEN];

    colorimeter.getMeasurement();

    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.frequency.red);
    Serial << ',' << _DEC(colorimeter.frequency.green);
    Serial << ',' << _DEC(colorimeter.frequency.blue);
    Serial << ',' << _DEC(colorimeter.frequency.white);

    dtostre(colorimeter.transmission.red, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.transmission.green, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.transmission.blue, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.transmission.white, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;

    dtostre(colorimeter.absorbance.red, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.green, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.blue, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.white, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    Serial << ']' << endl;
}

void SerialHandler::setNumSamples() {
    long numSamples;
    numSamples = readLong(1);
    if ((numSamples > 0) && (numSamples <= 65535)) {
        colorimeter.numSamples = (uint16_t) numSamples;
        Serial << '[' << RSP_SUCCESS << ']' << endl;
    }
    else {
        Serial << '[' << RSP_ERROR; 
        Serial << ',' << "out of range";
        Serial << ']' << endl;
    }
} 

void SerialHandler::sendNumSamples() {
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.numSamples);
    Serial << ']' << endl;
}

void SerialHandler::sendCalibration() {
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.calibration.red);
    Serial << ',' << _DEC(colorimeter.calibration.green);
    Serial << ',' << _DEC(colorimeter.calibration.blue);
    Serial << ',' << _DEC(colorimeter.calibration.white);
    Serial << ']' << endl;
}

void SerialHandler::sendMeasurementRed() {
    char valueStr[DBL_STR_LEN];
    colorimeter.getMeasurementRed();
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.frequency.red);
    dtostre(colorimeter.transmission.red, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.red, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    Serial << ']' << endl;
}

void SerialHandler::sendMeasurementGreen() {
    char valueStr[DBL_STR_LEN];
    colorimeter.getMeasurementGreen();
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.frequency.green);
    dtostre(colorimeter.transmission.green, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.green, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    Serial << ']' << endl;
}

void SerialHandler::sendMeasurementBlue() {
    char valueStr[DBL_STR_LEN];
    colorimeter.getMeasurementBlue();
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.frequency.blue);
    dtostre(colorimeter.transmission.blue, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.blue, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    Serial << ']' << endl;
}

void SerialHandler::sendMeasurementWhite() {
    char valueStr[DBL_STR_LEN];
    colorimeter.getMeasurementWhite();
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.frequency.white);
    dtostre(colorimeter.transmission.white, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    dtostre(colorimeter.absorbance.white, valueStr, DBL_PREC, 0);
    Serial << ',' << valueStr;
    Serial << ']' << endl;
}

void SerialHandler::setModeColorSpecific() {
    colorimeter.setSensorMode(COLOR_SPECIFIC);
    Serial << '[' << RSP_SUCCESS << ']' << endl;
}

void SerialHandler::setModeColorIndependent() {
    colorimeter.setSensorMode(COLOR_INDEPENDENT);
    Serial << '[' << RSP_SUCCESS << ']' << endl;
}

void SerialHandler::sendSensorMode() {
    Serial << '[' << RSP_SUCCESS;
    Serial << ',' << _DEC(colorimeter.sensorMode);
    Serial << ']' << endl;
}

void SerialHandler::unknownCmd() { 
    // un-recognized command. Send error message.
    Serial << '[' << RSP_ERROR;
    Serial << ',' << "unknown command";
    Serial << "]" << endl;
}
