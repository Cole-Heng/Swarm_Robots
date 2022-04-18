#import imp
import os
import time
from math import atan2, degrees, radians, pi, cos, sin, sqrt
import cv2
import sys
import os
import tags
import apriltag

def send_signal_stop(bot_id):
    print(str(0) + "," + str(0) + "," + str(bot_id), flush=True)

def send_signal_start(bot_id):
    print(str(0) + "," + str(1) + "," + str(bot_id), flush=True)

def send_signal_OOB(bot_id):
    print(str(0) + "," + str(2) + "," + str(bot_id), flush=True)

def send_pos_home(x, y, bot_id):
    print(str(1) + "," + str(0) + "," + str(x) + "," + str(y) + "," + str(bot_id), flush=True)

def send_pos_current(x, y, bot_id):
    print(str(1) + "," + str(1) + "," + str(x) + "," + str(y) + "," + str(bot_id), flush=True)

def send_pos_target(x, y, bot_id):
    print(str(1) + "," + str(2) + "," + str(x) + "," + str(y) + "," + str(bot_id), flush=True)

#TODO: add send vector if needed

def send_angle(theta, bot_id):
    print(str(3) + "," + str(theta) + "," + str(bot_id), flush=True)

def calc_offset(x_bot, y_bot, x_tar, y_tar, x_c1, y_c1, x_c2, y_c2):
    theta1 = float(degrees(atan2((y_tar - y_bot), (x_tar - x_bot))))
    theta2 = float(degrees(atan2((y_c1 - y_c2), (x_c1 - x_c2))))
    offset = theta1 - theta2
    if (offset > 180.0):
        offset = offset - 360
    elif (offset < -180.0):
        offset = offset + 360
    #offset = float(degrees(atan2((m_bot - m_target), (1 + (m_bot * m_target)))))
    #if (offset < 0):
    #    offset = -1 * (180 + offset)
    return offset * -1

def calc_slope(x1, y1, x2, y2):
    #if (x2 - x1 == 0):
    #    return ((float(y1) - float(y1)) / 0.1)
    return ((float(y1) - float(y2)) / (float(x2) - float(x1)))

def calc_dist(target, bot):
    return abs(sqrt(float((pow((target[0] - bot[0]), 2) + pow((target[1] - bot[1]), 2)))))

def mark_debug(frame, x_b, y_b, x_t, y_t):
    out = frame
    for i in range(len(x_b)):
        cv2.circle(out, (int(x_b[i]), int(y_b[i])), 5, (0, 255, 0), -1)
        cv2.circle(out, (int(x_t[i]), int(y_t[i])), 15, (255, 0, 0), 1)
    cv2.imshow("DEBUG", out)


