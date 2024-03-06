import numpy as np
import luca_api.Canlib_src.canalystii
import can


class Pulses:
    def __init__(self, pulses):
        if not isinstance(pulses, (int, float)):  # adjust as needed based on accepted types
            raise ValueError("Input pulses must be a number")

        # config parameter
        # pulse_threshold and their v_constant value
        self.pulse_threshold = np.array([500000, 300000], dtype=np.int32)
        self.vel_refer = np.array([2500, 500])
        self.vel_divided = 250

        # find_n_max parameter
        self.find_n_para = np.array([7.88, 1.57], dtype=float)
        # s_curve parameter
        self.mn, self.mx, self.a1, self.c1, self.a2, self.c2 = np.array([0, 6, 4, 1.5, 4, 1.5], dtype=float)

        self.pulses = pulses
        # this V is known as constant
        self.v = self.find_v_from_pulses()
        self.n = self.find_n()

    def find_v_from_pulses(self):
        """
        Return the velocity from given pulses
        :return: constant velocity
        :rtype: float
        """
        val = abs(self.pulses)

        # for each pulse there will be different values of constant Vec defined
        match val:
            case _ if val >= self.pulse_threshold[0]:
                v_constant = self.vel_refer[0]

            case _ if 0 < val <= self.pulse_threshold[1]:
                v_constant = self.vel_refer[1]

            case _:
                v_constant = val / self.vel_divided

        return v_constant

    # TODO: add another find v_min ?, check the para of v_constant

    # def find_v_min(pulse):
    #     if abs(pulse) >= 500000:
    #         v_codinh = 1200
    #     elif 0 < abs(pulse) <= 200000:
    #         v_codinh = 600
    #     else:
    #         v_codinh = abs(pulse) / 500
    #     return v_codinh

    def find_n(self):
        """
        find the int n to match the pulses and velocity
        :param pulses: number of pulse to take rotating
        :type pulses: int
        :param v: velocity to rotate
        :type v: float
        :return: int n
        :rtype: int
        """
        n = int((abs(self.pulses) / (self.find_n_para[0] * self.v)) * self.find_n_para[1])
        return n

    def s_curve(self):
        """
        :return: the array speeds base on n and v
        """
        speeds = np.array([])
        y = []
        tong_time = 0
        total_pos = 0

        temp = (self.mx - self.mn) / self.n
        for i in range(0, int(self.n / 2)):
            temp_f = self.mn + temp * i
            y1_temp = self.v / (1 + np.exp(-self.a1 * (temp_f - self.c1)))
            y.append(y1_temp)
            speeds = np.append(speeds, y1_temp)
            tong_time += self.pulses / y1_temp
            total_pos += y1_temp * 0.0156 * 1000

        for i in range(int(self.n / 2), self.n + 1):
            temp_f = self.mn + temp * (self.n - i)
            y1_temp = self.v / (1 + np.exp(-self.a2 * (temp_f - self.c2)))
            y.append(y1_temp)
            speeds = np.append(speeds, y1_temp)
            tong_time += self.pulses / y1_temp
            total_pos += y1_temp * 0.0156 * 1000

        return speeds


def cal_speed(list_pulses):
    """
    calculate the speed from a list of Pulses object
    :param list_pulses: list of Pulses objects
    :type list_pulses: list[Pulses]
    :return: n_max and array of speeds
    """
    # TODO: Vc1 and Vc2 use findV_min_instead ?
    # Input validation

    if not all(isinstance(pulse, Pulses) for pulse in list_pulses):
        raise ValueError("All elements in list_pulses must be instances of Pulses class.")

    try:
        ns = [motor_pulse.n for motor_pulse in list_pulses]
        n_max = max(ns)

        for motor_pulse in list_pulses:
            # motor_pulse.v = (abs(motor_pulse.pulses) / (7.88 * n_max)) * 1.57
            motor_pulse.v = (abs(motor_pulse.pulses) / (motor_pulse.find_n_para[0] * n_max)) * motor_pulse.find_n_para[
                1]
            motor_pulse.n = n_max

        speeds_array = [motor_pulse.s_curve() for motor_pulse in list_pulses]

        return n_max, speeds_array

    except AttributeError:
        raise AttributeError("Ensure the Pulses object has 'n', 'v', 'pulses', 's_curve' attributes.")
    except ZeroDivisionError:
        raise ValueError("Error occurred due to division by zero, please ensure 'n_max' is not zero.")
    except Exception as e:
        raise type(e)(f"An error occurred: {str(e)}")


# array_pulse = [Pulses(pulses=x) for x in [10000, 20000, 30000, 40000, 50000, 60000]]
# n_max, speeds_array = cal_speed(array_pulse)
# print(n_max)
# print(speeds_array)


def input_pulses_from_CLI():
    """
    Prompt the user to enter the pulses for each motor via the terminal.
    :return: list of pulses
    :rtype: List[int]
    """
    num_motors = input("Enter the number of motors: ")
    # Validate the input. If it's not a number or not provided, default to 6
    if not num_motors.isnumeric():
        print("Invalid input or no input! The default of 6 motors will be used.")
        num_motors = 6
    else:
        num_motors = int(num_motors)

    pulses = []
    while len(pulses) < num_motors:
        try:
            pulse = int(input(f"Enter pulse {len(pulses) + 1}: "))
            pulses.append(pulse)
        except ValueError:
            print("Invalid input for pulse! Please enter a number.")
    return pulses

# def run_cal_speed():
#     array_pulse = [Pulses(pulse) for pulse in input_pulses_from_CLI()]
#     n_max, speeds_array = cal_speed(array_pulse)
#     print(speeds_array)
#
#
# if __name__ == "__main__":
#     run_cal_speed()
