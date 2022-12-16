#include <Adafruit_NeoPixel.h>

#define PIN 12
#define NUMPIXELS 12

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
}

void loop() {
  pixels.clear();
  for(int i=0; i<NUMPIXELS; i++)
    pixels.setPixelColor(i, pixels.Color(255, 255, 255));
  pixels.show();
}
