import numpy as np
import math
from math import cos, sin, radians, pi
from scipy.spatial.transform import Rotation
import torch


def convert_number_and_id_to_hex_array(number, id):
    """
    Convert a int numbers of pulses and Hex id-represent for action to an array
    :param number: numbers of pulses motors need to rotate
    :type number: int
    :param id: the Hexa id of the action get/set for motors, like 0x44
    :type id: str
    :return: an array holds the value int of id and numbers of pulses
    :rtype: list of int
    Example:
        num = 100000, id = 0x44
        return [68, 160, 134, 1, 0]
        68 is int of 0x44, then [160, 134, 1, 0] is the int array from the 4 bytes xa0-x86-x01-x00 comes from 100k
        (LSB is xa0-160)

    """
    try:
        # convert int number to 4 bytes from the LSB to MSB
        byte_array = number.to_bytes(4, byteorder='little', signed=True)

        # convert each Hex value to int
        hex_to_int_array = [int(hex(byte), 16) for byte in byte_array]

        # add the int value of number at the start of array
        hex_to_int_array.insert(0, int(id, 16))

        return hex_to_int_array

    except AttributeError:
        print("Error: number must be an integer.")
    except ValueError:
        print("Error: id must be a hexadecimal string in format '0x..'.")
    except TypeError:
        print("Error: number must be an integer, id must be a string.")
    return None


def sign_fc(pos):
    """
    1 if pos >=0 else -1
    :param pos: int number
    :type pos: int
    :return: -1 or 1
    """
    try:
        return 1 if pos >= 0 else -1

    except TypeError:
        print('Error: Pos must be a number')
        return None


def find_max(m1, m2, m3, m4, m5, m6):
    """
    find the max parameter of motor 1 to 6
    :return: max value
    """
    return max(m1, m2, m3, m4, m5, m6)


def matrix_to_quaternion(matrix):
    # Trích xuất ma trận xoay từ ma trận 4x4
    rotation_matrix = matrix[:3, :3]

    rotation = Rotation.from_matrix(rotation_matrix)
    qw, qx, qy, qz = rotation.as_quat()

    return qw, qx, qy, qz


def Dof_6(theta1_deg, theta2_deg, theta3_deg, theta4_deg, theta5_deg, theta6_deg):
    a = [25, -25, -20, -20, 0, 0]
    d = [89.75, 0, 148.6, 0, 106, 0]

    theta = [radians(theta1_deg),
             radians(theta2_deg),
             -radians(theta3_deg) + pi,
             radians(theta4_deg) + pi / 2,
             -radians(theta5_deg),
             -radians(theta6_deg)]

    alpha = [radians(-90), radians(90), radians(-90), radians(-90), radians(-90), radians(90)]

    T_t1 = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 145.5],
                     [0, 0, 0, 1]])

    T_t2 = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 150],
                     [0, 0, 0, 1]])

    world_frame_bip = np.array([[cos(pi / 3), 0, sin(pi / 3), 123.53],
                                [0, 1, 0, 10],
                                [-sin(pi / 3), 0, cos(pi / 3), 528.12],
                                [0, 0, 0, 1]])

    def get_transform_matrix(theta, alpha, a, d):
        return np.array([[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
                         [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
                         [0, sin(alpha), cos(alpha), d],
                         [0, 0, 0, 1]])

    T = [get_transform_matrix(theta[i], alpha[i], a[i], d[i]) for i in range(6)]

    TC = np.linalg.multi_dot([world_frame_bip, T[0], T[1], T_t1, T[2], T[3], T_t2, T[4], T[5]])

    px = - TC[0][3]
    py = - TC[1][3]
    pz = TC[2][3]

    return np.array([px, py, pz], dtype=np.float32)


