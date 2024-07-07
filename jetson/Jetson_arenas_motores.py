import Jetson.GPIO as GPIO
import time
import keyboard

# Define pins for the square waves (BCM numbering)
wavePin1 = 18  # Corresponds to pin 12 on the Jetson Nano header
wavePin2 = 23  # Corresponds to pin 16 on the Jetson Nano header
wavePin3 = 24  # Corresponds to pin 18 on the Jetson Nano header
switchPin = 25  # Corresponds to pin 22 on the Jetson Nano header

# Initial values for t and dc
t = 100
dc = 10

# Timing constants
spacee = 40
onTime = 50


def generate_wave(pin, on_duration, off_duration):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(on_duration / 1000.0)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(off_duration / 1000.0)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(wavePin1, GPIO.OUT)
    GPIO.setup(wavePin2, GPIO.OUT)
    GPIO.setup(wavePin3, GPIO.OUT)
    GPIO.setup(switchPin, GPIO.IN)


def loop():
    global t, dc
    while True:

       # Este if es el que define el ON/OFF general de las salidas

       # if GPIO.input(switchPin) == GPIO.HIGH:

        # Adjust t and dc based on keypresses
        if keyboard.is_pressed('w'):
            t = min(t + 30, 2000)  # Increase t
        if keyboard.is_pressed('s'):
            t = max(t - 30, 60)    # Decrease t
        if keyboard.is_pressed('a'):
            dc = min(dc + 5, 100)  # Increase duty cycle
        if keyboard.is_pressed('d'):
            dc = max(dc - 5, 10)   # Decrease duty cycle

        ton = t * dc / 100

        print(f"t: {t}\tton: {ton}\tdc: {dc}")

        generate_wave(wavePin1, ton, t - ton)
        generate_wave(wavePin2, ton, t - ton)
        generate_wave(wavePin3, ton, t - ton)


if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
