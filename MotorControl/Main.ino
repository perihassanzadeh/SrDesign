//U L F R B D U' L' F' R' B' D' U2 L2 F2 R2 B2 D2
//#include <Arduino.h>
#include "A4988.h"
#include "DFRobot_RGBLCD1602.h"
#include "EEPROMex.h"
#include <Adafruit_NeoPixel.h>

//MOTOR CONTROL//
//PHYSICAL HARDWIRED CONTROL//
#define DIR 2  //pin 4
#define STEP 3 //pin 5
#define MOTOR_STEPS 200  // Motor steps per revolution
#define a0 6   //pin 12  //enable in binary
#define a1 7   //pin 13
#define a2 8   //pin 14
//SPEED CONTROL//
#define MAXRPM 1200  // MAXIMUM RPM for cruise speed
#define MAXACCEL 16000
#define MAXDECEL 16000
int RPM = MAXRPM/2;  //  set RPM for cruise speed
int ACCEL = MAXACCEL/2;  // Acceleration and deceleration values are always in FULL steps / s^2
int DECEL = MAXDECEL/2;
int percentMaxSpeed = 50;
#define MICROSTEPS 2

A4988 motor0(MOTOR_STEPS, DIR, STEP); //a = 000    //global motor objects
A4988 motor1(MOTOR_STEPS, DIR, STEP); //a = 001
A4988 motor2(MOTOR_STEPS, DIR, STEP); //a = 010
A4988 motor3(MOTOR_STEPS, DIR, STEP); //a = 011
A4988 motor4(MOTOR_STEPS, DIR, STEP); //a = 100
A4988 motor5(MOTOR_STEPS, DIR, STEP); //a = 101

//for solid speed
//*
#define motor0Backlash 6
#define motor1Backlash 4
#define motor2Backlash 4
#define motor3Backlash 5
#define motor4Backlash 4
#define motor5Backlash 4
//*/

//for rubiks magnetic
/*
#define motor0Backlash 7
#define motor1Backlash 6
#define motor2Backlash 6
#define motor3Backlash 8
#define motor4Backlash 7
#define motor5Backlash 7  
*/

//LCD SCREEN//
DFRobot_RGBLCD1602 lcd(16, 2); //global lcd object
byte debug[8] = {0b10101,0b01110,0b11011,0b01110,0b10001,0b00000,0b00000,0b00000};
byte home[8] = {0b00100,0b01110,0b11111,0b11111,0b11011,0b11011,0b00000,0b00000};
byte shuffle[8] = {0b01000,0b11111,0b01000,0b00010,0b11111,0b00010,0b00000,0b00000};
byte scan[8] = {0b00000,0b11011,0b10001,0b00100,0b10001,0b11011,0b00000,0b00000};
byte solve[8] = {0b00010,0b00100,0b01110,0b00100,0b01000,0b00000,0b00000,0b00000};
byte leftArrow[8] = {0b00010,0b00100,0b01000,0b11111,0b01000,0b00100,0b00010,0b00000};
byte checkMark[8] = {0b00000,0b00001,0b00010,0b10100,0b01000,0b00000,0b00000,0b00000};

//BUTTONS//
#define button1 A3   //pin 26
#define button2 A2   //pin 25
volatile bool B1Flag = 0;  //Flags to be used by interrupt - goes high (1) when button is pushed
volatile bool B2Flag = 0;
volatile unsigned long lastPushTime1;  //based off millis() - can run up to 50 days
volatile unsigned long lastPushTime2;
#define button1Led A0  //pin 23
#define button2Led 5  //pin 11

//ENCODER BUTTON
#define buttonE A1   //pin 24
volatile bool BEFlag = 0;
volatile unsigned long lastPushTimeE;

//ENCODER
#define EncA 10  //pin 16
#define EncB 9   //pin 15
volatile bool CWFlag = 0;  //Clockwise flag  -  goes high when encoder rotated clockwise
volatile bool CCWFlag = 0;  //Counter-clockwise flag ...


//SYSTEM VARIABLES//
#define led 4  //onboard led  //pin 6
//FSM
enum STATES {Skip, Debug, Home, Shuffle, Scan, Presolve, Solve};
STATES state = Home; //start at home
STATES stateLoop;
//TIMERS
int Timer1AVal; //button1 led count value  //number of wave toggles - set to 2x num of square waves wanted,  -1 for infinite (stop with TIMSK1 |= (0 << OCIE1A);)
int Timer1BVal; //button2 led count value
//ENCODER
int lineSelected; //used for item selection in menu
//RANDOM SHUFFLE SEED
uint32_t oldSeed;
uint32_t seed;
//SCAN SEQUENCE RECIEVED
bool scanned = 0; //track if scanned yet, set to 0 since it hasn't scanned yet when powered up
String inputSequence; //String inputSequence = "";
uint8_t movePoint[100];
int numMoves = 0;
//AUTO-SOLVE or STEP-SOLVE
bool solveType = 0; //set to auto solve by default
int currentPosition = 0;  //keep track of current move for step-solve mode
//DEBUG
int debugMotorSelect = 0;  //for testing
//LED ring
Adafruit_NeoPixel pixels(12, 12, NEO_GRB + NEO_KHZ800); //12 leds on pin 12

unsigned long lastTime = 0;


