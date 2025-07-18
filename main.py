import argparse
import controls
import engine_factory
from audio_device import AudioDevice
from pymavlink import mavutil

# Argument parsing
parser = argparse.ArgumentParser(
    description="Engine sound simulator. Use --mavlink to specify MAVLink connection string (e.g. udp:127.0.0.1:14556)."
)
parser.add_argument(
    "--mavlink",
    type=str,
    default="udp:127.0.0.1:14556",
    help="MAVLink connection string, e.g. udp:127.0.0.1:14556"
)
args = parser.parse_args()


# MAVLink connection
master = mavutil.mavlink_connection(args.mavlink)
master.wait_heartbeat()
print(f"Connected to MAVLink at {args.mavlink}")

engine = engine_factory.v_twin_60_deg()

audio_device = AudioDevice()
stream = audio_device.play_stream(engine.gen_audio)

print('\nEngine is running...')

try:
    controls.capture_input(engine, master) # blocks until user exits
except KeyboardInterrupt:
    pass

print('Exiting...')
stream.close()
audio_device.close()
