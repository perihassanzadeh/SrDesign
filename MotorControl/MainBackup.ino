//U L F R B D U' L' F' R' B' D'
#include "Motor.h"
#include "DFRobot_RGBLCD1602.h"

//MOTOR CONTROL//
#define dirPin 2  //pin 4
#define stepPin 3 //pin 5
#define a0Pin 6   //pin 12
#define a1Pin 7   //pin 13
#define a2Pin 8   //pin 14

Motor motor1 = Motor(0, 0, 0, 500, 90);  //global motor objects
Motor motor2 = Motor(0, 0, 1, 500, 90);
Motor motor3 = Motor(0, 1, 0, 500, 90);
Motor motor4 = Motor(0, 1, 1, 500, 90);
Motor motor5 = Motor(1, 0, 0, 500, 90);
Motor motor6 = Motor(1, 0, 1, 500, 90);

//LCD SCREEN//
DFRobot_RGBLCD1602 lcd(16, 2); //global lcd object

//BUTTONS//
#define button1 A3   //pin 26
#define button2 A2   //pin 25
volatile bool B1Flag = 0;  //Flags to be used by interrupt - goes high (1) when button is pushed
volatile bool B2Flag = 0;
#define button1Led A0  //pin 23
#define button2Led 5  //pin 11

//ENCODER BUTTON
#define buttonE A1   //pin 24
volatile bool BEFlag = 0;

//ENCODER
#define EncA 10  //pin 16
#define EncB 9   //pin 15
//volatile int lastEncPos = 0;  //stores previous encoder position
volatile bool CWFlag = 0;  //Clockwise flag  -  goes high when encoder rotated clockwise
volatile bool CCWFlag = 0;  //Counter-clockwise flag ...

//SYSTEM VARIABLES//
#define led 4  //onboard led  //pin 6
int speed = 50;   //controlled by encoder


void setup() {
  //START SERIAL PORT//
  Serial.begin(9600);
  Serial.println("Starting up");

  //LCD SCREEN INITIALIZATION//
  lcd.init();
  lcd.setRGB(100, 100, 100);
  lcd.setCursor(0, 0);
  lcd.print("Time:");
  lcd.setCursor(0, 1);  //for test debugging - display seconds in bottom left of screen
  lcd.print("Btn:"); //print seconds since startup
  lcd.setCursor(7, 1);  //for test debugging - display seconds in bottom left of screen
  lcd.print("Spe:"); //print seconds since startup
  lcd.print(speed);

  //MOTOR OUTPUT PIN DEFINITIONS//
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(a0Pin, OUTPUT);
  pinMode(a1Pin, OUTPUT);
  pinMode(a2Pin, OUTPUT);

  //BUTTON INPUT PIN DEFINTIONS AND INTERRUPTS// - (PIN CHANGE INTERRUPT)
  pinMode(button1, INPUT);  //using an external 4.7k pulldown resistor
  pinMode(button2, INPUT);
  pinMode(buttonE, INPUT);
  PCICR |= B00000010;  //Enable pin change interrupt on port C (A0-A5) (pins 23-28)
  PCMSK1 |= B00001110;  //Enable interrupts for pins A0-A2 (pins 24-26)

  //BUTTON LEDs
  pinMode(button1Led, OUTPUT);
  pinMode(button2Led, OUTPUT);

  //ENCODER INPUT PIN DEFINTIONS, INTERRUPTS, AND POSITION CONFIG//
  pinMode(EncA, INPUT);  //using an external 10k pullup resistor
  pinMode(EncB, INPUT);
  PCICR |= B00000001;  //Enable pin change interrupt on port B (D8-D13) (pins 14-19)
  PCMSK0 |= B00000100;  //Enable interrupts for pin D10 (pin 16, EncA)  //for old encoder:PCMSK0 |= B00000110;  //Enable interrupts for pins D9-D10 (pins 15-16)
  //lastEncPos = encoderInputToState(digitalRead(EncA), digitalRead(EncB)); //set to current (previous) position  //used with old encoder

  //LED
  pinMode(led, OUTPUT);
}

