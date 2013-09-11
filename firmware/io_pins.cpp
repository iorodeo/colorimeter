#include "io_pins.h"
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#ifndef BLE_SHIELD

// IO Pins for UNO Shield 
// --------------------------------------------------------

// RGB LED Control Pins
const int LED_BLU_PIN = 9; 
const int LED_GRN_PIN = 10; 
const int LED_RED_PIN = 11;

// Color Sensor Control Pins
const int COLOR_SENSOR_S0 = 4; 
const int COLOR_SENSOR_S1 = 5; 
const int COLOR_SENSOR_S2 = 6; 
const int COLOR_SENSOR_S3 = 7; 
const int COLOR_SENSOR_FO = 8;       

#else

// IO Pins for BLE shield
// --------------------------------------------------------

// RGB LED Control Pins
const int LED_BLU_PIN = 3; 
const int LED_GRN_PIN = A1; 
const int LED_RED_PIN = A0;

// Color Sensor Control Pins
const int COLOR_SENSOR_S0 = 4; 
const int COLOR_SENSOR_S1 = 5; 
const int COLOR_SENSOR_S2 = 6; 
const int COLOR_SENSOR_S3 = 7; 
const int COLOR_SENSOR_FO = 2;       

#endif

