#include "btstack.h"
#include "hog_host_test.h"
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "pico/cyw43_arch.h" 

#define HEAD_DIR_PIN 0
#define HEAD_STP_PIN 1
#define HEAD_ENA_PIN 2

#define PLATE_DIR_PIN_1 3
#define PLATE_DIR_PIN_2 6
#define PLATE_DIR_PIN_3 9

#define PLATE_STP_PIN_1 4
#define PLATE_STP_PIN_2 7
#define PLATE_STP_PIN_3 10

#define PLATE_ENA_PIN_1 5
#define PLATE_ENA_PIN_2 8
#define PLATE_ENA_PIN_3 11

#define BUZZER_PIN 22

#define HEAD_POSITION_MAX 100
#define PLATE_POSITION_MAX 100

uint8_t lx      = 128;
uint8_t ly      = 128;
uint8_t rx      = 128;
uint8_t ry      = 128;
uint8_t buttons = 0;
uint8_t hat     = 0;

bool head_homed  = FALSE;
bool plate_homed = FALSE;
bool head_dir    = TRUE;
bool plate_dir   = TRUE;
unsigned long head_position  = 0;
unsigned long plate_position = 0;

unsigned short state = 0;

void second_core_loop() {
    while (TRUE) {
        int stick_lx_position = (128 - lx);
        int stick_ly_position = (128 - ly);
        int stick_rx_position = (128 - rx);
        int stick_ry_position = (128 - ry);

        head_homed = TRUE;
        switch (state) {
            // Movement controlled by cotroller
            case 0:
                if (buttons > 0) {
                    // {A,B,X,Y,LB,RB}
                    uint8_t buttons_value = buttons;
                    bool button_presses[] = {FALSE,FALSE,FALSE,FALSE,FALSE,FALSE};
                    // RB
                    if (buttons_value >= 128) {
                        button_presses[5] = TRUE; 
                        buttons_value     = buttons_value - 128;
                    }
                    // LB
                    if (buttons_value >= 64) {
                        button_presses[4] = TRUE;
                        buttons_value     = buttons_value - 64;
                    }
                    // Y
                    if (buttons_value >= 16) {
                        button_presses[3] = TRUE;
                        buttons_value     = buttons_value - 16;
                    }
                    // X
                    if (buttons_value >= 8) {
                        button_presses[2] = TRUE;
                        buttons_value     = buttons_value - 8;
                    }
                    // B
                    if (buttons_value >= 2) {
                        button_presses[1] = TRUE;
                        buttons_value     = buttons_value - 2;
                    }
                    // A
                    if (buttons_value >= 1) {
                        button_presses[0] = TRUE;
                        buttons_value     = buttons_value - 1;
                    }
                    char buffer[50];
                    snprintf(buffer, sizeof(buffer),"[%d,%d,%d,%d,%d,%d]", button_presses[0], button_presses[1], button_presses[2], button_presses[3], button_presses[4], button_presses[5]);
                    Serial.println(buffer);
                }
                if (abs(stick_lx_position) > 15) {
                    int lx_step_time = 140 - abs(stick_lx_position);
                    if (stick_lx_position > 0) {
                        if (!head_dir) {
                            digitalWrite(HEAD_DIR_PIN, HIGH);
                            head_dir = TRUE;
                            sleep_ms(10);
                        }
                        if ((head_position < HEAD_POSITION_MAX) && head_homed) {
                            digitalWrite(LED_BUILTIN, LOW);
                            digitalWrite(HEAD_STP_PIN, HIGH);
                            sleep_ms(10);
                            digitalWrite(LED_BUILTIN, HIGH);
                            digitalWrite(HEAD_STP_PIN, LOW);
                            sleep_ms(lx_step_time);
                            head_position ++;
                            Serial.println(head_position);
                        }
                    } else {
                        if (head_dir) {
                            digitalWrite(HEAD_DIR_PIN, LOW);
                            head_dir = FALSE;
                            sleep_ms(10);
                        }
                        if ((head_position > 0) && head_homed) {
                            digitalWrite(LED_BUILTIN, LOW);
                            digitalWrite(HEAD_STP_PIN, HIGH);
                            sleep_ms(10);
                            digitalWrite(LED_BUILTIN, HIGH);
                            digitalWrite(HEAD_STP_PIN, LOW);
                            sleep_ms(lx_step_time);
                            head_position --;
                            Serial.println(head_position);
                        }
                    }
                } 
                if (abs(stick_ry_position) > 15) {
                    int ry_step_time = 140 - abs(stick_ry_position);
                    if (stick_ry_position > 0) {
                        if (!plate_dir) {
                            digitalWrite(PLATE_DIR_PIN_1, HIGH);
                            digitalWrite(PLATE_DIR_PIN_2, HIGH);
                            digitalWrite(PLATE_DIR_PIN_3, HIGH);
                            plate_dir = TRUE;
                            sleep_ms(10);
                        }
                        if (plate_position < PLATE_POSITION_MAX) {
                            digitalWrite(LED_BUILTIN, LOW);
                            digitalWrite(PLATE_STP_PIN_1, LOW);
                            digitalWrite(PLATE_STP_PIN_2, LOW);
                            digitalWrite(PLATE_STP_PIN_3, LOW);
                            sleep_ms(10);
                            digitalWrite(LED_BUILTIN, HIGH);
                            digitalWrite(PLATE_STP_PIN_1, HIGH);
                            digitalWrite(PLATE_STP_PIN_2, HIGH);
                            digitalWrite(PLATE_STP_PIN_3, HIGH);
                            sleep_ms(ry_step_time);
                            plate_position ++;
                            Serial.println(plate_position);
                        }
                    } else {
                        if (plate_dir) {
                            digitalWrite(PLATE_DIR_PIN_1, LOW);
                            digitalWrite(PLATE_DIR_PIN_2, LOW);
                            digitalWrite(PLATE_DIR_PIN_3, LOW);
                            plate_dir = FALSE;
                            sleep_ms(10);
                        }
                        if (plate_position > 0) {
                            digitalWrite(LED_BUILTIN, LOW);
                            digitalWrite(PLATE_STP_PIN_1, LOW);
                            digitalWrite(PLATE_STP_PIN_2, LOW);
                            digitalWrite(PLATE_STP_PIN_3, LOW);
                            sleep_ms(10);
                            digitalWrite(LED_BUILTIN, HIGH);
                            digitalWrite(PLATE_STP_PIN_1, HIGH);
                            digitalWrite(PLATE_STP_PIN_2, HIGH);
                            digitalWrite(PLATE_STP_PIN_3, HIGH);
                            sleep_ms(ry_step_time);
                            plate_position --;
                            Serial.println(plate_position);
                        }
                    }
                }
            // Movement controller by UART
            case 1:
                state = 0;
            // Head homing
            case 2:
                state = 0;
            // Plate homing
            case 3:
                state = 0;
        }
    }
}