void setup() {
  //START SERIAL PORT//
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  //LCD SCREEN INITIALIZATION//
  lcd.init();
  lcd.setRGB(100, 100, 100);
  lcd.customSymbol(0, debug);
  lcd.customSymbol(1, home);
  lcd.customSymbol(2, shuffle);
  lcd.customSymbol(3, scan);
  lcd.customSymbol(4, solve);
  lcd.customSymbol(5, leftArrow);
  lcd.customSymbol(6, checkMark);

  //MOTOR OUTPUT PIN DEFINITIONS//
  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(a0, OUTPUT);
  pinMode(a1, OUTPUT);
  pinMode(a2, OUTPUT);
  motor0.begin(RPM, MICROSTEPS);
  motor0.setSpeedProfile(motor0.LINEAR_SPEED, ACCEL, DECEL);
  motor1.begin(RPM, MICROSTEPS);
  motor1.setSpeedProfile(motor1.LINEAR_SPEED, ACCEL, DECEL);
  motor2.begin(RPM, MICROSTEPS);
  motor2.setSpeedProfile(motor2.LINEAR_SPEED, ACCEL, DECEL);
  motor3.begin(RPM, MICROSTEPS);
  motor3.setSpeedProfile(motor3.LINEAR_SPEED, ACCEL, DECEL);
  motor4.begin(RPM, MICROSTEPS);
  motor4.setSpeedProfile(motor4.LINEAR_SPEED, ACCEL, DECEL);
  motor5.begin(RPM, MICROSTEPS);
  motor5.setSpeedProfile(motor5.LINEAR_SPEED, ACCEL, DECEL);

  //BUTTON INPUT PIN DEFINTIONS AND INTERRUPTS// - (PIN CHANGE INTERRUPT)
  pinMode(button1, INPUT);  //using an external 4.7k pulldown resistor
  pinMode(button2, INPUT);
  pinMode(buttonE, INPUT);
  PCICR |= B00000010;  //Enable pin change interrupt on port C (A0-A5) (pins 23-28)
  PCMSK1 |= B00001110;  //Enable interrupts for pins A0-A2 (pins 24-26)

  //BUTTON LEDs
  pinMode(button1Led, OUTPUT);
  pinMode(button2Led, OUTPUT);
  //ONBOARD LED
  pinMode(led, OUTPUT);

  //ENCODER INPUT PIN DEFINTIONS, INTERRUPTS, AND POSITION CONFIG//
  pinMode(EncA, INPUT);  //using an external 10k pullup resistor
  pinMode(EncB, INPUT);
  PCICR |= B00000001;  //Enable pin change interrupt on port B (D8-D13) (pins 14-19)
  PCMSK0 |= B00000100;  //Enable interrupts for pin D10 (pins 16, EncA)


  //SYSTEM
  //Timer 1 for button1 and 2 blink led
  Timer1Config(0.9);  //config timer1 @ 0.9 Hz

  //init LED ring
  pixels.begin();

  //startup dance
  lcd.setCursor(2, 0);
  lcd.print("Rubik's Cube");
  lcd.setCursor(5, 1);
  lcd.print("Solver");

  startupShow();

  lcd.setRGB(100, 100, 100); //set to white for normal operation

  //start LED ring
  pixels.clear();
  for(int i=0; i<12; i++)  //12 pixels
    pixels.setPixelColor(i, pixels.Color(15, 15, 4));  //15 15 4
  pixels.show();
}


