#include <rc_usefulincludes.h>
// main roboticscape API header
#include "udp.h"
#include <roboticscape.h>
#include <time.h>
#include <stdlib.h>
#include <rc/motor.h> 

int pin1 = 1;
int pin2 =  8;
int frequency = 50;
char ip_target1[] = "172.25.55.237";
int msg_signal;
int ang_offset;

void forward(int pin1, int pin2, int frequency) {
    rc_servo_power_rail_en(1);
    rc_servo_send_pulse_normalized(pin1, -1);
    //rc_usleep(100000/30);
    rc_servo_send_pulse_normalized(pin2, 1);
    rc_usleep(100000/frequency);
}
void stop(int pin1, int pin2, int frequency) {
    rc_servo_send_pulse_normalized(pin1, 0);
    rc_servo_send_pulse_normalized(pin2, 0);
    //rc_servo_power_rail_en(1);
}
void turn_left(int pin1, int pin2, int frequency) {
    rc_servo_power_rail_en(1);
    rc_servo_send_pulse_normalized(pin1, 1);
    rc_servo_send_pulse_normalized(pin2, 1);
    rc_usleep(100000/frequency);
}
void turn_right(int pin1, int pin2, int frequency) {
    rc_servo_power_rail_en(1);
    rc_servo_send_pulse_normalized(pin1, -1);
    rc_servo_send_pulse_normalized(pin2, -1);
    rc_usleep(100000/frequency);
}

int main (int argc, char *argv[]) {
    // always initialize cape library first
    udp_init();
    uint8_t signal = 0;
    mavlink_message_t msg;
    
    if (rc_servo_init()) {
            fprintf(stderr,"ERROR: failed to initialize rc_initialize(), are you root?");
            return -1;
    }
    
    rc_set_state(RUNNING);
    while (rc_get_state() != EXITING) {
        if (rc_get_state() == RUNNING) {
            if (read_from_socket(ip_target1, &msg)) {
                //message received, decode
                uint8_t message_type = decode_get_message_type(&msg);
                //printf("got: %d\n", message_type);
                switch (message_type) {
                    case MESSAGE_SIGNAL:
                        signal = decode_get_signal(&msg);
                        //printf("got sig: %d\n", signal);
                            if(signal == SIGNAL_STOP) {
                                stop(pin1, pin2, frequency);
                            } else if(signal == SIGNAL_RUN) {
                                //printf("going\n");
                                forward(pin1, pin2, frequency);
                            } else if(signal == SIGNAL_OOB) {
                                stop(pin1, pin2, frequency);
                            }
                        break;
                    case MESSAGE_ANGLE:
                        ang_offset = decode_get_angle(&msg);
                        if ((ang_offset > 3) && (ang_offset < 180)) {
                            turn_right(pin1, pin2, frequency);
                        } else if ((ang_offset < -3) && (ang_offset > -180)) {
                            turn_left(pin1, pin2, frequency);
                        }
                    break;
                    default:
                        break;
                }
            }
            sleep(0.01);
        }
    }
}
