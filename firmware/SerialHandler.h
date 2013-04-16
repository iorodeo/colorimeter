#ifndef _SERIAL_HANDLER_H_
#define _SERIAL_HANDLER_H_
#include "SerialReceiver.h"
#include "Colorimeter.h"


class SerialHandler: public SerialReceiver {
    public:
        void processInput();
    private:
        void switchYard();
        void calibrate();
        void calibrateRed();
        void calibrateGreen();
        void calibrateBlue();
        void calibrateWhite();
        void sendMeasurement();
        void setNumSamples();
        void sendNumSamples();
        void sendCalibration();
        void sendMeasurementRed();
        void sendMeasurementGreen();
        void sendMeasurementBlue();
        void sendMeasurementWhite();
        void setModeColorSpecific();
        void setModeColorIndependent();
        void sendSensorMode();
        void unknownCmd();
};

extern Colorimeter colorimeter;

#endif