void loop() 
{
  unsigned long timePast = micros()-lastTime;
  Serial.println(timePast);
  Serial.println("Yes");
  lastTime = micros();

  //STATE TRANSITION - runs once like setup() but using flags
  switch(state)
  {
    case Debug://*******************************************************************************************//
      lcd.clear();
      lcd.setCursor(15, 0);
      lcd.write((unsigned char)0);  //debug symbol
    
      blinkStop(); //stop button blinking

      lcd.setCursor(0, 0);
      lcd.print("Time:");
      lcd.setCursor(10, 0);
      lcd.print("E:");
      lcd.print(EEPROM.readLong(0));
      lcd.setCursor(0, 1);
      lcd.print("Btn:"); 
      lcd.setCursor(7, 1);
      lcd.print("Spe:");
      lcd.print(percentMaxSpeed); 
      lcd.setCursor(15, 1);
      lcd.print(debugMotorSelect);
      stateLoop = state;  //begin state loop and reset transition flag
      state = Skip;
      break;
    case Home://*******************************************************************************************//
      lcd.clear();
      lcd.setCursor(15, 0);
      lcd.write((unsigned char)1);  //home symbol

      if(scanned){
        lcd.setCursor(14, 1);
        lcd.write((unsigned char)6); //check mark
        lcd.write((unsigned char)3);  //display scan symbol if scan has been completed
      }

      blinkStop(); //stop button blinking

      lcd.setCursor(0, 0);
      lcd.write((unsigned char)2);  //shuffle
      lcd.print("Shuffle ");
      lcd.write((unsigned char)5);  //left arrow
      lcd.print("-");
      lcd.setCursor(0, 1);
      if(scanned){ //display solve if already scanned
        lcd.write((unsigned char)4);
        lcd.print("Solve");
      }
      else{ //display scan if not yet scanned
        lcd.write((unsigned char)3);
        lcd.print("Scan");
      }

      //variable lcd output handled below
      lineSelected = 0;
      
      stateLoop = state;
      state = Skip;
      break;
    case Shuffle://*******************************************************************************************//
      lcd.clear();
      lcd.setCursor(15, 0);
      lcd.write((unsigned char)2);  //shuffle symbol

      blinkStop(); //stop button blinking
      blinkRed(-1);  //blink red indefinitely
      
      oldSeed = EEPROM.readLong(0); //retrieve old seed from address 0
      seed = oldSeed + 1;
      EEPROM.updateLong(0, seed);  //write (update) incemented seed back into address 0 (store seed to be used) 
      lcd.setCursor(0, 0);
      lcd.print("Seed:");
      
      randomSeed(seed); 
      lcd.print(random(0,2147483647), HEX);     //seed representation
      
      lcd.setCursor(3, 1);
      lcd.print("Push to start");
      
      stateLoop = state;
      state = Skip;
      break;
    case Scan://*******************************************************************************************//
      lcd.clear();
      lcd.setCursor(15, 0);
      lcd.write((unsigned char)3);  //scan symbol

      blinkStop(); //stop button blinking
      blinkRed(-1);

      lcd.setCursor(0, 0);
      lcd.print("Scan");

      lcd.setCursor(3, 1);
      lcd.print("Push to start");

      stateLoop = state;
      state = Skip;
      break;
    case Presolve://*******************************************************************************************//
      lcd.clear();
      lcd.setCursor(15, 0);
      lcd.write((unsigned char)4);  //solve symbol

      blinkStop(); //stop button blinking

      //autosolve or stepsolve
      lcd.setCursor(0, 0);
      lcd.print("Auto-Solve ");
      lcd.write((unsigned char)5);  //left arrow
      lcd.print("-");

      lcd.setCursor(0, 1);
      lcd.print("Step-Solve");

      lineSelected = 0; //select autosolve as default
      solveType = 0; 

      stateLoop = state;
      state = Skip;
      break;
    case Solve://*******************************************************************************************//
      lcd.clear();
      lcd.setCursor(15, 0);
      lcd.write((unsigned char)4);  //solve symbol

      blinkStop(); //stop button blinking

      if(solveType){ //if step-solve
        lcd.setCursor(0, 0);
        lcd.print("Step-Solve");
        lcd.setCursor(0, 1);
        lcd.print("Step: ");
        lcd.print(inputSequence.substring(movePoint[0],movePoint[1]-1));  //print string of first move

        lcd.setCursor(10, 1);
        lcd.print("1/");
        lcd.print(numMoves);
        lcd.print("  ");

        currentPosition = 0;  //start at step 0
        percentMaxSpeed = 50;    //set step solve to 50% speed always
        setMotorSpeeds(percentMaxSpeed);
      }
      else{ //if auto-solve
        blinkRed(-1);

        lcd.setCursor(0, 0);
        lcd.print("Speed:");
        lcd.print(percentMaxSpeed); 
        lcd.print("% ");

        lcd.setCursor(3, 1);
        lcd.print("Push to start");
      }


      stateLoop = state;
      state = Skip;
      break;
    default://*******************************************************************************************//
      //DO NOTHING if not transitioning (when state == Skip, set after passes through once)
      break;
  }

  //STATE LOGIC/OUTPUT - like loop() //**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//**//
  switch(stateLoop)
  {
    case Debug://**/////////////////////////////////////////////////////////////////////////////////////////**
      lcd.setCursor(5, 0);  //for test debugging - display seconds in bottom left of screen
      lcd.print(millis()/1000); //print seconds since startup

      //EXIT DEBUG (don't use home button)
      if(CCWFlag && digitalRead(button1) && digitalRead(button2)){    //home button cycles through selected motor
        state = Home;                                                 //forward button cycles through selected speed
        CCWFlag = 0;                                                  //encoder rotates motor CW or CCW
      }

      //ENCODER HANDLERS
      if(CWFlag){  //if encoder is rotates clockwise
        rotateMotor90(debugMotorSelect, 0); //CW    -just for testing
        CWFlag = 0;  //reset flag for next time
      }
      if(CCWFlag){
        rotateMotor90(debugMotorSelect, 1);  //CCW
        CCWFlag = 0;  //reset flag for next time
      }

      //PUSH BUTTON HANDLERS
      if(B1Flag && Timer1AVal == 0){ //if button is pushed and timer is ready to output wave (avoids a rare led always on state)
        lcd.setCursor(4,1);
        lcd.print("1");
        blinkYellow(2);
        debugMotorSelect = (debugMotorSelect+1)%6;
        lcd.setCursor(15, 1);
        lcd.print(debugMotorSelect);
        B1Flag = 0;
      }
      if(B2Flag && Timer1BVal == 0){
        lcd.setCursor(4,1);
        lcd.print("2");
        blinkRed(2);
        percentMaxSpeed = (percentMaxSpeed%100)+5;
        setMotorSpeeds(percentMaxSpeed);
        lcd.setCursor(11,1);
        lcd.print(percentMaxSpeed);
        if(percentMaxSpeed != 100)
          lcd.print("  ");  //might be shorter number
        B2Flag = 0;
      }
      if(BEFlag){
        lcd.setCursor(4,1);
        lcd.print("E");
        BEFlag = 0;
      }

      break;
    case Home://**/////////////////////////////////////////////////////////////////////////////////////////**

      if(CCWFlag && digitalRead(button1) && digitalRead(button2)){
        state = Debug;
        CCWFlag = 0;
      }
      if(CCWFlag)
      {
        lineSelected = 0;
        lcd.setCursor(9, 0);
        lcd.write((unsigned char)5);  //left arrow
        lcd.print("-");
        lcd.setCursor(9, 1);
        lcd.print("  ");
        CCWFlag = 0;
      }
      if(CWFlag)
      {
        lineSelected = 1;
        lcd.setCursor(9, 0);
        lcd.print("  ");
        lcd.setCursor(9, 1);
        lcd.write((unsigned char)5);  //left arrow
        lcd.print("-");
        CWFlag = 0;
      }

      //PUSH BUTTON HANDLERS
      if(B1Flag)
        B1Flag = 0;  //must handle flags so they aren't processed in next state
      if(B2Flag)
        B2Flag = 0;

      if(BEFlag){
        if(scanned){ //if already scanned, is displaying solve and should transition to solve
          if(lineSelected == 0) //first line = shuffle
            state = Shuffle;
          else
            state = Presolve;
        }
        else{ //hasnt been scanned and should transition to scan
          if(lineSelected == 0) //first line = shuffle
            state = Shuffle;
          else
            state = Scan;
        }
        BEFlag = 0;
      }
      
      break;
    case Shuffle://**/////////////////////////////////////////////////////////////////////////////////////////**

      if(CWFlag)
        CWFlag = 0;
      if(CCWFlag)
        CCWFlag = 0;

      if(B1Flag){ //transition home
        state = Home;
        B1Flag = 0;
      }
    
      if(B2Flag){ //button to start shuffling
        blinkStop(); //stop button blinking
        digitalWrite(button2Led, HIGH); //turn button solid

        setMotorSpeeds(50);
        
        //generate 22 random moves
        for(int i = 0; i < 26; i++){
          int num = random(0,12); //0,1,2,3,4,5,6,7,8,9,10,11 (8.33%) (CW & CCW for each of 6 faces)

          lcd.setCursor(0, 1); //display current shuffle move to screen
          lcd.print("Motor ");
          lcd.print(num/2);
          lcd.print(" ");
          if(num%2)
            lcd.print("CW      ");
          else
            lcd.print("CCW     ");

          rotateMotor90(num/2, num%2);  //uses core motor rotate fcn //0,1,2,3,4,5  (16.67%)  ,   //0,1 (50%) //0=CW, 1=CCW
          CWFlag = 0;
          while(!CWFlag){                //wait until encoder is turned CW
            if(B1Flag){ //transition home
              state = Home;               //home button will break out of this
              B1Flag = 0;
              break;
            }
          }
          if(state == Home)  //continue to break out if home button pushed
            break;
        }

        scanned = 0; //must rescan if shuffled
        inputSequence = "";  //memset(inputSequence, "", sizeof(inputSequence));
        numMoves = 0;  //memset(moves, "", sizeof(moves));   //delete [] moves; //clear moves
        memset(movePoint, NULL, sizeof(movePoint));
        state = Home;
        B2Flag = 0;
      }

      if(BEFlag)
        BEFlag = 0;
      
      break;
    case Scan://**/////////////////////////////////////////////////////////////////////////////////////////**
      
      if(CWFlag)
        CWFlag = 0;
      if(CCWFlag)
        CCWFlag = 0;

      if(B1Flag){ //transition home
        state = Home;
        B1Flag = 0;
      }

      
      if(B2Flag){ //button to start scan
        blinkStop(); //stop button blinking
        digitalWrite(button2Led, HIGH); //turn button solid

        Serial.flush(); //clear buffer

        Serial.println("1"); //send serial command to begin scan

        lcd.setCursor(0, 0);
        lcd.print("Starting scan   ");
        lcd.setCursor(0, 1);
        lcd.print("                ");

        lcd.setCursor(0, 1);
        for(int i = 0; i < 16; i++){  //print loading bar
          lcd.print(">");
          delay(100);
        }

        //WAIT FOR SERIAL STRING COMMAND//
        while (Serial.available() == 0) {  //wait (loop) for serial string data available
          if(B1Flag){  //if home button pushed while waiting - transition home
            state = Home;
            B1Flag = 0;
            break;
          }
        }

        if(state != Home){ //if home button wasn't pushed to exit loop - read in scan
          inputSequence = Serial.readString();
          inputSequence.trim();

          numMoves=1;  //first move
          movePoint[0] = 0;  //always begins with move
          for(int i=0; i<inputSequence.length(); i++){  //process number of moves
            if(inputSequence[i] == ' '){
              movePoint[numMoves] = i+1;                  //movePoint[] = points to index of first char of ith move in inputSequence
              Serial.print(movePoint[numMoves]);
              Serial.print(" ");
              numMoves++;                               //numMoves = number of moves in inputSequence
            }
          }
          Serial.println(numMoves); 
          scanned = 1;
          state = Home;    
        }        

        B2Flag = 0;
      }
      
/*
      if(B2Flag){ //button to start scan
        B2Flag = 0;
        blinkStop(); //stop button blinking
        digitalWrite(button2Led, HIGH); //turn button solid

        Serial.println("1"); //send serial command to begin scan

        lcd.setCursor(0, 0);
        lcd.print("Starting scan   ");
        lcd.setCursor(0, 1);
        lcd.print("                ");

        while (Serial.available() == 0) {  //wait (loop) for serial string data available
          if(B1Flag){  //if home button pushed while waiting - transition home
            state = Home;
            B1Flag = 0;
            break;
          }
        } 

        String inputChar = "";
        inputChar = Serial.readString();   //wait here for "2"
        inputChar.trim(); 
        if(inputChar == "2"){
          
          rotateMotor("2D");
          rotateMotor("2L");
          rotateMotor("2U");
          rotateMotor("R");
          rotateMotor("L'");
          rotateMotor("2U");
          rotateMotor("2R");
          rotateMotor("2L");
          rotateMotor("2U");
          rotateMotor("R");
          rotateMotor("L'");
          rotateMotor("2D");
          
          Serial.println("3");

          while (Serial.available() == 0) {  //wait (loop) for serial string data available
            if(B1Flag){  //if home button pushed while waiting - transition home
              state = Home;
              B1Flag = 0;
              break;
            }
          } 

          inputChar = "";
          inputChar = Serial.readString();   //wait here for "4"
          inputChar.trim(); 
          if(inputChar == "4"){
            
            rotateMotor("2D");
            rotateMotor("L");
            rotateMotor("R'");
            rotateMotor("2U");
            rotateMotor("2L");
            rotateMotor("2R");
            rotateMotor("2U");
            rotateMotor("L");
            rotateMotor("R'");
            rotateMotor("2U");
            rotateMotor("2B");
            rotateMotor("2R");
            rotateMotor("2L");
            rotateMotor("2B");
            rotateMotor("2R");
            rotateMotor("2L");
            rotateMotor("2B");
            rotateMotor("2F");
            
            Serial.println("5");

            while (Serial.available() == 0) {  //wait (loop) for serial string data available
              if(B1Flag){  //if home button pushed while waiting - transition home
                state = Home;
                B1Flag = 0;
                break;
              }
            } 

            inputChar = "";
            inputChar = Serial.readString();   //wait here for "6"
            inputChar.trim(); 
            if(inputChar == "6"){
              
              rotateMotor("2F");
              rotateMotor("2B");
              rotateMotor("2L");
              rotateMotor("2R");
              rotateMotor("2B");
              rotateMotor("2L");
              rotateMotor("2R");
              rotateMotor("2B");
              rotateMotor("2L");
              rotateMotor("2R");
              
              Serial.println("7");

              while (Serial.available() == 0) {  //wait (loop) for serial string data available
                if(B1Flag){  //if home button pushed while waiting - transition home
                  state = Home;
                  B1Flag = 0;
                  break;
                }
              } 

              inputSequence = "";   //memset(inputSequence, "", sizeof(inputSequence));
              inputSequence = Serial.readString();   //read until timeout
              inputSequence.trim(); 
              splitInputString(inputSequence);

              scanned = 1;
              state = Home;

            }
            else
              break;

          }
          else
            break;

        }
        else
          break;

      }
*/
      if(BEFlag)
        BEFlag = 0;

      break;
    case Presolve://**/////////////////////////////////////////////////////////////////////////////////////////**
    
      if(CCWFlag)
      {
        lineSelected = 0;
        lcd.setCursor(11, 0);
        lcd.write((unsigned char)5);  //left arrow
        lcd.print("-");
        lcd.setCursor(11, 1);
        lcd.print("  ");
        CCWFlag = 0;
      }
      if(CWFlag)
      {
        lineSelected = 1;
        lcd.setCursor(11, 0);
        lcd.print("  ");
        lcd.setCursor(11, 1);
        lcd.write((unsigned char)5);  //left arrow
        lcd.print("-");
        CWFlag = 0;
      }

      if(B1Flag){ //transition home
        state = Home;
        B1Flag = 0;
      }

      if(B2Flag)
        B2Flag = 0;
      
      if(BEFlag){
        if(lineSelected == 0) //first line = autosolve (solveType=0)
          solveType = 1;   //make this 0 to re-enable auto solve
        else
          solveType = 1;
        
        state = Solve;
        BEFlag = 0;
      }

      break;
    case Solve://**/////////////////////////////////////////////////////////////////////////////////////////**

      if(solveType){ //if step-solve
        if(CWFlag){  //if encoder rotates clockwise - go to next move 
          if(currentPosition < numMoves){       //if theres a next step 
            lcd.setCursor(6, 1);
            lcd.print(inputSequence.substring(movePoint[currentPosition],movePoint[currentPosition+1]-1));
            lcd.print(" ");
            lcd.setCursor(10, 1);
            lcd.print(currentPosition+1);           //display current position in solve sequence: 0/6
            lcd.print("/");
            lcd.print(numMoves);
            lcd.print("  ");
            rotateMotor(inputSequence.substring(movePoint[currentPosition],movePoint[currentPosition+1]-1));   //rotate motor with next move
            currentPosition++;                     //increment currentPosition
          }
          
          if(currentPosition == numMoves)  //if at end of sequence, indicate to go home
            blinkYellow(-1);
          
          CWFlag = 0;  //reset flag for next time
        }

        if(CCWFlag){ //if encoder rotates counter-clockwise - go back to last move
          if(currentPosition > 0){       //if theres a previous step
            lcd.setCursor(6, 1);
            lcd.print(inputSequence.substring(movePoint[currentPosition-1],movePoint[currentPosition]-1));
            lcd.print(" ");
            lcd.setCursor(10, 1);
            lcd.print(currentPosition);           //display current position in solve sequence: 0/6
            lcd.print("/");
            lcd.print(numMoves);
            lcd.print("  ");
            reverseRotateMotor(inputSequence.substring(movePoint[currentPosition-1],movePoint[currentPosition]-1));   //rotate motor opposite of last move
            currentPosition--;                     //decrement currentPosition
          }
          
          CCWFlag = 0;  //reset flag for next time
        }

        if(B1Flag){ //home button goes home and clears all scan variables
          scanned = 0;  //scan not relevant if moved, once go home
          inputSequence = "";   //memset(inputSequence, "", sizeof(inputSequence)); //clear input string and move array
          numMoves = 0;   //memset(moves, "", sizeof(moves));  //delete [] moves;  //clear moves[]
          memset(movePoint, NULL, sizeof(movePoint));
          state = Home;
          B1Flag = 0;
        }

        if(B2Flag) //button doesn't do anything
          B2Flag = 0;

      }

      else{  //if auto-solve
      /*
        //ENCODER HANDLERS
        if(CWFlag){  //if encoder is rotates clockwise
          if(percentMaxSpeed < 100)
            percentMaxSpeed = percentMaxSpeed + 5;  //increase speed
          setMotorSpeeds(percentMaxSpeed);
          lcd.setCursor(6,0);
          lcd.print(percentMaxSpeed);
          lcd.print("% ");
          CWFlag = 0;  //reset flag for next time
        }
        if(CCWFlag){
          if(percentMaxSpeed > 5)
            percentMaxSpeed = percentMaxSpeed - 5;  //decrease speed
          setMotorSpeeds(percentMaxSpeed);
          lcd.setCursor(6,0);
          lcd.print(percentMaxSpeed);
          lcd.print("% ");
          CCWFlag = 0;  //reset flag for next time
        }

        if(B2Flag){ //button to start solve, run motor sequence
          blinkStop(); //stop button blinking
          digitalWrite(button2Led, HIGH); //turn button solid

          lcd.setCursor(0,1);  //clear bottom of screen
          lcd.print("                ");

          unsigned long startTime = millis();

          for(int i=0; i<numMoves; i++){
            lcd.setCursor(0,1);  //display current command in bottom right of screen
            lcd.print("Move: ");
            lcd.print(inputSequence.substring(movePoint[i],movePoint[i+1]-1));
            lcd.print(" ");
            rotateMotor(inputSequence.substring(movePoint[i],movePoint[i+1]-1));  //rotate motor
          }
          
          unsigned long duration = (millis() - startTime);

          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("Cube solved");
          lcd.setCursor(0,1);
          lcd.print("in ");
          lcd.print(duration/1000);
          lcd.print(".");
          lcd.print((duration%1000)/100);
          lcd.print(" sec!");
          
          blinkStop();
          blinkYellow(-1);
          while(!B1Flag){}; //wait until home button is pressed

          scanned = 0;  //scan not relevant if cube moved/solved
          inputSequence = "";     //memset(inputSequence, "", sizeof(inputSequence));  //clear input string and move array
          numMoves = 0;  //memset(moves, "", sizeof(moves));  //delete [] moves;
          memset(movePoint, NULL, sizeof(movePoint));
          state = Home;  //return home after solve
          B2Flag = 0;
        }

        if(B1Flag){ //home button goes home
        state = Home;
        B1Flag = 0;
        } 
        */
      }
      

      if(BEFlag) //for both auto-solve and step-solve, encoder push doesn't do anything
        BEFlag = 0;

      break;
    default://**/////////////////////////////////////////////////////////////////////////////////////////**
      state = Home; //go home if messed up
      break;
  }

}