void registerBootKeyboardEventHandler(BootKeyboardEventHandler callback);

// Event handler function
void myBootKeyboardEventHandler(const uint8_t *data, uint16_t size) {
    // Print the data
    lx      = data[1];
    ly      = data[3];
    rx      = data[5];
    ry      = data[7];
    buttons = data[13]; 
    hat     = data[12];

    char buffer[100];
    snprintf(buffer, sizeof(buffer),"Left Stick: X: %d, Y: %d - Right Stick: X: %d, Y: %d - Hat: %d - Buttons: %d", lx, ly, rx, ry, hat, buttons);
    Serial.println(buffer);
    
    // control the car

}

void setup() {
  sleep_ms(5000);
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(HEAD_ENA_PIN, OUTPUT);
  pinMode(HEAD_DIR_PIN, OUTPUT);
  pinMode(HEAD_STP_PIN, OUTPUT);

  multicore_launch_core1(second_core_loop);

  digitalWrite(LED_BUILTIN, HIGH);
  sleep_ms(500);
  digitalWrite(LED_BUILTIN, LOW);
  sleep_ms(500);

  Serial.println("BTstack on Pico starting...");

  // Setup example
  btstack_main(0, NULL);

  registerBootKeyboardEventHandler(myBootKeyboardEventHandler);

  Serial.println("BTstack on Pico has started.");
}

void loop() {
  btstack_run_loop_execute();
} 
