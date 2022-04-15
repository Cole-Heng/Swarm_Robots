import imp
import os
import time
from math import atan2, degrees, radians, pi, cos, sin, dist
import cv2
import sys
import os
import tags
import apriltag

def send_signal_stop(bot_id):
    print(str(0) + "," + str(0) + "," + str(bot_id) + "\n")

def send_signal_start(bot_id):
    print(str(0) + "," + str(1) + "," + str(bot_id) + "\n")

def send_signal_OOB(bot_id):
    print(str(0) + "," + str(2) + "," + str(bot_id) + "\n")

def send_pos_home(x, y, bot_id):
    print(str(1) + "," + str(0) + "," + str(x) + "," + str(y) + "," + str(bot_id) + "\n")

def send_pos_current(x, y, bot_id):
    print(str(1) + "," + str(1) + "," + str(x) + "," + str(y) + "," + str(bot_id) + "\n")

def send_pos_target(x, y, bot_id):
    print(str(1) + "," + str(2) + "," + str(x) + "," + str(y) + "," + str(bot_id) + "\n")

#TODO: add send vector if needed

def send_angle(theta, bot_id):
    print(str(3) + "," + str(theta) + "," + str(bot_id) + "\n")

def calc_offset(m_bot, m_target):
    return degrees(atan2((m_bot - m_target), (1 + (m_bot * m_target))))

def calc_slope(x1, y1, x2, y2):
    return ((y2 - y1) / (x2 - x1))


def main():
    nBots = 2
    x_t = [None] * nBots
    y_t = [None] * nBots
    x_b = [None] * nBots
    y_b = [None] * nBots
    bot_1_stage = 0
    bot_2_stage = 0

    # read for tag centers until all tags have been found and localized
    while (any(elem is None for elem in x_b) or any(elem is None for elem in y_b)):
        frame = tags.get_frame()
        results = tags.find_tags(frame)
        centers = tags.get_bot_centers()
        for i in range(nBots) :
            if (centers[i] != None):
                x_b[i] = centers[i][0]
                y_b[i] = centers[i][1]

    x_t[0] = x_b[0] + (100 * cos(pi / 3))
    y_t[0] = y_b[0] + (100 * sin(pi / 3))
    x_t[1] = x_b[1]
    y_t[1] = y_t[1] - 75

    bot1_offset = None
    bot_2_offset = None
    while True:
        frame = tags.get_frame()
        results = tags.find_tags(frame)
        corners = tags.get_two_corners(results, nBots)
        if (corners[0] != None):
            bot_1_slope = calc_slope(corners[0][0], corners[0][1], corners[0][2], corners[0][3])
            target_1_slope = calc_slope(x_t[0], y_t[0], x_b[0], y_b[0])
            bot_1_offset = calc_offset(target_1_slope, bot_1_slope)
            if (bot_1_offset >  1):
                send_angle(bot_1_offset, 1)

        if (corners[1] != None):
            bot_2_slope = calc_slope(corners[1][0], corners[1][1], corners[1][2], corners[1][3])
            target_2_slope = calc_slope(x_t[1], y_t[1], x_b[1], y_b[1])
            bot_2_offset = calc_offset(target_2_slope, bot_2_slope)
            if (bot_2_offset >  1):
                send_angle(bot_2_offset, 2)

        if (bot_1_offset <= 1 and bot_2_offset <= 1):
            break


    send_signal_start(1)
    send_signal_start(2)
    while (bot_1_stage < 4 and bot_2_stage < 5): 
        frame = tags.get_frame()
        results = tags.find_tags(frame)
        centers = tags.get_bot_centers()
        corners = tags.get_two_corners(results, nBots)

        for i in range(nBots) :
            if (centers[i] != None):
                x_b[i] = centers[i][0]
                y_b[i] = centers[i][1]

        if (dist([x_t[0], y_t[0]], [x_b[0], y_b[0]]) <= 10):
            send_signal_stop(1)
            bot_1_stage = bot_1_stage + 0.5
            if (bot_1_stage == 0.5):
                x_t[0] = x_b[0] + (30 * cos(pi / 4))
                y_t[0] = y_b[0] - (30 * sin(pi / 4))
            if (bot_1_stage == 1.5):
                x_t[0] = x_b[0] + (30 * cos(pi / 4))
                y_t[0] = y_b[0] + (30 * sin(pi / 4))
            if (bot_1_stage == 2.5):
                x_t[0] = x_b[0] + (100 * cos(pi / 3))
                y_t[0] = y_b[0] - (100 * sin(pi / 3))
            if (bot_1_stage == 3.5):
                x_t[0] = x_b[0]
                y_t[0] = y_b[0] - 25

        if (dist([x_t[1], y_t[1]], [x_b[1], y_b[1]]) <= 10):
            send_signal_stop(2)
            bot_2_stage = bot_2_stage + 0.5
            if (bot_1_stage == 0.5):
                x_t[1] = x_b[1] + (15 * cos(pi / 4))
                y_t[1] = y_b[1] - (15 * sin(pi / 4))
            if (bot_1_stage == 1.5):
                x_t[1] = x_b[1] + 50
                y_t[1] = y_b[1]
            if (bot_1_stage == 2.5):
                x_t[1] = x_b[1] + (15 * cos(pi / 4))
                y_t[1] = y_b[1] - (15 * sin(pi / 4))
            if (bot_1_stage == 3.5):
                x_t[1] = x_b[1]
                y_t[1] = y_b[1] + 75
            if (bot_1_stage == 3.5):
                x_t[1] = x_b[1]
                y_t[1] = y_b[1] - 75

        if (bot_1_stage % 1 == 0.5):
            if (corners[0] != None):
                bot_1_slope = calc_slope(corners[0][0], corners[0][1], corners[0][2], corners[0][3])
                target_1_slope = calc_slope(x_t[0], y_t[0], x_b[0], y_b[0])
                bot_1_offset = calc_offset(target_1_slope, bot_1_slope)
                if (bot_1_offset >  1):
                    send_angle(bot_1_offset, 1)
                else:
                    bot_1_stage = bot_1_stage + 0.5
                    if (bot_1_stage != 4):
                        send_signal_start(1)

        if (bot_2_stage % 1 == 0.5):
            if (corners[0] != None):
                bot_2_slope = calc_slope(corners[1][0], corners[1][1], corners[1][2], corners[1][3])
                target_2_slope = calc_slope(x_t[1], y_t[1], x_b[1], y_b[1])
                bot_2_offset = calc_offset(target_2_slope, bot_2_slope)
                if (bot_2_offset >  1):
                    send_angle(bot_2_offset, 1)
                else:
                    bot_2_stage = bot_2_stage + 0.5
                    send_signal_start(2)
    


if __name__ == "__main__":
    main()

