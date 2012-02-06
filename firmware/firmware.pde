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
#include "tests.h"

void disableLCD();

Colorimeter colorimeter;
SerialHandler comm;

void setup() {
    disableLCD();
    Serial.begin(9600);
    colorimeter.initialize();
    colorimeter.numSamples = 1000;
    //colorimeter.EEPROM_loadCalibration();
    
}

void loop() {
    comm.processInput();
    //test_get_frequencies();
}

void disableLCD() {
    pinMode(7,OUTPUT);
    pinMode(8,OUTPUT);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
}