//interrupt service routine for all 3 buttons (A1-A3)
//flips flag for corresponding button
ISR (PCINT1_vect)
{
    if(digitalRead(button1) == HIGH && (millis()-lastPushTime1)>1000) //if button pushed and hasn't been pushed in a while (debounce)
    {
      B1Flag = 1;
      lastPushTime1 = millis();
    }
    if(digitalRead(button2) == HIGH && (millis()-lastPushTime2)>1000)
    {
      B2Flag = 1;
      lastPushTime2 = millis();
    }
    if(digitalRead(buttonE) == HIGH && millis()-lastPushTimeE>1000)
    {
      BEFlag = 1;
      lastPushTimeE = millis();
    }
}

//interrupt service routine for encoder (D10, EncA)
//called for any change in A, so verify rising, then see what B currently is
ISR (PCINT0_vect)
{
  if(digitalRead(EncA) == HIGH) //if A is rising //if encoder was rotated
  {
    if(digitalRead(EncB) == HIGH) //if B has risen, must be CCW
      CCWFlag = 1;
    else                  //if B has fallen, must be CW
      CWFlag = 1;
  }
}

//interrupt service routine for timer 1 - toggles output state every 1/2 wavelength - results in a 50% square wave at prespecified frequency
ISR(TIMER1_COMPA_vect){//timer1 interrupt toggles LED
  if(Timer1AVal != 0 || Timer1BVal != 0) //if A or B still have count down val left
    if(Timer1AVal != 0)
      digitalWrite(A0,!digitalRead(A0)); //A for button 1 //if negative toggle infintely, if positive count down
    if(Timer1BVal != 0)
      digitalWrite(5,!digitalRead(5)); //B for button 2 
  else //timer is enabled but both counts are 0, must've just ended timer
    TIMSK1 |= (0 << OCIE1A); //then turn off timer 1

  if(Timer1AVal > 0)
    Timer1AVal -= 1;
  if(Timer1BVal > 0)
    Timer1BVal -= 1;
}

