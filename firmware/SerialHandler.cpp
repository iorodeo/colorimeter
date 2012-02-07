#include "WProgram.h"
#include "SerialHandler.h"
#include "Streaming.h"

const uint8_t DBL_STR_LEN = 30;
const uint8_t DBL_PREC = 12;

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

        default:
            unknownCmd();
            break;
    }
}

void SerialHandler::calibrate() { 
    colorimeter.calibrate();
    colorimeter.EEPROM_saveCalibration();
    Serial << '[' << RSP_SUCCESS << ']' << endl;
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

void SerialHandler::unknownCmd() { 
    // un-recognized command. Send error message.
    Serial << '[' << RSP_ERROR;
    Serial << ',' << "unknown command";
    Serial << "]" << endl;
}
