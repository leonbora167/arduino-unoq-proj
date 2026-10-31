#include "Arduino_RouterBridge.h"
#include "Arduino_LED_Matrix.h"

Arduino_LED_Matrix matrix;
uint8_t frame_buffer[104] = {0};
// 8 rows by 13 columns = 104 bytes (values 0..7 for 3-bit grayscale brightness)

void set_matrix_frame(std::vector<uint8_t> frame)
{
  memset(frame_buffer, 0, sizeof(frame_buffer));
  for (size_t i = 0; i < frame.size() && i < 104; i++) {
    frame_buffer[i] = frame[i];
  }
  // draw() accepts a byte buffer of 104 bytes representing 8x13 pixels
  matrix.draw(frame_buffer);
}

void clear_matrix()
{
  memset(frame_buffer, 0, sizeof(frame_buffer));
  matrix.clear();
}

// LED 3 is controlled via PWM (values 0-255 for RGB color mixing)
void set_led3_color(int r, int g, int b) {
  analogWrite(LED3_R, r);
  analogWrite(LED3_G, g);
  analogWrite(LED3_B, b);
}

// LED 4 is a digital ON/OFF RGB LED (active-low: LOW = ON, HIGH = OFF)
void set_led4_color(bool r, bool g, bool b) {
  digitalWrite(LED4_R, r ? LOW : HIGH);
  digitalWrite(LED4_G, g ? LOW : HIGH);
  digitalWrite(LED4_B, b ? LOW : HIGH);
}

void setup() {
  matrix.begin();
  // Configure 3-bit grayscale so brightness values 0..7 are supported
  matrix.setGrayscaleBits(3);
  matrix.clear();

  // Initialize LED 4 GPIO output pins
  pinMode(LED4_R, OUTPUT);
  pinMode(LED4_G, OUTPUT);
  pinMode(LED4_B, OUTPUT);

  // Turn off LEDs 3 & 4 initially
  set_led3_color(0, 0, 0);
  set_led4_color(false, false, false);

  Bridge.begin();
  Bridge.provide("set_frame", set_matrix_frame);
  Bridge.provide("clear_matrix", clear_matrix);
  Bridge.provide("set_led3_color", set_led3_color);
  Bridge.provide("set_led4_color", set_led4_color);
}

void loop() {
  // Main background loop
}
