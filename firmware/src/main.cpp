#include <Arduino.h>
#include "pins.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <SPI.h>
#include <Wire.h>

#define TEXT_SIZE 2
#define VISIBLE_PIXELS 128
#define BUFFER_SIZE (2 * VISIBLE_PIXELS) // Twice as many, to help find trigger point

byte ch1[BUFFER_SIZE]; // channel 1 values. these values must be mapped to between 15 and 63
int i = 0;
int count = 0;

unsigned long sample_start_time = 0; // store the moment when the current sampling starts
unsigned long total_sample_time;
int sample_rate = 1; // sample once every time through the loop

uint8_t ch1_val_mapped;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire);

void displayln(const char* format, ...){
  char buffer[32];

  va_list args;
  va_start(args, format);
  vsprintf(buffer, format, args);
  va_end(args);

  int len = strlen(buffer);
  for(int i = 0; i < len; i++){
    display.write(buffer[i]);
  }
}

void drawGrid(){
  display.clearDisplay();

  display.drawLine(0, 16, 0, 64, WHITE); // vertical axis
  display.drawLine(0, 63, 128, 63, WHITE); // horizontal axis

  display.drawFastHLine(0, 16, 3, WHITE);
  display.drawFastHLine(0, 24, 3, WHITE);
  display.drawFastHLine(0, 33, 3, WHITE);
  display.drawFastHLine(0, 42, 3, WHITE);
  display.drawFastHLine(0, 51, 3, WHITE);
  
  display.display();
}

void drawValues(){
  int start = 0;

  if(digitalRead(TRIGGER_ENABLE)){
    // find the first occurence of zero
    for(int k = 0; k < BUFFER_SIZE; k++){
      if(ch1[i] == 0){
        // find the next value that is not zero
        for(; k < BUFFER_SIZE; k++){
          if(ch1[i] != 0){
            start = i;
            break;
          }
        }
        break;
      }
    }

    // if trigger pint is beyond the width of our screen, wave will be distorted
    if(start >= VISIBLE_PIXELS){
      return;
    }
  }

  for(int h = 0; h < VISIBLE_PIXELS; h++){
    display.drawPixel(h, 79 - (ch1[h + start]), WHITE); //79 offsets the upper 16 px reserved for displaying signal parameters
  }

}

void drawParams(unsigned long time){
  /*
  Show parameters of the sampled signal
  */

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);

  displayln("%ld us", time);
  
}

void setup() {
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // init serial monitor
  Serial.begin(9600);

  display.clearDisplay();
  display.setTextSize(TEXT_SIZE);

  drawGrid();

  // pin mode setups
  pinMode(CH1, INPUT);
}

void loop() {
  // record start time of the sampling
  if(i == 0)
    sample_start_time = micros();

  // do the actual sampling
  if((++count) % sample_rate == 0 ) // take sample for this iteration
    ch1[i++] = map(analogRead(CH1), 0, 1023, 16, 63); // map the value to fit on screen

  // if the buffer is full, draw on the screen
  if(i >= BUFFER_SIZE){
    // get time taken to take the sample
    total_sample_time = ((micros() - sample_start_time)) / 2; // divide by two because we are taking twice as many samples to find the trigger point

    // calculate the frequency

    if(!digitalRead(SCREEN_HOLD)){
      // show wave on screen
      display.clearDisplay();
      drawGrid();
      drawValues();
      drawParams(total_sample_time);
      display.display();
    }

    // reset for next sampling run
    i = 0;
    count = 0;
  }
}