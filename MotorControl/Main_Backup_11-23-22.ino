//U L F R B D U' L' F' R' B' D'
#include "Motor.h"
#include "DFRobot_RGBLCD1602.h"
#include "EEPROMex.h"

//MOTOR CONTROL//
#define dirPin 2  //pin 4
#define stepPin 3 //pin 5
#define a0Pin 6   //pin 12
#define a1Pin 7   //pin 13
#define a2Pin 8   //pin 14

Motor motor1 = Motor(0, 0, 0, 50, 90);  //global motor objects
Motor motor2 = Motor(0, 0, 1, 50, 90);
Motor motor3 = Motor(0, 1, 0, 50, 90);
Motor motor4 = Motor(0, 1, 1, 50, 90);
Motor motor5 = Motor(1, 0, 0, 50, 90);
Motor motor6 = Motor(1, 0, 1, 50, 90);

//LCD SCREEN//
DFRobot_RGBLCD1602 lcd(16, 2); //global lcd object
byte debug[8] = {
    0b10101,
    0b01110,
    0b11011,
    0b01110,
    0b10001,
    0b00000,
    0b00000,
    0b00000
    };
byte home[8] = {
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b11011,
    0b11011,
    0b00000,
    0b00000
    };
byte shuffle[8] = {
    0b01000,
    0b11111,
    0b01000,
    0b00010,
    0b11111,
    0b00010,
    0b00000,
    0b00000
    };
byte scan[8] = {
    0b00000,
    0b11011,
    0b10001,
    0b00100,
    0b10001,
    0b11011,
    0b00000,
    0b00000
    };
byte solve[8] = {
    0b00010,
    0b00100,
    0b01110,
    0b00100,
    0b01000,
    0b00000,
    0b00000,
    0b00000
    };
byte leftArrow[8] = {
    0b00010,
    0b00100,
    0b01000,
    0b11111,
    0b01000,
    0b00100,
    0b00010,
    0b00000
    };
byte checkMark[8] = {
    0b00000,
    0b00001,
    0b00010,
    0b10100,
    0b01000,
    0b00000,
    0b00000,
    0b00000
    };

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
int speed;   //controlled by encoder
//FSM
enum STATES {Skip, Debug, Home, Shuffle, Scan, Presolve, Solve};
STATES state;
STATES stateLoop;
//TIMERS
int Timer1AVal; //button1 led count value  //number of wave toggles - set to 2x num of square waves wanted,  -1 for infinite (stop with TIMSK1 |= (0 << OCIE1A);)
int Timer1BVal; //button2 led count value
//ENCODER
int lineSelected; //used for item selection
//RANDOM SHUFFLE SEED
uint32_t oldSeed;
uint32_t seed;
//SCAN SEQUENCE RECIEVED
bool scanned;
String inputSequence;
//AUTO-SOLVE or STEP-SOLVE
bool solveType;
//String moves[]; //store 


void setup() {
  //START SERIAL PORT//
  Serial.begin(9600);

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
  //ONBOARD LED
  pinMode(led, OUTPUT);

  //ENCODER INPUT PIN DEFINTIONS, INTERRUPTS, AND POSITION CONFIG//
  pinMode(EncA, INPUT);  //using an external 10k pullup resistor
  pinMode(EncB, INPUT);
  PCICR |= B00000001;  //Enable pin change interrupt on port B (D8-D13) (pins 14-19)
  PCMSK0 |= B00000100;  //Enable interrupts for pin D10 (pins 16, EncA)


  //SYSTEM
  //STATE MACHINE START
  state = Home;

  speed = 50;

  //Timer 1 for button1 and 2 blink led
  Timer1Config(0.9);  //config timer1 @ 0.9 Hz

  scanned = 0; //has not scanned when powered up
  inputSequence = "";
  solveType = 0; //set tp auto solve

  //startup dance
  lcd.setCursor(2, 0);
  lcd.print("Rubik's Cube");
  lcd.setCursor(5, 1);
  lcd.print("Solver");

  startupShow();

  lcd.setRGB(100, 100, 100); //set to white for normal operation
}