//configure Timer1 frequency which runs leds, changes speed at which leds blink when enabled 
void Timer1Config(double frequency)
{
  cli(); //stop interrupts while changes are made
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  OCR1A = 15625/(2*frequency) - 1;  //(must be <65536)  //count up value = clock frequency / half wave freq(toggle freq) * (prescalar,1024)
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS12) | (1 << CS10);  // Set CS12 and CS10 bits for 1024 prescaler
  sei();  //start back up interrupts
}

//stop both red and yellow blinking, turns off both leds
void blinkStop()
{
  Timer1AVal = 0;  //empty count downs
  Timer1BVal = 0;
  TIMSK1 |= (0 << OCIE1A); //stop timer
  digitalWrite(button1Led, LOW); //ensure both LEDs off
  digitalWrite(button2Led, LOW);
}

//if amount is -1 = forever, else amount dictates num of halfwaves (set amount to 2x squarewaves)
void blinkYellow(int amount)
{
  Timer1AVal = amount;  //set counter
  TIMSK1 |= (1 << OCIE1A);  //turn on timer
}

//if amount is -1 = forever, else amount dictates num of halfwaves (set amount to 2x squarewaves)
void blinkRed(int amount)
{
  Timer1BVal = amount;  //set counter
  TIMSK1 |= (1 << OCIE1A);  //turn on timer
}

