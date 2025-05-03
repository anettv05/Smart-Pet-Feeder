# gpio_helper.py â€ run with system Python: sudo python3 gpio_helper.py
# gpio_helper.py â€ run with system Python: sudo python3 gpio_helper.py
import time
import subprocess
from gpiozero import AngularServo, Device
from gpiozero.pins.pigpio import PiGPIOFactory


# Configuration
SERVO_PIN = 18
FEED_INTERVAL = 20  # 20 seconds

# Initialize AngularServo
servo = AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
initial_angle = 0
last_feed_time = 0

def set_angle(angle):
    servo.angle = angle
    time.sleep(1)

def feed_pet():
    print("Feeding pet...")
    global initial_angle
    set_angle(60)
    time.sleep(2)
    set_angle(0)
    time.sleep(1)


 
servo.detach()
def detect_pet_with_venv(width=640, height=480):
    command = [
        "libcamera-vid", "--width", str(width), "--height", str(height),
        "--framerate", "15", "--codec", "yuv420", "-o", "-", "-t", "0"
    ]
    cam_proc = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)

    try:
        detect_proc = subprocess.Popen(
            ["/home/pi/Desktop/cv-env/bin/python3", "/home/pi/Desktop/petfeeder.py"],
            stdin=cam_proc.stdout,
            stdout=subprocess.PIPE
        )

        for line in detect_proc.stdout:
            if line.decode().strip() == "PET":
                detect_proc.terminate()
                cam_proc.terminate()
                return True

        detect_proc.terminate()
        cam_proc.terminate()
        return False

    except Exception as e:
        cam_proc.terminate()
        print(f"Error during detection: {e}")
        return False

try:
    while True:
        print("Checking for pet...")
        pet_here = detect_pet_with_venv()
        if pet_here:
            print("Pet detected.")
            if time.time() - last_feed_time > FEED_INTERVAL:
                feed_pet()
                servo.detach()
                last_feed_time = time.time()
            else:
                print("Feed interval not reached.")
        else:
            print("No pet detected.")
        time.sleep(2)  # Delay between checks

except KeyboardInterrupt:
    print("Exiting...")