void loop() 
{

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
      lcd.print(speed); 
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
      blinkRed(-1);
      
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
        lcd.setCursor(1, 0);
        lcd.print("Step: ");

        //create array of moves
        int spaceIndex = 0;
          while(inputSequence.length() > 0)            //process through sequence string of face moves
          {
            spaceIndex = inputSequence.indexOf(" ");
            String tempFirst = inputSequence.substring(0, spaceIndex);    //find space separation, then find command up to first space
            //Serial.print("Processing " + tempFirst + ":  ");

            decodeAndRunMotor(tempFirst);                                 //run motors based on first command in string     

            lcd.setCursor(14,1);  //display current command in bottom right of screen
            lcd.print(tempFirst);
            lcd.print(" ");

            if(spaceIndex == -1)
              inputSequence = "";
            else
              inputSequence = inputSequence.substring(spaceIndex + 1, inputSequence.length());    //remove first command from string and repeat
          }
      }
      else{ //if auto-solve
        blinkRed(-1);

        lcd.setCursor(0, 0);
        lcd.print("Speed:");
        lcd.print(speed); 
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
      if(CCWFlag && digitalRead(button1) && digitalRead(button2)){
        state = Home;
        CCWFlag = 0;
      }

      //ENCODER HANDLERS
      if(CWFlag){  //if encoder is rotates clockwise
        motor3.setSpeed(90);
        motor3.rotate(1);
        if(speed < 100)
          speed = speed + 5;
        lcd.setCursor(11,1);
        lcd.print(speed);
        CWFlag = 0;  //reset flag for next time
      }
      if(CCWFlag){
        if(speed > 5)
          speed = speed - 5;
        lcd.setCursor(11,1);
        lcd.print(speed);
        lcd.print(" "); //might be shorter number
        CCWFlag = 0;  //reset flag for next time
      }

      //PUSH BUTTON HANDLERS
      if(B1Flag && Timer1AVal == 0){ //if button is pushed and timer is ready to output wave (avoids a rare led always on state)
        lcd.setCursor(4,1);
        lcd.print("1");
        blinkYellow(2);
        B1Flag = 0;
      }
      if(B2Flag && Timer1BVal == 0){
        lcd.setCursor(4,1);
        lcd.print("2");
        blinkRed(2);
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

        setAllMotorSpeed(90);
        
        //generate 22 random moves
        for(int i = 0; i < 23; i++){
          int num = random(0,12); //0,1,2,3,4,5,6,7,8,9,10,11 (8.33%) (CW & CCW for each of 6 faces)

          lcd.setCursor(0, 1); //display current shuffle move to screen
          lcd.print("Motor ");
          lcd.print(num/2);
          lcd.print(" ");
          if(num%2)
            lcd.print("CW      ");
          else
            lcd.print("CCW     ");

          switch(num/2){ //0,1,2,3,4,5  (16.67%)
            case 0:
              motor1.rotate(num%2); //0,1 (50%) //0=CW, 1=CCW
            break;
            case 1:
              motor2.rotate(num%2);
            break;
            case 2:
              motor3.rotate(num%2);
            break;
            case 3:
              motor4.rotate(num%2);
            break;
            case 4:
              motor5.rotate(num%2);
            break;
            case 5:
              motor6.rotate(num%2);
            break;
            default:

            break;
          }
        }

        scanned = 0; //must rescan if shuffled
        inputSequence = "";
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

        Serial.println("1"); //send serial command to begin scan

        lcd.setCursor(0, 0);
        lcd.print("Initiating scan ");
        lcd.setCursor(0, 1);
        lcd.print("                ");

        lcd.setCursor(0, 1);
        for(int i = 0; i < 16; i++){
          lcd.print(">");
          delay(300);
        }

        //WAIT FOR SERIAL STRING COMMAND//
        while (Serial.available() == 0) {  //wait (loop) for serial string data available
          if(B1Flag){  //if home button pushed while waiting - transition home
            state = Home;
            B1Flag = 0;
            break;
          }
        }            
        
        if(state != Home){ //if home button wasn't pushed to exit loop
          inputSequence = Serial.readString();   //read until timeout
          inputSequence.trim(); 
          
          int i = 0;
          int s = 0;
          //for (i=0; inputSequence[i]; inputSequence[i]=='.' ? i++ : *s++); //determine length of input string

          scanned = 1;
          state = Home;
        }

        B2Flag = 0;
      }

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
          solveType = 0;
        else
          solveType = 1;
        
        state = Solve;
        BEFlag = 0;
      }

      break;
    case Solve://**/////////////////////////////////////////////////////////////////////////////////////////**

      if(solveType){ //if step-solve


      }
      else{  //if auto-solve
        //ENCODER HANDLERS
        if(CWFlag){  //if encoder is rotates clockwise
          if(speed < 100)
            speed = speed + 5;
          setAllMotorSpeed(speed);
          lcd.setCursor(6,0);
          lcd.print(speed);
          lcd.print("% ");
          CWFlag = 0;  //reset flag for next time
        }
        if(CCWFlag){
          if(speed > 5)
            speed = speed - 5;
          setAllMotorSpeed(speed);
          lcd.setCursor(6,0);
          lcd.print(speed);
          lcd.print("% ");
          CCWFlag = 0;  //reset flag for next time
        }

        if(B2Flag){ //button to start solve, run motor sequence
          blinkStop(); //stop button blinking
          digitalWrite(button2Led, HIGH); //turn button solid

          lcd.setCursor(0,1);  //clear bottom of screen
          lcd.print("                ");

          unsigned long startTime = millis();
          int spaceIndex = 0;
          while(inputSequence.length() > 0)            //process through sequence string of face moves
          {
            spaceIndex = inputSequence.indexOf(" ");
            String tempFirst = inputSequence.substring(0, spaceIndex);    //find space separation, then find command up to first space
            //Serial.print("Processing " + tempFirst + ":  ");

            decodeAndRunMotor(tempFirst);                                 //run motors based on first command in string     

            lcd.setCursor(14,1);  //display current command in bottom right of screen
            lcd.print(tempFirst);
            lcd.print(" ");

            if(spaceIndex == -1)
              inputSequence = "";
            else
              inputSequence = inputSequence.substring(spaceIndex + 1, inputSequence.length());    //remove first command from string and repeat
          }

          unsigned long duration = (millis() - startTime);

          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("Solve completed ");
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
          inputSequence = "";
          state = Home;
          B2Flag = 0;
        }

      }

      //if either auto-solve or step-solve
      if(B1Flag){ //transition home
        state = Home;
        B1Flag = 0;
      }

      if(BEFlag)
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

