import json  # for converting from string to list
import socket  # for communicating with the broker
import argparse  # for parsing the program argument(s)
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Communication constants
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 8000
BUFFER_SIZE = 4096

# Message constants
ACK = "ACK"
FORMAT = "utf-8"
SEPERATOR = "$"


def __generate_subscribe_message(topic_name: str = "default"):
    return SEPERATOR.join(["SUB", topic_name])


def __string_to_array(string_data: str):
    return json.loads(string_data)


if __name__ == "__main__":
    # parse input to get topic name
    parser = argparse.ArgumentParser()
    parser.add_argument("-topic", required=True, type=str)
    args = vars(parser.parse_args())
    TOPIC = args["topic"]

    # Create a UDP socket (Datagram)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    broker_addr = (BROKER_HOST, BROKER_PORT)

    # Create a subscriber message which you want to subscribe topic
    subscribe_message = __generate_subscribe_message(TOPIC)
    # Send subscriber message to server
    client.sendto(subscribe_message.encode(FORMAT), broker_addr)

    # Receive a notification message indicating that the message has been delivered from server
    raw_ack, _ = client.recvfrom(BUFFER_SIZE)
    ack = raw_ack.decode(FORMAT)

    time_array = []
    temperature_array = []
    rpm_array = []

    # Print ack
    if ack.lower() == "ack":
        print("Subscribe-ACK is received, subscribed to the topic \'{}\'".format(TOPIC))

        # Get a message from subscribed topic and print
        while True:
            # Receive message continuously (don't forget decode)
            raw_data, _ = client.recvfrom(BUFFER_SIZE)
            data = __string_to_array(raw_data.decode(FORMAT))

            working_time = data[0]
            temperature = data[1]
            rpm = data[2]

            time_array.append(working_time)
            temperature_array.append(temperature)
            rpm_array.append(rpm)

            print("[INFO]: Message received from {}".format(TOPIC))
            print("Working Time: {}".format(working_time))
            print("Temperature: {} Centigrade Degree".format(temperature))
            print("RPM Value: {}".format(rpm))
            print("-------------------------------------")

            if working_time == 1000:
                break

    client.close()

    plt.plot(time_array, temperature_array)
    plt.xlabel("time - axis")
    plt.ylabel("temperature - axis")
    plt.title("Robotic Arm - Operating Temperature Variation Characteristic")
    plt.axhline(y=75, color='r', linestyle='--')
    plt.show()


