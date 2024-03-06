import can
import numpy as np
from luca_api.Canlib_src import canalystii
from luca_api.Canlib_src.Can_control import Can_control_multi
from luca_api.Velocity.vec_and_pulse import Pulses
from luca_api.utils.math_processing import convert_number_and_id_to_hex_array, sign_fc
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

        self.max_pos = 2000000
        self.min_pos = 0

        self.max_speed = 1200
        self.min_speed = 50

        for i in range(1, number_joint + 1):
            joint = canalystii.CANalystIIBus(channel=can_channel, device=i, bitrate=self.bitrate)

            current_angle = 0
            current_pos = 0

            self.joints.append(joint)
            self.current_angles.append(current_angle)
            self.current_poses.append(current_pos)
            time.sleep(0.02)

    def map_values(self, value):
        return ((value - self.min_pos) / (self.max_pos - self.min_pos)) * (
                self.max_speed - self.min_speed) + self.min_speed

    def move_home_fc(self):
        """
        send all pulses to 0 to go back HOME
        :return:
        """
        # TODO: consider using this: target_pulses = [0] * len(self.joints), and checking that "for"
        target_home_pulse = [0] * 6

        multi_home = Can_control_multi(self.joints)
        multi_home.speedy_move(target_pulses=target_home_pulse)

        time.sleep(1)  # consider remove this

        for i in range(len(self.joints)):
            self.current_poses[i], self.current_angles[i] = self.current_joints(i + 1)

    # def start_all_fc(self):

    def current_joints(self, joint_number):
        """
        return the current angle and pos of a joint
        :param joint_number: the ID of joint
        :type joint_number: int
        :return:
        """
        try:
            can_frame = can.Message(arbitration_id=joint_number, data=[0x41], is_extended_id=False, dlc=1)
            self.joints[joint_number - 1].send(can_frame)
            msg = self.joints[joint_number - 1].recv()
            byte_array = msg.data
            self.joints[joint_number - 1].flush_tx_buffer()

            if msg.arbitration_id == joint_number:
                number_pos = byte_array[4:8]
                self.current_poses[joint_number - 1] = int.from_bytes(number_pos, byteorder='little', signed=True)
                self.current_angles[joint_number - 1] = round(
                    self.current_poses[joint_number - 1] * 360 / self.full_pulse, 2)

            return self.current_poses[joint_number - 1], self.current_angles[joint_number - 1]
        #TODO need return or not ?

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

    def joint_rotate(self, joint_number, degrees):
        """
        Rotate a joint by a certain number of degrees
        :param joint_number: The ID of joint
        :param degrees: The number of degrees to move the joint ( in deg)
        """
        try:
            bus_number = self.joints[joint_number - 1]
            device_id = joint_number

            new_angle = self.current_angles[joint_number - 1] + degrees
            new_pos = int(new_angle * self.full_pulse / 360)
            mess_id = '0x44'
            mess_data = convert_number_and_id_to_hex_array(new_pos, mess_id)
            can_frame = can.Message(arbitration_id=joint_number, data=mess_data, is_extended_id=False, dlc=5)

            self.joints[joint_number - 1].send(can_frame)

            new_distance = abs(new_pos - self.current_poses[joint_number - 1])
            new_direction = sign_fc(new_pos - self.current_poses[joint_number - 1])

            speed_time = Pulses.s_curve(new_distance)

            for new_speed in speed_time:
                if new_direction == 1:
                    speed_data = convert_number_and_id_to_hex_array(int(new_speed * new_direction), '0x24')
                    can_speed = can.Message(arbitration_id=device_id, data=speed_data, is_extended_id=False, dlc=5)
                    bus_number.send(can_speed)
                    time.sleep(0.0001)

                else:
                    speed_data = convert_number_and_id_to_hex_array(int(new_speed * new_direction), '0x25')
                    bus_number.send(can_speed)
                    time.sleep(0.0001)

            bus_number.flush_tx_buffer()


        except Exception as e:
            print(f"Error moving joint {joint_number} forward: ", str(e))
            raise e

    # def joint_reverse(self, joint_number, degrees):
    #     """
    #     Move a joint in reverse by a certain number of degrees
    #     :param joint_number: The ID of joint
    #     :param degrees: The number of degrees to move the joint in reverse
    #     """
    #     try:
    #         new_angle = self.current_angles[joint_number - 1] - degrees
    #         new_pos = int(new_angle * self.full_pulse / 360)
    #         mess_id = '0x44'
    #         mess_data = convert_number_and_id_to_hex_array(new_pos, mess_id)
    #         can_frame = can.Message(arbitration_id=joint_number, data=mess_data, is_extended_id=False, dlc=5)
    #         self.joints[joint_number - 1].send(can_frame)
    #
    #     except Exception as e:
    #         print(f"Error moving joint {joint_number} in reverse: ", str(e))
    #         raise e

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
