#include <math.h>
#include <EEPROM.h>
#include <Streaming.h>
#include "io_pins.h"
#include "RGBLed.h"
#include "ColorSensor.h"
#include "Colorimeter.h"
#include "EEPROMAnything.h"
#include "SerialReceiver.h"
#include "SerialHandler.h"

Colorimeter colorimeter;
SerialReceiver receiver;

void setup() {
    Serial.begin(9600);

    // Set software serial pins low to stop LCD from blinking
    pinMode(7,OUTPUT);
    pinMode(8,OUTPUT);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);

    //colorimeter.initialize();
    //colorimeter.numSamples = 1000;
    //colorimeter.EEPROM_loadCalibration();
    //colorimeter.calibrate();
    //colorimeter.EEPROM_saveCalibration();
}

void loop() {

    while (Serial.available() > 0) {
        receiver.process(Serial.read());
        if (receiver.messageReady()) {
            receiver.printMessage();
            receiver.reset();
        }
    }

    //colorimeter.getMeasurement();

    //Serial << "Calibration" << endl;
    //Serial << "red:   " << colorimeter.calibration.red << endl;
    //Serial << "green: " << colorimeter.calibration.green << endl;
    //Serial << "blue:  " << colorimeter.calibration.blue << endl;
    //Serial << "white: " << colorimeter.calibration.white << endl;
    //Serial << endl;

    //Serial << "Sample Frequency" << endl;
    //Serial << "red:   " << colorimeter.frequency.red << endl;
    //Serial << "green: " << colorimeter.frequency.green << endl;
    //Serial << "blue:  " << colorimeter.frequency.blue << endl;
    //Serial << "white: " << colorimeter.frequency.white << endl;
    //Serial << endl;

    //Serial << "Transmission" << endl;
    //Serial << "red:   " << colorimeter.transmission.red << endl;
    //Serial << "green: " << colorimeter.transmission.green << endl;
    //Serial << "blue:  " << colorimeter.transmission.blue << endl;
    //Serial << "white: " << colorimeter.transmission.white << endl;
    //Serial << endl;

    //Serial << "Absorbance" << endl;
    //Serial << "red:   " << colorimeter.absorbance.red << endl;
    //Serial << "green: " << colorimeter.absorbance.green << endl;
    //Serial << "blue:  " << colorimeter.absorbance.blue << endl;
    //Serial << "white: " << colorimeter.absorbance.white << endl;
    //Serial << endl;

    //delay(100);

}
