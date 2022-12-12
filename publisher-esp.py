import socket  # for communicating with the broker
import time
from robotic_arm import RoboticArm


# Communication constants
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 8000
BUFFER_SIZE = 4096

# Message constants
ACK = "ACK"
FORMAT = "utf-8"
SEPERATOR = "$"


def __generate_data_for_topic(topic: str, working_time: int, temperature: float, rpm: float):
    return [working_time, temperature, rpm]


def __generate_publish_message(topic: str = "default", data_array: list = []):
    return SEPERATOR.join(["PUB", topic_name, str(data)])


if __name__ == "__main__":
    # Create a UDP socket (Datagram)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Create a tuple consists server address and server port
    broker_addr = (BROKER_HOST, BROKER_PORT)

    robot = RoboticArm()
    target_temperature = RoboticArm.optimum_temperature

    topic_name = "robotic_arm_1"

    while robot.working_time < 1000:
        robot.work_one_step()
        robot.get_feedback_and_act()
        robot.make_noise()
        robot.increase_one_unit_time()

        print("Robot Time -> {}".format(robot.working_time))
        print("Robot Temp. -> {}".format(robot.temperature))
        print("Robot RPM. -> {}".format(robot.rpm))
        time.sleep(0.005)

        data = __generate_data_for_topic(topic_name, robot.working_time, robot.temperature, robot.rpm)
        message = __generate_publish_message(topic_name, data)

        client.sendto(message.encode(FORMAT), broker_addr)
        print("Data published to the topic \'{}\'".format(topic_name))

        raw_ack, _ = client.recvfrom(BUFFER_SIZE)
        ack = raw_ack.decode(FORMAT)

        if ack.lower() == "ack":
            print("Publish-ACK is received")
        print("------------------")
