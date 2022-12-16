#include "EEPROMex.h"
#include "DFRobot_RGBLCD1602.h"

DFRobot_RGBLCD1602 lcd(16, 2); //global lcd object

void setup() {
  lcd.init();
  lcd.setRGB(100, 100, 100);

  lcd.clear();
  lcd.setCursor(0, 0);

  int address = 0;
  uint32_t value = 13;
  //bool complete = EEPROM.updateLong(address, value);
  uint32_t read = EEPROM.readLong(0);
  lcd.print(read);

}

void loop() {
  // put your main code here, to run repeatedly:

}
