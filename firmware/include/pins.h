#ifndef PINS_H
#define PINS_H

// pin definitions for rotary encoder
#define BUTTON_PIN    2
#define DIRECTION_PIN 3
#define STEP_PIN      4

// pin definitions for oled 
#define SDA 20
#define SCL 21

// pins for channel inputs
#define CH1 A0

// other features
#define SCREEN_HOLD 4  // freeze the screen
#define TRIGGER_ENABLE 5

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C
#define MIDPOINT_Y (SCREEN_HEIGHT/2)
#define MIDPOINT_X (SCREEN_WIDTH/2)
#define GRID_DASH_ENABLE 0 // draw dashed grids

// pin definitions for rotary encoder
#define ENC_BUTTON 7
#define ENC_STEP    2
#define ENC_DIRECTION   3   // this pin supports interrupts on atmega

#endif
