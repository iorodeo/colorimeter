#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include "Streaming.h"
#include "tests.h"

void led_cycle_test() {
    // A simple test of the rgb led. When put in the main loop this function
    // cycles through the four possible outputs with a 1 second delay.
    static int state = 0;
    switch (state) {
        case 0:
            colorimeter.led.setRed();
            break;

        case 1:
            colorimeter.led.setGreen();
            break;

        case 2:
            colorimeter.led.setBlue();
            break;
        case 3:
            colorimeter.led.setWhite();
            break;
        default:
            state = 0;
            break;
    }
    state++;
    if (state == 4) {
        state = 0;
    }
    delay(1000);
}


void test_get_frequencies() { 
    // Tests the getFrequency methods of the colorimeter.
    Serial << "Red:   " << _DEC(colorimeter.getFrequencyRed())   << endl;
    delay(100);
    Serial << "Green: " << _DEC(colorimeter.getFrequencyGreen()) << endl;
    delay(100);
    Serial << "Blue:  " << _DEC(colorimeter.getFrequencyBlue())  << endl;
    delay(100);
    Serial << "White:  " << _DEC(colorimeter.getFrequencyWhite())  << endl;
    delay(100);
}
