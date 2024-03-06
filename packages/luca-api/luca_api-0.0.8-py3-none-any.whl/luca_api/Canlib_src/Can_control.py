import time
from luca_api.Canlib_src import canalystii
# import canalystii
import can
from luca_api.utils.math_processing import convert_number_and_id_to_hex_array, sign_fc
from luca_api.Velocity.vec_and_pulse import cal_speed
import logging


class Can_control_single:
    """
    about the send/get data through Canbus for 1 motor
    """

    def __init__(self, bus, id):
        """
        Initialize the motor controller.
        :param bus: The bus object through which to communicate.
        :param id: The ID of the motor.
        """
        self.bus = bus
        self.id = id
        self.current_pos = read_pos(self.bus, self.id)

    def read_pos(self):
        """
        read the position from the bus and id for get current, speed, pos
        """

        can_frame = can.Message(arbitration_id=self.id, data=[0x41], is_extended_id=False, dlc=1)
        try:
            self.bus.send(can_frame)
            msg = bus.recv(0.1)  # 0.1s timeout, this one might not necessary
            self.bus.flush_tx_buffer()

        except can.CanError:
            print(f"Failed to send or receive for id {self.id}")
            return None

        self.current_pos = None  # Initialize current_pos

        if msg is not None and msg.arbitration_id == self.id:
            byte_array = msg.data
            number = byte_array[4:8]
            self.current_pos = int.from_bytes(number, byteorder='little', signed=True)

        return self.current_pos

    def send_pulse(self, pulse):
        """
        send pulse by 0x44 by can_frame
        :return: CAN message command
        """
        try:
            pulse_converted = convert_number_and_id_to_hex_array(pulse, '0x44')
            can_frame = can.Message(arbitration_id=self.id, data=pulse_converted, is_extended_id=False, dlc=5)
            self.bus.send(can_frame)
        except Exception as e:
            logging.error(f"Failed to send pulse for id {self.id}. Error: {str(e)}")

    def send_speed(self, speed, direction):
        """

        :param speed: the speed output from the Velocity module
        :param direction: CW/CCW
        :return: CAN message command
        """
        try:
            speed_data_array = convert_number_and_id_to_hex_array(int(speed * direction),
                                                                  '0x24' if direction == 1 else '0x25')
            can_speed = can.Message(arbitration_id=self.id, data=speed_data_array, is_extended_id=False, dlc=5)
            self.bus.send(can_speed)
        except Exception as e:
            logging.error(f"Failed to send speed for id {self.id}. Error: {str(e)}")

    def compute_distance_and_direction(self, target_pulse):
        """
        compute the distance and direction to rotate
        :param target_pulse:
        :return: distance in pulse with signal of direction
        """
        try:
            pulse_distance = abs(target_pulse - self.current_pos)
            direction = sign_fc(target_pulse - self.current_pos)
            return pulse_distance, direction
        except Exception as e:
            logging.error(f"Failed to compute distance and direction for id {self.id}. Error: {str(e)}")
            return None, None

    def flush_buffer(self):
        self.bus.flush_tx_buffer()


class Can_control_multi:
    """
    about the send/get data through Canbus for many motor
    """

    def __init__(self, motors):
        """
        :param motors: a list of motor to control simultaneously
        """
        self.motors = motors

    def speedy_move(self, target_pulses):
        if not isinstance(target_pulses, list):
            raise TypeError("Target pulses must be a list.")

        if len(self.motors) != len(target_pulses):
            raise ValueError("The length of target pulses must match the number of motors.")

        distances = []
        directions = []
        speeds = []
        n_max = 0

        # using the control single motor class above:
        for i in range(len(self.motors)):
            distance, direction = self.motors[i].compute_distance_and_direction(target_pulses[i])
            distances.append(distance)
            directions.append(direction)
            self.motors[i].send_pulse(target_pulses[i])

        n_max, *speeds = cal_speed(*distances)

        for i in range(n_max):
            for j in range(len(self.motors)):
                self.motors[j].send_speed(speeds[j][i], directions[j])
                time.sleep(0.001)

        for motor in self.motors:
            motor.flush_buffer()


class Can_device:
    """
    Handle the loading input of many Can devices at once
    """

    def __init__(self, devices):
        self.bitrate = 1000000
        self.buses = [canalystii.CANalystIIBus(channel=0, device=devices, bitrate=self.bitrate) for device in devices]
        self.motors = [Can_control_single(bus, i + 1) for i, bus in enumerate(self.buses)]

    def get_multi_motor_controller(self):
        return Can_control_multi(self.motors)

    # EXAMPLE for testing

# if __name__ == "__main__":
#     motor_system = Can_device(devices=[1, 2, 3, 4, 5, 6])
#     multi_motor_controller = motor_system.get_multi_motor_controller()
#
#     for i in range(2):
#         multi_motor_controller.speedy_move([300000, -400000, -200000, -500000, 400000, -600000])
#         multi_motor_controller.speedy_move([300000, -100000, 1000000, -500000, 400000, -600000])
#
#     multi_motor_controller.speedy_move([0, 0, 1000000, -500000, 700000, -300000])
#
#     print("Done")
