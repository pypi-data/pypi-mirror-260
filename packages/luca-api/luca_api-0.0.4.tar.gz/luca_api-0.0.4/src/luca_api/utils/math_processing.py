import numpy as np
import math
from math import *
from scipy.spatial.transform import Rotation


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
    # TODO: check type of return: int or float ?

