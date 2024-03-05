import numpy as np
import luca_api.Canlib_src.canalystii
import can


class Pulses:
    def __init__(self, pulses):
        if not isinstance(pulses, (int, float)):  # adjust as needed based on accepted types
            raise ValueError("Input pulses must be a number")

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
            case _ if val >= 500000:
                v_constant = 2500
            case _ if 0 < val <= 100000:
                v_constant = 750
            case _ if 100000 < val <= 300000:
                v_constant = 1250
            case _:
                v_constant = val / 200
        return v_constant

    # def find_n

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
        n = int((abs(self.pulses) / (7.88 * self.v)) * 1.57)
        return n

    def s_curve(self):
        """
        :return: the array speeds base on n and v
        """
        mn = 0
        mx = 6
        a1 = 4
        c1 = 1.5
        a2 = 4
        c2 = 1.5
        speeds = np.array([])

        temp = (mx - mn) / self.n
        for i in range(0, int(self.n / 2)):
            temp_f = mn + temp * i
            y1_temp = self.v / (1 + np.exp(-a1 * (temp_f - c1)))
            speeds = np.append(speeds, y1_temp)
        for i in range(int(self.n / 2), self.n + 1):
            temp_f = mn + temp * (self.n - i)
            y1_temp = self.v / (1 + np.exp(-a2 * (temp_f - c2)))
            speeds = np.append(speeds, y1_temp)
        return speeds


def cal_speed(list_pulses):
    """
    calculate the speed from a list of Pulses object
    :param list_pulses: list of Pulses objects
    :type list_pulses: list[Pulses]
    :return: n_max and array of speeds
    """

    # Input validation
    if not all(isinstance(pulse, Pulses) for pulse in list_pulses):
        raise ValueError("All elements in list_pulses must be instances of Pulses class.")

    try:
        ns = [motor_pulse.n for motor_pulse in list_pulses]
        n_max = max(ns)

        for motor_pulse in list_pulses:
            motor_pulse.v = (abs(motor_pulse.pulses) / (7.88 * n_max)) * 1.57
            motor_pulse.n = n_max

        speeds_array = [motor_pulse.s_curve() for motor_pulse in list_pulses]

        return n_max, speeds_array

    except AttributeError:
        raise AttributeError("Ensure the Pulses object has 'n', 'v', 'pulses', 's_curve' attributes.")
    except ZeroDivisionError:
        raise ValueError("Error occurred due to division by zero, please ensure 'n_max' is not zero.")
    except Exception as e:
        raise type(e)(f"An error occurred: {str(e)}")


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


array_pulse = [Pulses(pulse) for pulse in input_pulses_from_CLI()]
n_max, speeds_array = cal_speed(array_pulse)
print(speeds_array)

# array_pulse = [Pulses(pulses=x) for x in [100000, 200000, 300000, 400000, 500000, 600000]]
# n_max, speeds_array = cal_speed(array_pulse)
# print(speeds_array)
