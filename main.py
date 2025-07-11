import controls
import engine_factory
from audio_device import AudioDevice
from pymavlink import mavutil

# MAVLink connection
master = mavutil.mavlink_connection('udp:127.0.0.1:14556')
master.wait_heartbeat()
print("Connected to MAVLink")

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
