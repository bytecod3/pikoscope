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

// mapping the input channel values for y-axis spanning
uint8_t current_pot_value = 0;
uint8_t previous_pot_value = 0;
uint8_t potentiometer_change; // find the change that has occured in turning the potentiometer value
float scale_factor = 0.005;
float change_factor, decrease_factor;
uint8_t ch1_val_mapped;

// menu and encoder variables
volatile byte a_flag = 0;
volatile byte b_flag = 0;
volatile uint16_t encoder_position = 0;
volatile uint16_t old_encoder_position = 0;
volatile byte encoder_reading;  // store read values for later comparison


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

  // draw a plus at the midpoint

  display.drawFastHLine(MIDPOINT_X-4, (uint8_t)(SCREEN_HEIGHT+15)/2, 8, WHITE);
  display.drawFastVLine(MIDPOINT_X, ((SCREEN_HEIGHT+16)/2)-(8/2), 8, WHITE);

  display.drawFastHLine(0, ((uint8_t)(SCREEN_HEIGHT+15)/2), SCREEN_WIDTH, WHITE);
  display.drawFastVLine(MIDPOINT_X, 16, SCREEN_HEIGHT-16, WHITE);

  // draw ticks on the horizontal axis
  for(size_t x = 0; x < 128; x++){
    if((x%16) == 0){
      display.drawFastVLine(x, (uint8_t)(SCREEN_HEIGHT+15)/2 -2, 4, WHITE);
    }
  }

  // draw ticks on the vertical axis
  // upper half. Each div is 9.2px, to give me 2.5 divisions on the upper half
  // 2.5 x 2 = 5V which is the p-p voltage capability of this piko-scope
  display.drawFastHLine(MIDPOINT_X, 30 - 2, 4, WHITE);
  display.drawFastHLine(MIDPOINT_X, 21 - 2, 4, WHITE);
  
  // lower half
  display.drawFastHLine(MIDPOINT_X, 48 - 2, 4, WHITE);
  display.drawFastHLine(MIDPOINT_X, 57 - 2, 4, WHITE);

  display.display();
}


uint8_t span_y(uint8_t magnitude){
    /*
    Y-axis magnitude spanning algorithm
    */

    // read the potentiometer
    current_pot_value = analogRead(Y_SPANNER);
    current_pot_value = map(current_pot_value, 0, 255, 16, 63);

    //potentiometer_change = current_pot_value - previous_pot_value;
    // Serial.println(potentiometer_change);
    
    // decrease/ increase factor
    // Minimum signal displayed = 2mV
    // maximum = 5000V == 5V
    // difference  = 4998mV
    // for 1K-Ohm pot, 1 Ohm == ~5mV

    change_factor = current_pot_value  * scale_factor;
    magnitude = magnitude * change_factor;
    // Serial.print("Mag: ");
    // Serial.println(magnitude);

    return magnitude;
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
    uint8_t value_to_render =  span_y(ch1[h + start]);
    //display.drawPixel(h, 79 - (value_to_render), WHITE); //79 offsets the upper 16 px reserved for displaying signal parameters
    display.drawPixel(h, 15 + value_to_render, WHITE);
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

void staticMenu(){
  /*
  Display a static menu when the device is first powered
  */

}

// void runMenu(){
//   /*
//   ISR routine
//   Run this function when encoder is rotated 
//   If normal signal sampling is being done, interrupt the signal display and show menu
//   */

//   cli();  // stop interrupts happenning
//   Serial.println("Menu called");

//   display.clearDisplay();

//   display.writePixel("Menu", 0, 0);

//   display.display();

//   sei(); // resume interrupts
// }

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
  pinMode(ENC_BUTTON, INPUT_PULLUP);
  pinMode(ENC_STEP, INPUT_PULLUP);
  pinMode(ENC_DIRECTION, INPUT_PULLUP);
  pinMode(Y_SPANNER, INPUT);

  // attach interrupts for rotary encoder menu display
  // user can rotate the menu clockwise or anticlockwise, so monitor for a change
  // attachInterrupt(digitalPinToInterrupt(ENC_DIRECTION), runMenu, RISING);
  // attachInterrupt(digitalPinToInterrupt(ENC_STEP), runMenu, RISING);


}

void loop() {

  // record start time of the sampling
  if(i == 0)
    sample_start_time = micros();

  // do the actual sampling
  if((++count) % sample_rate == 0 ){ // take sample for this iteration
    ch1[i++] = map(analogRead(CH1), 0, 1023, 16, 63); // map the value to fit on screen
  }

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