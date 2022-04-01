#include "udp.h"
#include <stdio.h>
#include <time.h>

int main() {
    udp_init();
    char out1[] = "172.25.52.79";
    for (int i = 0; i < 50; i++) {
        printf("run #%d\n", i);
        //printf("%s\n", out1);
        send_heartbeat(out1);
        sleep(1);
    }
    return 0;
}