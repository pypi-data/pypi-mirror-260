import can
import numpy as np
from luca_api.Canlib_src import canalystii
from luca_api.utils.math_processing import convert_number_and_id_to_hex_array
import time


class Luca_movement:
    def __init__(self, can_channel, number_joint):
        """
        set the movement of each motor joint
        :param can_channel:
        :param number_joint:
        :type number_joint: int
        """

        self.joints = []
        self.current_angles = []
        self.current_poses = []
        self.full_pulse = int(3342336)
        self.bitrate = int(1000000)
        self.bus = bus  # considering this CAREFULLY !

        for i in range(1, number_joint + 1):
            joint = canalystii.CANalystIIBus(channel=can_channel, device=i, bitrate=self.bitrate)
            self.joints.append(joint)
            current_pos, current_angle = self.current_joint(i)
            self.current_angles.append(current_angle)
            self.current_poses.append(current_pos)
            time.sleep(0.02)

    def current_joints(self, joint_number):
        """
        return the current angle and poses of a joint
        :param joint_number: the ID of joint
        :type joint_number: int
        :return:
        """
        try:
            can_frame = can.Message(arbitration_id=joint_number, data=[0x41], is_extended_id=False, dlc=1)
            self.joints[joint_number - 1].send(can_frame)
            msg = self.joints[joint_number - 1].recv()
            byte_array = msg.data

            if msg.arbitration_id == joint_number:
                number_pos = byte_array[4:8]
                self.current_poses[joint_number - 1] = int.from_bytes(number_pos, byteorder='little', signed=True)
                self.current_angles[joint_number - 1] = round(
                    self.current_poses[joint_number - 1] * 360 / self.full_pulse, 2)

            return self.current_poses[joint_number - 1], self.current_angles[joint_number - 1]

        except Exception as e:
            print(f"Error reading joint {joint_number}: ", str(e))
            raise e

    def current_forward_speeed(self, joint_number):
        """
        Return the current forward speed of a joint
        :param joint_number: The ID of joint
        :type joint_number: int
        :return: current speed of the joint
        """
        try:
            can_frame = can.Message(arbitration_id=joint_number, data=[0x18], is_extended_id=False, dlc=1)
            self.joints[joint_number - 1].send(can_frame)
            msg = self.joints[joint_number - 1].recv()
            byte_array = msg.data

            if msg.arbitration_id == joint_number:
                number_pos = byte_array[1:3]
                current_speed = int.from_bytes(number_pos, byteorder='little', signed=True)

            else:
                current_speed = 0

            return current_speed

        except Exception as e:
            print(f"Error getting current speed for joint {joint_number}: ", str(e))
            raise e

    def current_reverse_speed(self, joint_number):
        """
        Return the current reverse speed of a joint
        :param joint_number: The ID of joint
        :type joint_number: int
        :return: current speed of the joint
        """
        try:
            can_frame = can.Message(arbitration_id=joint_number, data=[0x19], is_extended_id=False, dlc=1)
            self.joints[joint_number - 1].send(can_frame)
            msg = self.joints[joint_number - 1].recv()
            byte_array = msg.data

            if msg.arbitration_id == joint_number:
                number1 = byte_array[1:3]
                current_speed = int.from_bytes(number1, byteorder='little', signed=True)
            else:
                current_speed = 0
            return current_speed

        except Exception as e:
            print(f"Error getting current reverse speed for joint {joint_number}: ", str(e))
            raise e

    def joint_forward(self, joint_number, degrees):
        """
        Move a joint forward by a certain number of degrees
        :param joint_number: The ID of joint
        :param degrees: The number of degrees to move the joint ( in deg)
        """
        try:
            new_angle = self.current_angles[joint_number - 1] + degrees
            new_pos = int(new_angle * self.full_pulse / 360)
            mess_id = '0x44'
            mess_data = convert_number_and_id_to_hex_array(new_pos, mess_id)
            can_frame = can.Message(arbitration_id=joint_number, data=mess_data, is_extended_id=False, dlc=5)
            self.joints[joint_number - 1].send(can_frame)

        except Exception as e:
            print(f"Error moving joint {joint_number} forward: ", str(e))
            raise e

    def joint_reverse(self, joint_number, degrees):
        """
        Move a joint in reverse by a certain number of degrees
        :param joint_number: The ID of joint
        :param degrees: The number of degrees to move the joint in reverse
        :type joint_number: int
        :type degrees: int
        """
        try:
            new_angle = self.current_angles[joint_number - 1] - degrees
            new_pos = int(new_angle * 3342336 / 360)
            mess_id = '0x44'
            mess_data = convert_number_and_id_to_hex_array(new_pos, mess_id)
            can_frame = can.Message(arbitration_id=joint_number, data=mess_data, is_extended_id=False, dlc=5)
            self.joints[joint_number - 1].send(can_frame)

        except Exception as e:
            print(f"Error moving joint {joint_number} in reverse: ", str(e))
            raise e

    def set_offset(self, joint_number):
        """
        Sets the offset for a joint if the current angle is not 0
        :param joint_number: The ID of joint
        :type joint_number: int
        """
        try:
            if self.current_angles[joint_number - 1] != 0:
                mess_data = convert_number_and_id_to_hex_array(self.current_angles[joint_number - 1], '0x53')
                can_frame = can.Message(arbitration_id=joint_number, data=mess_data, is_extended_id=False, dlc=5)
                self.joints[joint_number - 1].send(can_frame)

        except Exception as e:
            print(f"Error setting offset for joint {joint_number}: ", str(e))
            raise e

    def open_hand(self):
        try:
            can_frame = can.Message(arbitration_id=10, data=[0x28], is_extended_id=False, dlc=1)
            self.bus.send(can_frame)
        except can.CanError:
            print('Error: Failed to send CAN frame in open_hand method')
            return False
        return True

    def close_hand(self):
        try:
            can_frame = can.Message(arbitration_id=10, data=[0x1E], is_extended_id=False, dlc=1)
            self.bus.send(can_frame)
        except can.CanError:
            print('Error: Failed to send CAN frame in close_hand method')
            return False
        return True
