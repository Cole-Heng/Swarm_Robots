#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "udp.h"

int main () {
    udp_init();
    char out_ip1[] = "172.25.53.172";
    char out_ip2[] = "172.25.52.78";
    mavlink_message_t msg;
    //char str_in[25];
    float x = 0.5;
    float y = 1.5;
    float dx = 0, dy = 0;
    printf("begin run\n");
    while (1) {
	char str_in[25];
        //scanf("%f %f", &dx, &dy);
	if (fgets(str_in, 25, stdin) != NULL) {
	    if (strcmp(str_in, "\n") == 0) {
		continue;
	    }
            x = atof(strtok(str_in, ","));
	    y = atof(strtok(NULL, ","));
	}
	encode_position(POS_TARGET, x, y, out_ip1);
	//x = x+1;
	//y = y+1;
    }
}
