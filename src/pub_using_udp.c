#include "udp.h"
#include <stdio.h>
#include <time.h>

int main() {
    udp_init();
    char out_ip1[] = "172.25.52.79";
    char out_ip2[] = "172.25.52.78";
    uint8_t signal = 0;
    float p_x_current = 0;
    float p_y_current = 0;
    float p_x_target = 0;
    float p_y_target = 0;
    float v_x_current = 0;
    float v_y_current = 0;
    float v_x_target = 0;
    float v_y_target = 0;
    int pos_type;

    mavlink_message_t *msg;
    for (int i = 0; i < 50; i++) {
        printf("run #%d\n", i);
        //printf("%s\n", out1);
        send_heartbeat(out_ip1);
        encode_position(POS_TARGET, 25, 35, out_ip1);

        //read input
        if(read_from_socket(out_ip1, msg)) {
            //message received, decode
            uint8_t message_type = decode_get_message_type(msg);

            switch(message_type) {
                case MESSAGE_SIGNAL:
                    signal = decode_get_signal(msg);
                    break;
                case MESSAGE_POSITION:
                    pos_type = decode_get_pos_type(msg);
                    if (pos_type == POS_CURRENT) {
                        p_x_current = decode_get_pos_x(msg);
                        p_y_current = decode_get_pos_y(msg);
                    } else if (pos_type == POS_TARGET) {
                        p_x_target = decode_get_pos_x(msg);
                        p_y_target = decode_get_pos_y(msg);
                    }
                default:
                    break;
            }
        }


        sleep(1);
    }
    return 0;
}