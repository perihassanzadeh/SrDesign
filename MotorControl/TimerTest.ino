int Timer1AVal;  //number of wave toggles - 2x num of square waves,  -1 for infinite (stop infinite with TIMSK1 |= (0 << OCIE1A);)
int Timer1BVal;

void setup() {
  //LEDS
  pinMode(A0, OUTPUT);
  pinMode(5, OUTPUT);
  //BUTTONS
  pinMode(A3, INPUT);
  pinMode(A2, INPUT);

  digitalWrite(A0, LOW); //off starting state
  digitalWrite(5, LOW);

  Timer1Config(0.9);  //config timer1 @ 0.9 Hz
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(300); //actually use interrupts for button input so no need to debounce of track states
  if(digitalRead(A3) == HIGH) //if button1
  {
    Timer1AVal = 6;    //3 square waves
    TIMSK1 |= (1 << OCIE1A);  //start timer interrupt
  }
  if(digitalRead(A2) == HIGH)  //if button2
  {
    Timer1BVal = 8;    //4 square waves
    TIMSK1 |= (1 << OCIE1A);  //start timer interrupt
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