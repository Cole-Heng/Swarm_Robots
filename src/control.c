#include <stdio.h>
#include "udp.h"

int main () {
    udp_init();
    char out_ip1[] = "172.25.55.85";
    char out_ip2[] = "172.25.52.78";
    mavlink_message_t msg;

    float x;
    float y;
    printf("begin run");
    while (1) {
        scanf("%f %f", &x, &y);
        encode_position(POS_TARGET, x, y, out_ip1);
    }
}