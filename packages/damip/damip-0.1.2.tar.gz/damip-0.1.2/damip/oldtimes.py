#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02 28 00:58:20 2024

@project: damip
@author : kaiwei.li
@company: Digitopia Robotics Ltd.,Co.
"""

import sys
import os
import time
import json
import serial

class robot:

    __uart_dev= "/dev/ttyS3"
    __baudrate = 1000000 #(9600,19200,38400,57600,115200,921600)
    __serial_delay = 1 #delay seconds for serial

    name = "Oldtimes"

    try:
        __ser = serial.Serial(__uart_dev, int(__baudrate), timeout=2) # timeout
    except Exception as e:
        print(":) Open serial failed!\n")
    
    def __init__(self):
        self.name = "Oldtimes"

    def hello(self):
        return('hello, I am an Oldtimes robot, My name is ' + self.name + ".")

    # Initial by serial
    def init(self):
        self.__serial_buffer_clear()
        self.__wifi_close()
        self.head_postion(300)
        self.right_arm_postion(500)
        self.left_arm_postion(500)
        
    # Close wifi by serial
    def __wifi_close(self):
        try:
            cmd_wifi_off = "{\"T\":66}"
            write_num = self.__ser.write(cmd_wifi_off.encode('UTF-8'))
            print(":) Send: ", str(cmd_wifi_off), str(write_num))
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Closed wifi\n")
        return

    # Open serial
    def __serial_open(self):
        try:
            __ser = serial.Serial(__uart_dev, int(__baudrate), timeout=2) # timeout
        except Exception as e:
            print(":) Open serial failed!\n")
    
    # Close serial
    def __serial_close(self):
        try:
            self.__ser.close()
        except Exception as e:
            print(":) Close serial failed!\n")
        return

    # Set head postion by serial
    def head_postion(self, value):
        try:
            cmd_neck_pos = "{\"T\":50,\"id\":6,\"pos\":" + str(value) + ",\"spd\":240,\"acc\":30}"
            #print(cmd_neck_pos)
            write_num = self.__ser.write(cmd_neck_pos.encode('UTF-8'))
            print(":) Send: ", str(cmd_neck_pos), str(write_num))
            #delay
            time.sleep(self.__serial_delay)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Set head postion: ", value)
        return

    # Shake head by serial
    def head_shake(self, value):
        if value < 0 or value > 100:
            print(":) head shake value not support, value should be in 0~100.")
            return
        postion_m = 300
        postion_a = postion_m - 100 * value
        postion_b = postion_m + 100 * value
        self.head_postion(postion_a)
        self.head_postion(postion_b)
        self.head_postion(postion_m)
        return

    # Set right arm postion by serial
    def right_arm_postion(self, value):
        try:
            cmd_arm_pos = "{\"T\":50,\"id\":2,\"pos\":" + str(value) + ",\"spd\":500,\"acc\":30}"
            #print(cmd_arm_pos)
            write_num = self.__ser.write(cmd_arm_pos.encode('UTF-8'))
            print(":) Send: ", str(cmd_arm_pos), str(write_num))
            #delay
            time.sleep(self.__serial_delay)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Set right arm postion: ", value)
        return

    # Shake right arm by serial
    def right_arm_shake(self, value):
        if value < 0 or value > 100:
            print(":) arm shake value not support, value should be in 0~100.")
            return
        postion_m = 500
        postion_a = postion_m - 200 * value
        postion_b = postion_m + 200 * value
        self.right_arm_postion(postion_a)
        self.right_arm_postion(postion_b)
        self.right_arm_postion(postion_m)
        return

    # Set left arm postion by serial
    def left_arm_postion(self, value):
        try:
            cmd_arm_pos = "{\"T\":50,\"id\":8,\"pos\":" + str(value) + ",\"spd\":500,\"acc\":30}"
            #print(cmd_arm_pos)
            write_num = self.__ser.write(cmd_arm_pos.encode('UTF-8'))
            print(":) Send: ", str(cmd_arm_pos), str(write_num))
            #delay
            time.sleep(self.__serial_delay)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Set left arm postion: ", value)
        return

    # Shake left arm by serial
    def left_arm_shake(self, value):
        if value < 0 or value > 100:
            print(":) left arm shake value not support, value should be in 0~100.")
            return
        postion_m = 500
        postion_a = postion_m - 200 * value
        postion_b = postion_m + 200 * value
        self.left_arm_postion(postion_a)
        self.left_arm_postion(postion_b)
        self.left_arm_postion(postion_m)
        return

    # Clear serial read buffer
    def __serial_buffer_clear(self):
        try:
            received_data = self.__ser.read_all().decode('UTF-8')
            print(":) Recv: ", received_data)
            received_data = self.__ser.read_all().decode('UTF-8')
            print(":) Recv: ", received_data)
            received_data = self.__ser.read_all().decode('UTF-8')
            print(":) Recv: ", received_data)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Cleared serial read buffer\n")
        return

    # Get battery percentage
    def battery_status(self):
        try:
            cmd_vol_get = "{\"T\":70}"
            write_num = self.__ser.write(cmd_vol_get.encode('UTF-8'))
            print(":) Send: ", str(cmd_vol_get), str(write_num))
            time.sleep(self.__serial_delay)
            received_data_vol = self.__ser.read_all().decode('UTF-8')
            print(":) Recv: ", received_data_vol)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Get battery voltage\n")
        
        json_data = json.loads(received_data_vol)
        bus_v = json_data['bus_V']

        BUS_FULL_VOL = 12.324
        bat_p = round((bus_v / BUS_FULL_VOL) * 100, 2)
        print(":) battery info:", str(bat_p), "%\n")
        return(str(json_data))

    # Get servo info
    def servo_status(self, number):
        try:
            cmd_get_servo = "{\"T\":53,\"id\":" + str(number) + "}"
            write_num = self.__ser.write(cmd_get_servo.encode('UTF-8'))
            print(":) Send: ", str(cmd_get_servo), str(write_num))
            time.sleep(self.__serial_delay)
            cmd_get_servo = self.__ser.read_all().decode('UTF-8')
            print(":) Recv: ", cmd_get_servo)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Get servo info\n")
        
        if len(cmd_get_servo) != 0:
            json_data = json.loads(cmd_get_servo)
            pos = json_data['pos']
            volt = json_data['volt']
            temp = json_data['temp']
        else:
            print(":) Recv length is zero, bypass\n")
        return(str(json_data))

    # Get stance status
    def stance_status(self):
        try:
            cmd_stance_get = "{\"T\":71}"
            write_num = self.__ser.write(cmd_stance_get.encode('UTF-8'))
            print(":) Send: ", str(cmd_stance_get), str(write_num))
            time.sleep(self.__serial_delay)
            received_data_stance = self.__ser.read_all().decode('UTF-8')
            print(":) Recv: ", received_data_stance)
        except serial.SerialException as e:
            print(f"SerialException: {e}")
        except serial.SerialTimeoutException as e:
            print(f"SerialTimeoutException: {e}")
        finally:
            print(":) Get stance status\n")
        
        json_data = json.loads(received_data_stance)
        
        temp = json_data['temp']

        roll = json_data['roll']
        pitch = json_data['pitch']
        yaw = json_data['yaw']
        
        acce_X = json_data['acce_X']
        acce_Y = json_data['acce_Y']
        acce_Z = json_data['acce_Z']

        gyro_X = json_data['gyro_X']
        gyro_Y = json_data['gyro_Y']
        gyro_Z = json_data['gyro_Z']

        magn_X = json_data['magn_X']
        magn_Y = json_data['magn_Y']
        magn_Z = json_data['magn_Z']

        print(":) acceleration info:", str(acce_X), "/", str(acce_Y), "/", str(acce_Z), "\n")
        print(":) gyroscope info:", str(gyro_X), "/", str(gyro_Y), "/", str(gyro_Z), "\n")
        print(":) magnetic field info:", str(magn_X), "/", str(magn_Y), "/", str(magn_Z), "\n")
        return(str(json_data))