void blinkRed(int amount)
{
  Timer1BVal = amount;  //set counter
  TIMSK1 |= (1 << OCIE1A);  //turn on timer
}

void startupShow(){
  blinkYellow(-1);
  blinkRed(-1);
  for(int i=0; i<256; i++){     //nothing to white   end 255,255,255
      lcd.setRGB(i, i, i);
  }
  delay(20);
  for(int i=0; i<256; i++){     //white to red    end 255,0,0
      lcd.setRGB(255, 255-i, 255-i);
  }
  delay(20);
  for(int i=0; i<256; i++){     //red to blue    end 0,0,255
      lcd.setRGB(255-i, 0, i);
  }
  delay(20);
  for(int i=0; i<256; i++){     //blue to orange    end 255,127,0
      lcd.setRGB(i, i/2, 255-i);
  }
  delay(20);
  for(int i=0; i<256; i++){     //orange to green    end 0,255,0
      lcd.setRGB(255-i, 128+(i/2), 0);
  }
  delay(20);
  for(int i=0; i<256; i++){     //green to yellow    end 255,255,0
      lcd.setRGB(i, 255, 0);
  }
  delay(50);
  blinkStop();
}

void setAllMotorSpeed(double percentage){
  motor1.setSpeed(percentage);
  motor2.setSpeed(percentage);
  motor3.setSpeed(percentage);
  motor4.setSpeed(percentage);
  motor5.setSpeed(percentage);
  motor6.setSpeed(percentage);
}


//input: U L F R B or D (or with ' variant like F')
//sends proper step and direction command to motor - rotates this motor 90 degrees
void decodeAndRunMotor(String faceChar)
{
  if(faceChar == "U'")                     //can't case statement with string :(
    motor1.rotate(1);
  else if(faceChar == "U")
    motor1.rotate(0);
  else if(faceChar == "L'")
    motor2.rotate(1);
  else if(faceChar == "L")
    motor2.rotate(0);
  else if(faceChar == "F'")
    motor3.rotate(1);
  else if(faceChar == "F")
    motor3.rotate(0);
  else if(faceChar == "R'")
    motor4.rotate(1);
  else if(faceChar == "R")
    motor4.rotate(0);
  else if(faceChar == "B'")
    motor5.rotate(1);
  else if(faceChar == "B")
    motor5.rotate(0);
  else if(faceChar == "D'")
    motor6.rotate(1);
  else if(faceChar == "D")
    motor6.rotate(0);
  //else
    //Serial.write("No command found\n");
}