//display lcd screen colors and flash buttons, short startup sequence
void startupShow(){
  blinkYellow(-1);
  blinkRed(-1);
  for(int i=0; i<256; i++){     //nothing to white   end 255,255,255
      lcd.setRGB(i, i, i);
      for(int j=0; j<12; j++)  //12 pixels
        pixels.setPixelColor(j, pixels.Color(i, i, i));
      pixels.show();
  }
  delay(20);
  for(int i=0; i<256; i++){     //white to red    end 255,0,0
      lcd.setRGB(255, 255-i, 255-i);
      for(int j=0; j<12; j++)  //12 pixels
        pixels.setPixelColor(j, pixels.Color(255, 255-i, 255-i));
      pixels.show();
  }
  delay(20);
  for(int i=0; i<256; i++){     //red to blue    end 0,0,255
      lcd.setRGB(255-i, 0, i);
      for(int j=0; j<12; j++)  //12 pixels
        pixels.setPixelColor(j, pixels.Color(255-i, 0, i));
      pixels.show();
  }
  delay(20);
  for(int i=0; i<256; i++){     //blue to orange    end 255,127,0
      lcd.setRGB(i, i/2, 255-i);
      for(int j=0; j<12; j++)  //12 pixels
        pixels.setPixelColor(j, pixels.Color(i, i/2, 255-i));
      pixels.show();
  }
  delay(20);
  for(int i=0; i<256; i++){     //orange to green    end 0,255,0
      lcd.setRGB(255-i, 128+(i/2), 0);
      for(int j=0; j<12; j++)  //12 pixels
        pixels.setPixelColor(j, pixels.Color(255-i, 128+(i/2), 0));
      pixels.show();
  }
  delay(20);
  for(int i=0; i<256; i++){     //green to yellow    end 255,255,0
      lcd.setRGB(i, 255, 0);
      for(int j=0; j<12; j++)  //12 pixels
        pixels.setPixelColor(j, pixels.Color(i, 255, 0));
      pixels.show();
  }
  delay(40);
  blinkStop();
}

