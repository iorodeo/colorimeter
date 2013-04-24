#include <math.h>
#include <EEPROM.h>
#include "Streaming.h"
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
}

void loop() {
    comm.processInput();
}
