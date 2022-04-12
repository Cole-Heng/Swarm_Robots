/*This code is used to randomly assign the two agents the either drive in the
  shape of an M or U. Once assigned the overhead computer will confirm the
  agents are at the starting position and then send a signal to start. The 
  agents will move to coordinates inside the grid that will spell out the M or U
  over time. 
*/
#include <rc_usefulincludes.h>
// main roboticscape API header
#include <roboticscape.h>
#include <time.h>
#include <stdlib.h>
#include <rc/motor.h>

int main(int argc, char *argv[]){
    // always initialize cape library first
    if(rc_servo_init()){
            fprintf(stderr,"ERROR: failed to initialize rc_initialize(), are you root?");
            return -1;
    }
    int pin1 = 1;
    int pin2 = 8;
    int frequency = 50;
    int RandAssignment;
    int overheadinterrupt;
    
    rc_set_state(RUNNING);
    rc_servo_power_rail_en(1);
    // done initializing so set state to RUNNING
    while(rc_get_state()!=EXITING){
        // handle other states
        //int rc_motor_init_freq ();
        srand(time(NULL));
        RandAssignment
        if(rc_get_state()==RUNNING){
            if(RandAssignment == 1){
                //spell out M
                //get to starting position
                while(overheadinterrupt = 1){
                    //recieve coordinate n1
                    while(atcoord != 1){ //moving towards point
                        rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 1.5){ //turning right 135 degrees
                        rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, -1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                        //printf("turning left\n");
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 2){
                    //recieve coordinate n2
                    //drive to n2
                    while(atcoord != 1){
                        rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 1){ //turn left 90 degrees
                        rc_servo_send_pulse_normalized(pin1, 1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 3){
                    //recieve coordinate n3
                    //drive to n3
                    while(atcoord != 1){
                        rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 1.5){
                        rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, -1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                        //printf("turning left\n");
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 4){
                    //recieve coordinate n4
                    //drive to n4
                    while(atcoord != 1){
                         rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                rc_servo_send_pulse_normalized(pin1, 0);
                rc_servo_send_pulse_normalized(pin2, 0);
            }
            if(RandAssignment == 2){
                //spell out U
                //get to starting position
                //go forward until at position
                while(overheadinterrupt = 1){
                    //recieve coordinate n1
                    //drive to n1
                    while(atcoord != 1){
                         rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 0.5){
                        rc_servo_send_pulse_normalized(pin1, 1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                        //printf("turning left\n");
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 2){
                    //recieve coordinate n2
                    //drive to n2
                    while(atcoord != 1){
                         rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 0.5){
                        rc_servo_send_pulse_normalized(pin1, 1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                        //printf("turning left\n");
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 3){
                    //recieve coordinate n3
                    //drive to n3
                    while(atcord != 1){
                        rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 0.5){
                        rc_servo_send_pulse_normalized(pin1, 1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                        //printf("turning left\n");
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 4){
                    //recieve coordinate n4
                    //drive to n4
                    while(atcoord != 1){
                         rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                    //stop movement when at goal coord
                    rc_servo_send_pulse_normalized(pin1, 0);
                    rc_servo_send_pulse_normalized(pin2, 0);
                    //turn to prepare for next coord
                    time_t seconds = time(NULL);
                    clock_t timer = seconds;
                    int diff1;
                    while(diff1 < 0.5){
                        rc_servo_send_pulse_normalized(pin1, 1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                        time_t seconds = time(NULL);
                        diff1 = seconds - timer;
                        //printf("turning left\n");
                    }
                    rc_servo_init();
                    rc_servo_power_rail_en(1);
                    diff1 = 0;
                    //rc_servo_send_pulse_normalized(pin1, 0);
                    sleep(2);
                    if(overheadinterrupt = 0){
                        break;
                    }
                }
                while(overheadinterrupt = 5){
                    //recieve coordinate n5
                    //drive to n5
                    while(atcoord != 1){
                         rc_servo_send_pulse_normalized(pin1, -1);
                        rc_servo_send_pulse_normalized(pin2, 1);
                        rc_usleep(100000/frequency);
                    }
                }
                rc_servo_send_pulse_normalized(pin1, 0);
                rc_servo_send_pulse_normalized(pin2, 0);
            }