/*
//pass String of large serial input string ("U L F R B D U' L' F' R' B' D'")
//stores split String array in moves[] and length in movesLength
void splitInputString(String input)
{
  //previous trim command ensures there is no extraneous white spaces
  input.trim();

  int numSpaces = 0;
  for(int i=0; i<input.length(); i++){  //count number of spaces in input string
    if(input[i] == ' '){
      numSpaces++;
    }
  }

  movesLength = ++numSpaces;  //number of elements in string will be 1 more than number of spaces
  //moves = new String [movesLength];
  
  int spaceIndex = 0;
  for(int i=0; i<movesLength; i++)
  {
    spaceIndex = input.indexOf(" ");  //find index of first space
    if(spaceIndex < 0) //if can't find index, must be out of spaces
      moves[i] = input;
    else
    {
      moves[i] = input.substring(0, spaceIndex); //store next move in sequence
      input = input.substring(spaceIndex+1);   //cut off first move
    }
  }
  
}
*/

//sets RPM, ACCEL, and DECEL to a percemtage of MAXRPM, MAXACCEL, MAXDECEL
//sets for all motors
void setMotorSpeeds(int percentage){
  percentMaxSpeed = percentage;
  RPM = ((double)percentMaxSpeed)/100 * MAXRPM;
  ACCEL = ((double)percentMaxSpeed)/100 * MAXACCEL;
  DECEL = ((double)percentMaxSpeed)/100 * MAXDECEL;
  motor0.setRPM(RPM);
  motor0.setSpeedProfile(motor0.LINEAR_SPEED, ACCEL, DECEL);
  motor1.setRPM(RPM);
  motor1.setSpeedProfile(motor1.LINEAR_SPEED, ACCEL, DECEL);
  motor2.setRPM(RPM);
  motor2.setSpeedProfile(motor2.LINEAR_SPEED, ACCEL, DECEL);
  motor3.setRPM(RPM);
  motor3.setSpeedProfile(motor3.LINEAR_SPEED, ACCEL, DECEL);
  motor4.setRPM(RPM);
  motor4.setSpeedProfile(motor4.LINEAR_SPEED, ACCEL, DECEL);
  motor5.setRPM(RPM);
  motor5.setSpeedProfile(motor5.LINEAR_SPEED, ACCEL, DECEL);
}

//input: U L F R B D U' L' F' R' B' D' 2U 2L 2F 2R 2B 2D U2 L2 F2 R2 B2 D2
//sends proper step and direction command to motor - rotates this motor                         //*********DRIVER TO MOTOR ASSIGNMENTS*******//
void rotateMotor(String faceChar)
{
  if(faceChar == "L'")                     //can't case statement with string :(
    rotateMotor90(0, 1);  //rotate motor 0 CCW
  else if(faceChar == "L")
    rotateMotor90(0, 0);
  else if(faceChar == "L2" || faceChar == "2L")
    rotateMotor180(0);
  else if(faceChar == "U'")
    rotateMotor90(1, 1);
  else if(faceChar == "U")
    rotateMotor90(1, 0);
  else if(faceChar == "U2" || faceChar == "2U")
    rotateMotor180(1);
  else if(faceChar == "B'")
    rotateMotor90(2, 1);
  else if(faceChar == "B")
    rotateMotor90(2, 0);
  else if(faceChar == "B2" || faceChar == "2B")
    rotateMotor180(2);
  else if(faceChar == "D'")
    rotateMotor90(3, 1);
  else if(faceChar == "D")
    rotateMotor90(3, 0);
  else if(faceChar == "D2" || faceChar == "2D")
    rotateMotor180(3);
  else if(faceChar == "F'")
    rotateMotor90(4, 1);
  else if(faceChar == "F")
    rotateMotor90(4, 0);
  else if(faceChar == "F2" || faceChar == "2F")
    rotateMotor180(4);
  else if(faceChar == "R'")
    rotateMotor90(5, 1);
  else if(faceChar == "R")
    rotateMotor90(5, 0);
  else if(faceChar == "R2" || faceChar == "2R")
    rotateMotor180(5);
}

