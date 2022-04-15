#include <string.h>
#include <stdio.h>
#include <common/mavlink.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>

// Message types
#define MESSAGE_SIGNAL 0
#define MESSAGE_POSITION 1
#define MESSAGE_VECTOR 2
#define MESSAGE_ANGLE 3

#define SIGNAL_STOP 0
#define SIGNAL_RUN 1
#define SIGNAL_OOB 2 //out of bounds

#define POS_HOME 0
#define POS_CURRENT 1
#define POS_TARGET 2

#define BUFFER_LENGTH 2041

void udp_init();
struct sockaddr_in* target_init(const char *target_ip);
void send_heartbeat(const char *target_ip);
uint8_t decode_get_message_type(const mavlink_message_t* msg);

void encode_position(int pos_type, float x, float y, const char *target_ip);
void encode_vector(float vx, float vy, const char *target_ip);
void encode_signal(int signal, const char *target_ip);
void encode_angle(float theta, const char *target_ip);

int decode_get_pos_type(const mavlink_message_t* msg);
float decode_get_pos_x(const mavlink_message_t* msg);
float decode_get_pos_y(const mavlink_message_t* msg);
float decode_get_vec_x(const mavlink_message_t* msg);
float decode_get_vec_y(const mavlink_message_t* msg);

int decode_get_signal(const mavlink_message_t* msg);

float decode_get_angle(const mavlink_message_t* msg);

int read_from_socket(const char *target_ip, mavlink_message_t *msg);

typedef struct vector vector;
struct vector
{
	float x;
	float y;
};
