#include <Arduino.h>
#include "Motor.h"

#define microStep 16;

//create motor object enable pins (a2 a1 a0) represent the binary value of the motor
Motor::Motor(bool a2, bool a1, bool a0){
  a2EN = a2;
  a1EN = a1;
  a0EN = a0;
}

//create motor object and also assign frequency (speed) and degrees (rotation amount)
Motor::Motor(bool a2, bool a1, bool a0, double percentage, double degrees){
  a2EN = a2;
  a1EN = a1;
  a0EN = a0;
  double frequency = percentage;
  highTime = (1/frequency)/2;
  stepCount = 200 * (degrees/360) * microStep; //200 steps = 360 degrees
}

//adjusts speed of motor by change the frequency at which the square wave is send to the driver
void Motor::setSpeed(double percentage){
  double frequency = percentage;
  highTime = (1/frequency)/4; 
}

//adjusts the number of square waves sent to the driver (number of steps)
void Motor::setDegrees(double degrees){
  stepCount = 200 * (degrees/360) * microStep; //200 steps = 360 degrees
}

//rotates motor in direction specified by dir. TRUE = clockwise, FALSE = counterclockwise
void Motor::rotate(bool dir){
  digitalWrite(6, a0EN); //enable proper motor driver through combinational logic
  digitalWrite(7, a1EN);
  digitalWrite(8, a2EN);

  digitalWrite(2, dir); //configure direction pin for motor driver

  for(int i = 0; i < stepCount; i++){  //send square wave to stepper driver based on stepCount and highTime
    digitalWrite(3, HIGH);
    delay(highTime*1000/10);    //delay is in ms -> x1000
    digitalWrite(3, LOW);
    delay(highTime*1000/10);  //always 50% duty cycle
  }

}