//input: input: U L F R B D U' L' F' R' B' D' 2U 2L 2F 2R 2B 2D U2 L2 F2 R2 B2 D2
//sends reverse direction with proper step, 180 degree rotations are always CW though
//uses same driver to motor assignments from rotateMotor(String faceChar), no need to edit here
void reverseRotateMotor(String faceChar)
{
  if(faceChar == "U'")                     //can't case statement with string :(
    rotateMotor("U");             //simply flip direction, don't call directly so no need to change assigment it driver assignment changes
  else if(faceChar == "U")
    rotateMotor("U'");
  else if(faceChar == "L'")
    rotateMotor("L");
  else if(faceChar == "L")
    rotateMotor("L'");
  else if(faceChar == "F'")
    rotateMotor("F");
  else if(faceChar == "F")
    rotateMotor("F'");
  else if(faceChar == "R'")
    rotateMotor("R");
  else if(faceChar == "R")
    rotateMotor("R'");
  else if(faceChar == "B'")
    rotateMotor("B");
  else if(faceChar == "B")
    rotateMotor("B'");
  else if(faceChar == "D'")
    rotateMotor("D");
  else if(faceChar == "D")
    rotateMotor("D'");
  else
    rotateMotor(faceChar);  //if anything else, must be double rotation, so can just call normal rotation
}

//base function to rotate motors given motor number and direction
//rotate a motor 90 degrees, given the motor number(0-5) and direction(0=CW,1=CCW)
void rotateMotor90(int numMotor, bool direction)
{
  switch(numMotor)
  {
    case 0:
      digitalWrite(a0, 0);
      digitalWrite(a1, 0);
      digitalWrite(a2, 0);
      if(direction){
        motor0.rotate(-90 - motor0Backlash);  //backlash compensation
        motor0.rotate(motor0Backlash);
      }
      else{
        motor0.rotate(90 + motor0Backlash);
        motor0.rotate(-motor0Backlash);
      }
      break;
    case 1:
      digitalWrite(a0, 1);
      digitalWrite(a1, 0);
      digitalWrite(a2, 0);
      if(direction){
        motor1.rotate(-90 - motor1Backlash);
        motor1.rotate(motor1Backlash);
      }
      else{
        motor1.rotate(90 + motor1Backlash);
        motor1.rotate(-motor1Backlash);
      }
      break;
    case 2:
      digitalWrite(a0, 0);
      digitalWrite(a1, 1);
      digitalWrite(a2, 0);
      if(direction){
        motor2.rotate(-90 - motor2Backlash);
        motor2.rotate(motor2Backlash);
      }
      else{
        motor2.rotate(90 + motor2Backlash);
        motor2.rotate(-motor2Backlash);
      }
      break;
    case 3:
      digitalWrite(a0, 1);
      digitalWrite(a1, 1);
      digitalWrite(a2, 0);
      if(direction){
        motor3.rotate(-90 - motor3Backlash);
        motor3.rotate(motor3Backlash);
      }
      else{
        motor3.rotate(90 + motor3Backlash);
        motor3.rotate(-motor3Backlash);
      }
      break;
    case 4:
      digitalWrite(a0, 0);
      digitalWrite(a1, 0);
      digitalWrite(a2, 1);
      if(direction){
        motor4.rotate(-90 - motor4Backlash);
        motor4.rotate(motor4Backlash);
      }
      else{
        motor4.rotate(90 + motor4Backlash);
        motor4.rotate(-motor4Backlash);
      }
      break;
    case 5:
      digitalWrite(a0, 1);
      digitalWrite(a1, 0);
      digitalWrite(a2, 1);
      if(direction){
        motor5.rotate(-90 - motor5Backlash);
        motor5.rotate(motor5Backlash);
      }
      else{
        motor5.rotate(90 + motor5Backlash);
        motor5.rotate(-motor5Backlash);
      }
      break;
  }
}

void rotateMotor180(int numMotor)  //direction doesn't matter for 180
{
  switch(numMotor)
  {
    case 0:
      digitalWrite(a0, 0);
      digitalWrite(a1, 0);
      digitalWrite(a2, 0);
      motor0.rotate(180 + motor0Backlash);  //backlash compensation
      motor0.rotate(-motor0Backlash);
      break;
    case 1:
      digitalWrite(a0, 1);
      digitalWrite(a1, 0);
      digitalWrite(a2, 0);
      motor1.rotate(180 + motor1Backlash);
      motor1.rotate(-motor1Backlash);
      break;
    case 2:
      digitalWrite(a0, 0);
      digitalWrite(a1, 1);
      digitalWrite(a2, 0);
      motor2.rotate(180 + motor2Backlash);
      motor2.rotate(-motor2Backlash);
      break;
    case 3:
      digitalWrite(a0, 1);
      digitalWrite(a1, 1);
      digitalWrite(a2, 0);
      motor3.rotate(180 + motor3Backlash);
      motor3.rotate(-motor3Backlash);
      break;
    case 4:
      digitalWrite(a0, 0);
      digitalWrite(a1, 0);
      digitalWrite(a2, 1);
      motor4.rotate(180 + motor4Backlash);
      motor4.rotate(-motor4Backlash);
      break;
    case 5:
      digitalWrite(a0, 1);
      digitalWrite(a1, 0);
      digitalWrite(a2, 1);
      motor5.rotate(180 + motor5Backlash);
      motor5.rotate(-motor5Backlash);
      break;
  }
}

