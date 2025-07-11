import threading

def capture_input(engine, connection):
    lock = threading.Lock()
    while True:
        msg = connection.recv_match(type='RPM', blocking=True)
        if msg:
            with lock:
                engine._rpm = msg.rpm1
        