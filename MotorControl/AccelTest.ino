#include <Arduino.h>
#include <HardwareSerial.h>

#define MOTOR_STEPS 200  // Motor steps per revolution
#define RPM 1200  // Target RPM for cruise speed
#define MOTOR_ACCEL 16000  // Acceleration and deceleration values are always in FULL steps / s^2
#define MOTOR_DECEL 16000

#define MICROSTEPS 2
#define DIR 2
#define STEP 3

#include "A4988.h"
A4988 stepperUP(MOTOR_STEPS, DIR, STEP);


void setup() {

  Serial.begin(9600);

  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT);

  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);

  digitalWrite(6, 0);
  digitalWrite(7, 0);
  digitalWrite(8, 0);

  unsigned long start = millis();

  stepperUP.begin(RPM, MICROSTEPS);
  stepperUP.setSpeedProfile(stepperUP.LINEAR_SPEED, MOTOR_ACCEL, MOTOR_DECEL);

  unsigned long startTime = millis();

  stepperUP.rotate(180);

  unsigned long totalTime = millis() - startTime;


  Serial.println(totalTime);
}

void loop() {

}
