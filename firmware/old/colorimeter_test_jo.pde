#include <Streaming.h>

#define BLU_LED A1
#define GRN_LED A2
#define RED_LED A3

#define S0   A0
#define S1   5
#define S2   3
#define S3   4
#define FREQOUT  2       
#define SAMPLES 5000

#define CURRENT_LED RED_LED

void setup() {

    Serial.begin(9600);

    pinMode(BLU_LED, OUTPUT);
    pinMode(GRN_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);
    pinMode(S0, OUTPUT); 
    pinMode(S1, OUTPUT); 
    pinMode(S2, OUTPUT); 
    pinMode(S3, OUTPUT); 
    pinMode(FREQOUT, INPUT);

    // Set all LEDs off 
    digitalWrite(BLU_LED,LOW);
    digitalWrite(GRN_LED,LOW); 
    digitalWrite(RED_LED,LOW);

    // Set frequency scaling 
    digitalWrite(S0,HIGH);
    digitalWrite(S1,HIGH);

} 

void loop() {
    
    long freqBlue;
    long freqGreen;
    long freqRed;
    long freqClear;
//
//    // Set LED state
    digitalWrite(CURRENT_LED,HIGH); 
    Serial << "LED: on" << endl;
   
    delay(50);
    setChannelBlue();
    freqBlue = getFrequency(FREQOUT);
    setChannelGreen();
    freqGreen = getFrequency(FREQOUT);
    setChannelRed();
    freqRed = getFrequency(FREQOUT);
    setChannelClear();
    freqClear = getFrequency(FREQOUT);
//
    //Serial << "blue: " << freqBlue << endl;
    //Serial << "green: " << freqGreen << endl;
    Serial << "red: " << freqRed << endl;
    Serial << "clear: " << freqClear << endl;
    Serial << endl;
//
    
   delay(20);
}



void setChannelBlue() {
    digitalWrite(S2,LOW);
    digitalWrite(S3,HIGH);
}

void setChannelGreen() {
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
}

void setChannelRed() {
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
}

void setChannelClear() {
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
}

long getFrequency(int pin) {
    long dt;
    long freq = 0;
    for(unsigned int j=0; j<SAMPLES; j++) {
        //Serial << "  sample: " << j << endl;
        dt = pulseIn(pin, HIGH, 250000);
        //Serial << "dt: " << dt << endl;
        freq+= 500000/dt;
    }
    return freq / SAMPLES;
}


