#include <common/mavlink.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
#include <sys/time.h>
#include <time.h>
#include <arpa/inet.h>
#include <stdbool.h>

#define BUFFER_LENGTH 2041 // minimum buffer size that can be used with qnx (I don't know why)

// uint64_t microsSinceEpoch();

mavlink_system_t mavlink_system = {
    1, // System ID (1-255)
    1  // Component ID (a MAV_COMPONENT value)
};

int main() {
    char target_ip1[100];
    strcpy(target_ip1, "172.25.52.79");
	char target_ip2[100];
    strcpy(target_ip2, "172.25.52.79");
	
	int sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP);
	struct sockaddr_in out1Addr; 
	struct sockaddr_in out2Addr; 
	struct sockaddr_in locAddr;
	//struct sockaddr_in fromAddr;
	uint8_t buf[BUFFER_LENGTH];
	ssize_t recsize;
	socklen_t fromlen1 = sizeof(out1Addr);
	socklen_t fromlen2 = sizeof(out2Addr);
	int bytes_sent;
	mavlink_message_t msg;
	uint16_t len;
	int i = 0;
	//int success = 0;
	unsigned int temp = 0;

	memset(&locAddr, 0, sizeof(locAddr));
	locAddr.sin_family = AF_INET;
	locAddr.sin_addr.s_addr = INADDR_ANY;
	locAddr.sin_port = htons(14551);

	if (-1 == bind(sock,(struct sockaddr *)&locAddr, sizeof(struct sockaddr)))
    {
		perror("error bind failed");
		close(sock);
		exit(EXIT_FAILURE);
    } 

	/* Attempt to make it non blocking */
#if (defined __QNX__) | (defined __QNXNTO__)
	if (fcntl(sock, F_SETFL, O_NONBLOCK | FASYNC) < 0)
#else
	if (fcntl(sock, F_SETFL, O_NONBLOCK | O_ASYNC) < 0)
#endif
	{
		fprintf(stderr, "error setting nonblocking: %s\n", strerror(errno));
		close(sock);
		exit(EXIT_FAILURE);
    }

	memset(&out1Addr, 0, sizeof(out1Addr));
	out1Addr.sin_family = AF_INET;
	out1Addr.sin_addr.s_addr = inet_addr(target_ip1);
	out1Addr.sin_port = htons(14550);

	memset(&out2Addr, 0, sizeof(out2Addr));
	out2Addr.sin_family = AF_INET;
	out2Addr.sin_addr.s_addr = inet_addr(target_ip2);
	out2Addr.sin_port = htons(14550);
    //mavlink_msg_global_position_int_pack(1,1,);
    printf("Begin Test\n");

	for (int i = 0; i < 50; i++) {
		mavlink_msg_heartbeat_pack(42, 200, &msg, MAV_TYPE_GCS, MAV_AUTOPILOT_INVALID, MAV_MODE_FLAG_TEST_ENABLED, 0, MAV_STATE_ACTIVE);
		len = mavlink_msg_to_send_buffer(buf, &msg);
		bytes_sent = sendto(sock, buf, len, 0, (struct sockaddr*)&out1Addr, sizeof(struct sockaddr_in));

		// mavlink_msg_set_position_target_local_ned_pack(42, 1, &msg, 101010, 1, 1, MAV_FRAME_LOCAL_NED, 0, 3.5, 9.2, 0, 2.5, 8.2, 0, 0, 0, 0, 0, 0);
		// len = mavlink_msg_to_send_buffer(buf, &msg);
		// bytes_sent = sendto(sock, buf, len, 0, (struct sockaddr*)&gcAddr, sizeof(struct sockaddr_in));

		//from addr1
		memset(buf, 0, BUFFER_LENGTH);
		recsize = recvfrom(sock, (void *)buf, BUFFER_LENGTH, 0, (struct sockaddr *)&out1Addr, &fromlen1);
		if (recsize > 0)
      	{
			// Something received - print out all bytes and parse packet
			mavlink_message_t msg;
			mavlink_status_t status;
			
			printf("Bytes Received from addr1: %d\nDatagram: ", (int)recsize);
			for (i = 0; i < recsize; ++i)
			{
				temp = buf[i];
				printf("%02x ", (unsigned char)temp);
				if (mavlink_parse_char(MAVLINK_COMM_0, buf[i], &msg, &status))
				{
					// Packet received
					printf("\nReceived packet: SYS: %d, COMP: %d, LEN: %d, MSG ID: %d\n", msg.sysid, msg.compid, msg.len, msg.msgid);
					if (msg.msgid == 0) {
						printf("%d\n", mavlink_msg_heartbeat_get_system_status(&msg));
					}
				}
			}
			printf("\n");
		}

		//from addr2
		memset(buf, 0, BUFFER_LENGTH);
		recsize = recvfrom(sock, (void *)buf, BUFFER_LENGTH, 0, (struct sockaddr *)&out2Addr, &fromlen2);
		if (recsize > 0)
      	{
			// Something received - print out all bytes and parse packet
			mavlink_message_t msg;
			mavlink_status_t status;
			
			printf("Bytes Received from addr2: %d\nDatagram: ", (int)recsize);
			for (i = 0; i < recsize; ++i)
			{
				temp = buf[i];
				printf("%02x ", (unsigned char)temp);
				if (mavlink_parse_char(MAVLINK_COMM_0, buf[i], &msg, &status))
				{
					// Packet received
					printf("\nReceived packet: SYS: %d, COMP: %d, LEN: %d, MSG ID: %d\n", msg.sysid, msg.compid, msg.len, msg.msgid);
					if (msg.msgid == 0) {
						printf("%d\n", mavlink_msg_heartbeat_get_system_status(&msg));
					}
				}
			}
			printf("\n");
		}

		memset(buf, 0, BUFFER_LENGTH);
		sleep(1); // Sleep one second
	}
	printf("End Test.\n");
    return 0;
}
