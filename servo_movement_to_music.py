import aubio            #library for analyzing music
import audio            #library for dealing with bluetooth audiofiles
import numpy as np          #library for formatting
from time import sleep          #library for working with servo motors
import pigpio           #library for working with servo motors
 
 
servo = 23          #servo Pin
 
 
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)
 
 
FORMAT = pyaudio.paFloat32
BUFFER = 1024              
CHANNELS = 2
RATE = 44100
 
 
try:
 
    p = pyaudio.PyAudio()
 
    stream = p.open(format = FORMAT, channels = CHANNELS,
                rate = RATE, input = True, frames_per_buffer = BUFFER) # opening stream with music
    tempo_o = aubio.tempo("default", 2048, 2048, RATE)
 
     
    def moving_chicken(bpm):          # function for moving the servo motor
 
        bps = bpm / 90        # this value determines for how long the motor stops after performing a turn; this makes the motor's angular velocity change depending on how slow or rapid the played song is
        pwm.set_servo_pulsewidth(servo, 500)
        time.sleep(bps)
        pwm.set_servo_pulsewidth(servo, 1250)
        time.sleep(bps)
 
 
    def beat_detected():      #function for detecting bpm
         
        beat = aubio.tempo("default", 2048, 2048, RATE)
 
        try:
            while True:
 
                data = stream.read(BUFFER)
                samples = np.frombuffer(data, dtype=np.float32)
                is_beat = tempo_o(samples)
                bpm = tempo_o.get_bpm()
                print(bpm)
                 
                if bpm > 0:
                     
                    moving_chicken(bps)
             
 
        except IOError as e:
            print("error")
             
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            pwm.set_PWM_dutycycle(servo, 0)
            pwm.set_PWM_frequency(servo, 0)
           
    beat_detected()
     
except Exception as e:
    print("error")
