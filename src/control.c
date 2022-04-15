#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "udp.h"

int main () {
    udp_init();
    char IPs[2][15];
    strcpy(IPs[0], "172.25.53.172");
    strcpy(IPs[1], "172.25.52.78");
    mavlink_message_t msg;
    //char str_in[25];
    float p1 = -1;
    float p2 = -1;
    float p3 = -1;
    int p4 = -1;
    int message = -1;
    float dx = 0, dy = 0;
    printf("begin run\n");
    while (1) {
	char str_in[25];
        //scanf("%f %f", &dx, &dy);
	if (fgets(str_in, 25, stdin) != NULL) {
	    if (strcmp(str_in, "\n") == 0) {
		continue;
	    }
        message = atoi(strtok(str_in, ","));
	    p1 = atof(strtok(NULL, ","));
        p2 = atof(strtok(NULL, ","));
        if (message == MESSAGE_POSITION) {
            p3 = atof(strtok(NULL, ","));
            p4 = atoi(strtok(NULL, ","));
            encode_position(p1, p2, p3, IPs[p4]);
        } else if (message == MESSAGE_SIGNAL) {
            encode_signal((int)p1, IPs[(int)p2]);
        } else if (message == MESSAGE_VECTOR) {
            //TODO add code for vector if needed
        } else if (message == MESSAGE_ANGLE) {
            encode_angle(p1, IPs[(int)p2]);
        }
	}
	//encode_position(POS_TARGET, x, y, out_ip1);
	//x = x+1;
	//y = y+1;
    }
}
