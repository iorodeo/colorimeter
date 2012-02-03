#ifndef _SERIAL_HANDLER_H_
#define _SERIAL_HANDLER_H_
#include "SerialReceiver.h"
#include "Colorimeter.h"



const int CMD_CALIBRATE=0;
const int CMD_GET_MEASUREMENT=1;
const int CMD_SET_NUM_SAMPLES=2;
const int CMD_GET_NUM_SAMPLES=3;
const int CMD_GET_CALIBRATION=4;

const int RSP_ERROR = 0;
const int RSP_SUCCESS = 1;

class SerialHandler: public SerialReceiver {
    public:
        void processInput();
    private:
        void switchYard();
        void calibrate();
        void sendMeasurement();
        void setNumSamples();
        void sendNumSamples();
        void sendCalibration();
        void unknownCmd();
};

extern Colorimeter colorimeter;

#endif


