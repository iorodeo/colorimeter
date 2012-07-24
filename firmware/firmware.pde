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

Colorimeter colorimeter;
SerialHandler comm;

void setup() {
    Serial.begin(9600);
    colorimeter.initialize();
    colorimeter.numSamples = 500;
    //colorimeter.numSamples = 1000;
    //colorimeter.EEPROM_loadCalibration();
    
}

void loop() {
    comm.processInput();

    //colorimeter.led.setRed();
    //colorimeter.sensor.setChannelRed();

    //colorimeter.led.setGreen();
    //colorimeter.sensor.setChannelGreen();

    //colorimeter.led.setBlue();
    //colorimeter.sensor.setChannelBlue();

    //colorimeter.led.setWhite();
    //colorimeter.sensor.setChannelClear();
}