void loop() 
{
  lcd.setCursor(5, 0);  //for test debugging - display seconds in bottom left of screen
  lcd.print(millis()/1000); //print seconds since startup

  //PUSH BUTTON HANDLERS
  if(B1Flag == 1){
    lcd.setCursor(4,1);
    lcd.print("1");
    digitalWrite(button1Led, HIGH);
    delay(600);
    digitalWrite(button1Led, LOW);
    B1Flag = 0;
  }
  if(B2Flag == 1){
    lcd.setCursor(4,1);
    lcd.print("2");
    digitalWrite(button2Led, HIGH);
    delay(600);
    digitalWrite(button2Led, LOW);
    B2Flag = 0;
  }
  if(BEFlag == 1){
    lcd.setCursor(4,1);
    lcd.print("E");
    BEFlag = 0;
  }

  //ENCODER HANDLER
  if(CWFlag == 1){  //if encoder is rotates clockwise
    if(speed < 100)
      speed = speed + 5;
    lcd.setCursor(11,1);
    lcd.print("   ");
    lcd.setCursor(11,1);
    lcd.print(speed);
    CWFlag = 0;  //reset flag for next time
  }
  if(CCWFlag == 1){
     if(speed > 5)
      speed = speed - 5;
    lcd.setCursor(11,1);
    lcd.print("   ");
    lcd.setCursor(11,1);
    lcd.print(speed);
    CCWFlag = 0;  //reset flag for next time
  }



  //WAIT FOR AND PROCESS SERIAL STRING COMMAND//
  if(Serial.available())    //while (Serial.available() == 0) {}            //wait for serial string data available
  {
    String inputSequence = Serial.readString();   //read until timeout
    inputSequence.trim();                         // remove any \r \n whitespace at the end of the String
    int spaceIndex = 0;
    while(inputSequence.length() > 0)            //process through sequence string of face moves
    {
      spaceIndex = inputSequence.indexOf(" ");
      String tempFirst = inputSequence.substring(0, spaceIndex);    //find space separation, then find command up to first space
      Serial.print("Processing " + tempFirst + ":  ");
      decodeAndRunMotor(tempFirst);                                 //run motors based on first command in string     

      lcd.setCursor(14,1);  //display current command in bottom right of screen
      lcd.print("  ");
      lcd.print(tempFirst);

      if(spaceIndex == -1)
        inputSequence = "";
      else
        inputSequence = inputSequence.substring(spaceIndex + 1, inputSequence.length());    //remove first command from string and repeat
    }
  }

}


//interrupt service routine for all 3 buttons (A1-A3)
//flips flag for corresponding button
ISR (PCINT1_vect)
{
  if(digitalRead(button1) == HIGH)
    B1Flag = 1;
  else if(digitalRead(button2) == HIGH)
    B2Flag = 1;
  else if(digitalRead(buttonE) == HIGH)
    BEFlag = 1;
}

//interrupt service routine for encoder (D10, EncA)
ISR (PCINT0_vect)  //called for any change in A, so verify rising, then see what B currently is
{
  if(digitalRead(EncA) == HIGH) //if A is rising
  {
    if(digitalRead(EncB) == HIGH) //if B has risen, must be CCW
      CCWFlag = 1;
    else                  //if B has fallen, must be CW
      CWFlag = 1;
  }
  /*  //old encoder
  //interrupt service routine for encoder (D9-D10)
  //flips direction flag based encoder inputs (previous and current state)
  //Position(Pos) STATES: 0,1,2,3
  int currentEncPos = encoderInputToState(digitalRead(EncA), digitalRead(EncB));
  if(currentEncPos == ((lastEncPos+1)%4)) //CW
    CWFlag = 1;
  else   //must be CCW
    CCWFlag = 1;
  lastEncPos = currentEncPos;
  */
}


//translates the 2 inputs for the encoder into a predefined state 
//STATE = AB: 0=00, 1=10, 2=11, 3=01
/*
int encoderInputToState(bool A, bool B)
{
  if(A == false){
    if(B == false)
      return 0;  //00
    else
      return 3;  //01
  }
  else{
    if(B == false)
      return 1;  //10
    else
      return 2;  //11
  }
}
* */

//input: U L F R B or D (or with ' variant like F')
//sends proper step and direction command to motor - rotates this motor 90 degrees
void decodeAndRunMotor(String faceChar)
{
  if(faceChar == "U'"){                     //can't case statement with string :(
    motor1.rotate(1);
    Serial.write("Motor U rotated counter-clockwise\n");
  }
  else if(faceChar == "U"){
    motor1.rotate(0);
    Serial.write("Motor U rotated clockwise\n");
  }
  else if(faceChar == "L'"){
    motor2.rotate(1);
    Serial.write("Motor L rotated counter-clockwise\n");
  }
  else if(faceChar == "L"){
    motor2.rotate(0);
    Serial.write("Motor L rotated clockwise\n");
  }
  else if(faceChar == "F'"){
    motor3.rotate(1);
    Serial.write("Motor F rotated counter-clockwise\n");
  }
  else if(faceChar == "F"){
    motor3.rotate(0);
    Serial.write("Motor F rotated clockwise\n");
  }
  else if(faceChar == "R'"){
    motor4.rotate(1);
    Serial.write("Motor R rotated counter-clockwise\n");
  }
  else if(faceChar == "R"){
    motor4.rotate(0);
    Serial.write("Motor R rotated clockwise\n");
  }
  else if(faceChar == "B'"){
    motor5.rotate(1);
    Serial.write("Motor B rotated counter-clockwise\n");
  }
  else if(faceChar == "B"){
    motor5.rotate(0);
    Serial.write("Motor B rotated clockwise\n");
  }
  else if(faceChar == "D'"){
    motor6.rotate(1);
    Serial.write("Motor D rotated counter-clockwise\n");
  }
  else if(faceChar == "D"){
    motor6.rotate(0);
    Serial.write("Motor D rotated clockwise\n");
  }
  else
    Serial.write("No command found\n");
}
