#include <math.h>
#include <EEPROM.h>
#include <Streaming.h>
#include "io_pins.h"
#include "RGBLed.h"
#include "ColorSensor.h"
#include "Colorimeter.h"
#include "EEPROMAnything.h"

Colorimeter colorimeter;

void setup() {
    Serial.begin(9600);
    colorimeter.initialize();
    colorimeter.setNumSamples(5000);

    pinMode(7,OUTPUT);
    pinMode(8,OUTPUT);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
}

void loop() {

    //FrequencyData data;
    //data = colorimeter.getFrequencyAll();
    

    //TransmissionData data;
    //data = colorimeter.getTransmissionAll();
    AbsorbanceData data;
    data = colorimeter.getAbsorbanceAll();

    delay(10);

    //Serial << "red: " << data.red; 
    //Serial << ", green: " << data.green;
    //Serial << ", blue: " << data.blue;
    //Serial << endl;
}
