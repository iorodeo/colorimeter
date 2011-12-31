#include <Streaming.h>
#include "io_pins.h"
#include "RGBLed.h"
#include "ColorSensor.h"

RGBLed led;
ColorSensor sensor;

void setup() {
    Serial.begin(9600);
    led.initialize(
        LED_RED_PIN, 
        LED_GRN_PIN, 
        LED_BLU_PIN
        );

    sensor.initialize(
        COLOR_SENSOR_S0,
        COLOR_SENSOR_S1,
        COLOR_SENSOR_S2,
        COLOR_SENSOR_S3,
        COLOR_SENSOR_FO
        );

    sensor.setChannelBlue();

}

void loop() {
    static bool state = false;
    long freq;

    if (state) {
        state = false;
        led.setBlue();
        Serial << "blue, ";
    }
    else {
        state = true;
        led.setGreen();
        Serial << "green, ";
    }
    freq = sensor.getFrequency(1000);
    Serial << "freq = " << freq << endl;

    delay(1000);
}
