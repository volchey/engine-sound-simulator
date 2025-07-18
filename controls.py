import time
import threading
from pymavlink import mavutil


def capture_input(engine, connection):
    lock = threading.Lock()
    
    missed_messages = 0
    
    i = 51
    while True:
        if i > 30:
            connection.mav.command_long_send(
                connection.target_system,
                connection.target_component,
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
                0,
                mavutil.mavlink.MAVLINK_MSG_ID_RPM, # param1: message ID
                100000, # param2: interval in microseconds (10Hz)
                0, 0, 0, 0, 0 # param3-7: unused
            )
            i = 0
            time.sleep(0.1)
            
        i += 1
        msg = connection.recv_match(type='RPM', blocking=True, timeout=0.1)
        if msg:
            missed_messages = 0
            with lock:
                engine.specific_rpm(msg.rpm1)
        else:
            missed_messages += 1
            if missed_messages > 10:
                print("Warning!!! No RPM messages received for a while")
                engine.specific_rpm(engine.idle_rpm)
                time.sleep(2)

        