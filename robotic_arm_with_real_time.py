"""
OPTIMUM TEMPERATURE 75 centigrade degree
IF robot rpm >= 3000 rpm, robot heats.
ELSE robot cools down.
ROBOT starts with 25 degree and 3000 RPM.
"""

import time
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



class RoboticArm:
    optimum_temperature = 75

    def __init__(self):
        # started with 3000 rpm
        self.rpm = 3000
        # started with 25 centigrade degree
        self.temperature = 25
        # working time has started
        self.working_time = 0
        # print info
        print("\n[INFO]: Robotic ARM has started.")

    def decrease_rpm(self, value: int):
        # input value for decreasing
        # check value
        if value > self.rpm:
            print("[ERROR]: Value must not be greater than rpm of robotic arm.")
        else:
            self.rpm -= value

    def increase_rpm(self, value: int):
        # input value for increasing
        # check value
        if value + self.rpm > 3300:
            print("[ERROR]: Value must not be greater than maximum load (110% rpm).")
        else:
            self.rpm += value

    def increase_one_unit_time(self):
        self.working_time += 1

    def work_one_step(self):
        if self.rpm >= 3000:
            # HEAT
            self.temperature += 0.5 * self.rpm / 10000
        else:
            # COOL
            self.temperature += -0.5 * self.rpm / 10000
            pass

    def get_feedback_and_act(self):
        if self.temperature >= RoboticArm.optimum_temperature:
            self.decrease_rpm(100)
        elif self.rpm <= 3200:
            self.increase_rpm(100)

    def make_noise(self):
        operation = random.randint(1, 2)
        value = random.random() / 2

    #     IF operation == 1, add
        if operation == 1:
            self.temperature += value
        elif operation == 2:
            self.temperature -= value

    def __repr__(self):
        return "ROBOTIC ARM INFO\n" \
               "----------------\n" \
               "* robot rpm -> {} RPM\n" \
               "* robot temp. -> {} centigrade degree\n\n".format(self.rpm, self.temperature)


if __name__ == "__main__":
    time_array = []
    temperature_array = []

    robot = RoboticArm()
    target_temperature = RoboticArm.optimum_temperature

    fig, ax = plt.subplots()
    fig, az = plt.subplots()

    plt.plot(time_array, temperature_array)

    az.set(xlabel = "Time - axis", ylabel = "RPM - axis")
    ax.set(xlabel = "Time - axis", ylabel = "Temperature - axis")
    x = []
    y = []
    z = []
    ax.plot(x, y)
    az.plot(x, z)
    ax.set_title("Robotic Arm - Operating Temperature Variation Characteristic")
    az.set_title("Robotic Arm - Operating RPM Characteristic")
            


    while robot.working_time < 1000:
        # IF robotic arm's temperature greater than target temperature
        robot.work_one_step()
        robot.get_feedback_and_act()
        robot.make_noise()
        robot.increase_one_unit_time()

        print("Robot Time -> {}".format(robot.working_time))
        print("Robot Temp. -> {}".format(robot.temperature))
        print("------------------")
        time.sleep(0.0005)

        time_array.append(robot.working_time)
        temperature_array.append(robot.temperature)

        x.append(robot.working_time)
        y.append(robot.temperature)
        z.append(robot.rpm)

        az.plot(x, z)
        ax.plot(x, y)
        plt.pause(0.0005)

#     END OF WHILE

