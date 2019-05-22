// Date Created:      May 17, 2019
// Created By:        Andrew N. Sanchez
// Project Titled:    Donkey Car Speedometer
// Description:       Displays speed on 4 Digit 7 Segment but sends speed and distance through serial

#include <FlexiTimer2.h>

#define PI 3.1415926535897932384626433832795

#define ENCODE_PIN_A 2
#define RADIUS 3.2          // Set radius of 1 rev to units of distance
#define PULSES_PER_REV 600  // LPD2806 Rotary Encoder gives 600 pulses per revolution
                            // Change this value according to your encoder
#define LATCH_PIN 12        // Pin connected to ST_CP of 74HC595（Pin12）
#define CLK_PIN 13         // Pin connected to SH_CP of 74HC595（Pin11）
#define DATA_PIN 11        // Pin connected to DS of 74HC595（Pin14）

int com_pin[] = {7, 6, 5, 4}; // Common pin (anode) of 4 digit 7-segment disp

// Define the encoding of characters 0-F of the common-anode 7-Segment Display
byte num[] = {0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90, 0x88, 0x83, 0xc6, 0xa1, 0x86, 0x8e};

volatile unsigned int counter = 0; // encoder counter
volatile unsigned int revolutions = 0;  // encoder revolutions

float velocity;

void setup() {
  Serial.begin(9600);

  // set pins for encoder
  pinMode(ENCODE_PIN_A, INPUT); // set encoder pin
  digitalWrite(ENCODE_PIN_A, HIGH); // turn on pull up resistor
  attachInterrupt(0, enc_trigger, RISING); // set interrupts for rising pulses sent from encoder

  // set pins for display
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLK_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  for (int i = 0; i < 4; i++)
  {
    pinMode(com_pin[i], OUTPUT);
  }

  //Timer Interrupts
  FlexiTimer2::set(1000, calc_speed);  // timer interrupts every second
  FlexiTimer2::start();  // timer start
}

void loop() {
  send_speed();
  disp_speed();
}

void send_speed() {
  float v = velocity;
  byte * chunks = (byte *) &v;
  Serial.write(chunks, 4);  // send float
}

//currently does not display precision values
void disp_speed() {

  int v = (int) velocity;  //get current speed

  // get digits to display
  byte bit[4];
  bit[0] = v % 10;
  bit[1] = v / 10 % 10;
  bit[2] = v / 100 % 10;
  bit[3] = v / 1000 % 10;

  for (int i = 0; i < 4; i++) {
    // Select a single 7-segment display
    chooseCommon(i);
    // Send data to 74HC595
    int write_val = num[bit[3-i]];
    // write_val | 0x01                inject decimal
    writeData(write_val);
    delay(5);
  }
}

void chooseCommon(byte com) {
  // Close all single 7-segment display
  for (int i = 0; i < 4; i++) {
    digitalWrite(com_pin[i], LOW);
  }
  // Open the selected single 7-segment display
  digitalWrite(com_pin[com], HIGH);
}

void writeData(int value) {
  // Make latchPin output low level
  digitalWrite(LATCH_PIN, LOW);
  // Send serial data to 74HC595
  shiftOut(DATA_PIN, CLK_PIN, LSBFIRST, value);
  // Make latchPin output high level, then 74HC595 will update the data to parallel output
  digitalWrite(LATCH_PIN, HIGH);
}

// INTERRUPT FUNCITONS

// fires at rising encoder pulse
void enc_trigger() {
  counter++;
  if( counter == PULSES_PER_REV ) {
    revolutions++;
  }
  counter = 0; // reset
}

// fires after 1 second has passed
void calc_speed() {
  velocity = revolutions*(2*PI*RADIUS);
  revolutions = 0; // reset revolutions for next revolution count per second
}
