#include <Streaming.h>
#include "io_pins.h"
#include "RGBLed.h"
#include "ColorSensor.h"
#include "Colorimeter.h"


Colorimeter colorimeter;

void setup() {
    Serial.begin(9600);
    colorimeter.initialize();
    colorimeter.setNumSamples(500);
}

void loop() {

    //FrequencyData data;
    //data = colorimeter.getFrequencies();
    TransmissionData data;
    data = colorimeter.getTransmissions();

    Serial << "red: " << data.red; 
    Serial << ", green: " << data.green;
    Serial << ", blue: " << data.blue;
    Serial << endl;
}