def main():
    send_signal_stop(0)
    send_signal_stop(1)
    DEBUG = True
    nBots = 2
    x_t = [None] * nBots
    y_t = [None] * nBots
    x_b = [None] * nBots
    y_b = [None] * nBots
    bot_0_stage = 0
    bot_1_stage = 0
    msg_0_count = 0
    msg_1_count = 0

    #if (DEBUG == True):
        #print("Code Location: Begin")
        #print("----------------")

    # read for tag centers until all tags have been found and localized
    while (any(elem is None for elem in x_b) or any(elem is None for elem in y_b)):
        frame = tags.get_frame()
        results = tags.find_tags(frame)
        centers = tags.get_bot_centers(results, nBots)
        if (len(centers) == 2):
            for i in range(nBots) :
                if (centers[i][0] == -1):
                    continue
                x_b[i] = centers[i][0]
                y_b[i] = centers[i][1]

    x_t[0] = x_b[0] + (100 * cos(pi / 3))
    y_t[0] = y_b[0] - (100 * sin(pi / 3))
    x_t[1] = x_b[1] + 0
    y_t[1] = y_b[1] + 75

    frame_mod = frame
    bot_0_offset = None
    bot_1_offset = None
    while True:
        if (DEBUG == True):
            #print("Code Location: Orienting Bots")
            for i in range(len(x_b)):
                #print("bot#:" + str(i))
                #print("location: " + str(x_b[i]) + ", " + str(y_b[i]))
                #print("Target: " + str(x_t[i]) + ", " + str(y_t[i]))
                #print("------")
                mark_debug(frame_mod, x_b, y_b, x_t, y_t)
            #print("----------------")
            if cv2.waitKey(1) & 0xFF == ord('1'):
                break

        frame = tags.get_frame()
        results = tags.find_tags(frame)
        corners = tags.get_two_corners(results, nBots)
        centers = tags.get_bot_centers(results, nBots)
        if (len(centers) == 2):
            for i in range(nBots) :
                if (centers[i][0] == -1):
                    continue
                x_b[i] = centers[i][0]
                y_b[i] = centers[i][1]
        frame_mod = frame

        if (corners[0] != None):
            #bot_0_slope = calc_slope(corners[0][0], corners[0][1], corners[0][2], corners[0][3])
            #target_1_slope = calc_slope(x_t[0], y_t[0], x_b[0], y_b[0])
            bot_0_offset = calc_offset(x_b[0], y_b[0], x_t[0], y_t[0], corners[0][0], corners[0][1], corners[0][2], corners[0][3])
            if (bot_0_offset != None):
                if (abs(bot_0_offset) >  5):
                    msg_0_count = msg_0_count + 1
                    if (msg_0_count >= 10):
                        msg_0_count = 0
                        send_angle(bot_0_offset, 0)

        if (corners[1] != None):
            #bot_1_slope = calc_slope(corners[1][0], corners[1][1], corners[1][2], corners[1][3])
            #target_2_slope = calc_slope(x_t[1], y_t[1], x_b[1], y_b[1])
            #bot_1_offset = calc_offset(target_2_slope, bot_1_slope)
            bot_1_offset = calc_offset(x_b[1], y_b[1], x_t[1], y_t[1], corners[1][0], corners[1][1], corners[1][2], corners[1][3])
            #cv2.line(frame_mod, (corners[1][0], corners[1][1]), (corners[1][2], corners[1][3]), (0, 0, 255), 1)
            #cv2.circle(frame_mod, (corners[1][0], corners[1][1]), 3, (255, 255, 0), -1)
            if (bot_1_offset != None):
                if (abs(bot_1_offset) >  5):
                    msg_1_count = msg_1_count + 1
                    if (msg_1_count >= 10):
                        msg_1_count = 0
                        send_angle(bot_1_offset, 1)

        cv2.putText(frame_mod, str(bot_0_offset), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame_mod, str(bot_1_offset), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if (bot_0_offset != None and bot_1_offset != None):
            if (abs(bot_0_offset) <= 5 and abs(bot_1_offset) <= 5):
                break

    send_signal_start(0)
    send_signal_start(1)
    msg_0_count = 0
    msg_1_count = 0
    msg_0_go_count = 0
    msg_1_go_count = 0
    while (bot_0_stage < 4 or bot_1_stage < 5): 
        frame_mod = frame
        if (DEBUG == True):
            #print("Code Location: Shape Control")
            cv2.putText(frame_mod, str(bot_0_offset), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame_mod, str(bot_1_offset), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame_mod, str(bot_0_stage), (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame_mod, str(bot_1_stage), (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            for i in range(len(x_b)):
                #print("bot#:" + str(i))
                #print("location: " + str(x_b[i]) + ", " + str(y_b[i]))
                #print("Target: " + str(x_t[i]) + ", " + str(y_t[i]))
                #print("------")
                mark_debug(frame_mod, x_b, y_b, x_t, y_t)
            #print("----------------")
            #cv2.putText(frame_mod, str(bot_0_offset), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            #cv2.putText(frame_mod, str(bot_1_offset), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            #cv2.putText(frame_mod, str(bot_0_stage), (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            #cv2.putText(frame_mod, str(bot_1_stage), (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if cv2.waitKey(1) & 0xFF == ord('1'):
                break

        frame = tags.get_frame()
        results = tags.find_tags(frame)
        centers = tags.get_bot_centers(results, nBots)
        corners = tags.get_two_corners(results, nBots)

        for i in range(nBots):
            if (len(centers[i]) == 2):
                if (centers[i][0] == -1):
                    continue
                x_b[i] = centers[i][0]
                y_b[i] = centers[i][1]

        if (calc_dist([x_t[0], y_t[0]], [x_b[0], y_b[0]]) <= 15 and bot_0_stage < 4):
            send_signal_stop(0)
            bot_0_stage = bot_0_stage + 0.5
            if (bot_0_stage == 0.5):
                x_t[0] = x_b[0] + (50 * cos(pi / 4))
                y_t[0] = y_b[0] + (50 * sin(pi / 4))
            if (bot_0_stage == 1.5):
                x_t[0] = x_b[0] + (50 * cos(pi / 4))
                y_t[0] = y_b[0] - (50 * sin(pi / 4))
            if (bot_0_stage == 2.5):
                x_t[0] = x_b[0] + (100 * cos(pi / 3) + 5)
                y_t[0] = y_b[0] + (100 * sin(pi / 3))
            if (bot_0_stage == 3.5):
                x_t[0] = x_b[0]
                y_t[0] = y_b[0] + 25
        elif (bot_0_stage % 1 == 0.0 and bot_0_stage != 4):
            msg_0_go_count += 1
            if (msg_0_go_count >= 4):
                msg_0_go_count = 0
                send_signal_start(0)


        if (calc_dist([x_t[1], y_t[1]], [x_b[1], y_b[1]]) <= 15 and bot_1_stage < 5):
            send_signal_stop(1)
            bot_1_stage = bot_1_stage + 0.5
            if (bot_1_stage == 0.5):
                x_t[1] = x_b[1] + (50 * cos(pi / 4))
                y_t[1] = y_b[1] + (50 * sin(pi / 4))
            if (bot_1_stage == 1.5):
                x_t[1] = x_b[1] + 50
                y_t[1] = y_b[1]
            if (bot_1_stage == 2.5):
                x_t[1] = x_b[1] + (50 * cos(pi / 4))
                y_t[1] = y_b[1] - (50 * sin(pi / 4))
            if (bot_1_stage == 3.5):
                x_t[1] = x_b[1]
                y_t[1] = y_b[1] - 75
            if (bot_1_stage == 4.5):
                x_t[1] = x_b[1]
                y_t[1] = y_b[1] + 75
        elif (bot_1_stage % 1 == 0.0 and bot_1_stage != 5):
            msg_1_go_count += 1
            if (msg_1_go_count >= 4):
                msg_1_go_count = 0
                send_signal_start(1)

        if (bot_0_stage % 1 == 0.5):
            if (corners[0] != None):
                #bot_0_slope = calc_slope(corners[0][0], corners[0][1], corners[0][2], corners[0][3])
                #target_1_slope = calc_slope(x_t[0], y_t[0], x_b[0], y_b[0])
                #bot_0_offset = calc_offset(target_1_slope, bot_0_slope)
                bot_0_offset = calc_offset(x_b[0], y_b[0], x_t[0], y_t[0], corners[0][0], corners[0][1], corners[0][2], corners[0][3])
                if (bot_0_offset != None):
                    if (abs(bot_0_offset) >  5):
                        msg_0_count = msg_0_count + 1
                        if (msg_0_count >= 8):
                            msg_0_count = 0
                            send_angle(bot_0_offset, 0)
                    else:
                        bot_0_stage = bot_0_stage + 0.5
                        if (bot_0_stage != 4):
                            send_signal_start(0)

        if (bot_1_stage % 1 == 0.5):
            if (corners[1] != None):
                #bot_1_slope = calc_slope(corners[1][0], corners[1][1], corners[1][2], corners[1][3])
                #target_2_slope = calc_slope(x_t[1], y_t[1], x_b[1], y_b[1])
                #bot_1_offset = calc_offset(target_2_slope, bot_1_slope)
                bot_1_offset = calc_offset(x_b[1], y_b[1], x_t[1], y_t[1], corners[1][0], corners[1][1], corners[1][2], corners[1][3])
                if (bot_1_offset != None):
                    if (abs(bot_1_offset) >  5):
                        msg_1_count = msg_1_count + 1
                        if (msg_1_count >= 8):
                            msg_1_count = 0
                            send_angle(bot_1_offset, 1)
                    else:
                        bot_1_stage = bot_1_stage + 0.5
                        if (bot_1_stage != 5):
                            send_signal_start(1)


if __name__ == "__main__":
    main()

