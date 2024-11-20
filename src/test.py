import time
import pwmio
import board
solenoid_pwm = pwmio.PWMOut(board.GP18, frequency=1000000, duty_cycle=0)
def set_solenoid(state, full_power_duration=0.01, start_duty_cycle = 65535, transition_duration=0.5, end_duty_cycle = 5000, steps=50):
  if state:
    solenoid_pwm.duty_cycle = start_duty_cycle
    time.sleep(full_power_duration)  # Non-blocking sleep for full power duration
    for step in range(steps + 1):
      current_duty_cycle = start_duty_cycle - int((start_duty_cycle - end_duty_cycle) * step / steps)
      solenoid_pwm.duty_cycle = current_duty_cycle
      time.sleep(transition_duration / steps)
    solenoid_pwm.duty_cycle = end_duty_cycle
  else:
    for step in range(steps + 1):
      current_duty_cycle = start_duty_cycle - int((start_duty_cycle - end_duty_cycle) * step / steps)
      solenoid_pwm.duty_cycle = current_duty_cycle
      time.sleep(transition_duration / steps)
    solenoid_pwm.duty_cycle = end_duty_cycle
set_solenoid(state = 0, full_power_duration=0.0, start_duty_cycle=6000, transition_duration=0.5, end_duty_cycle=0, steps=10)
set_solenoid(state = 1, full_power_duration=0.1, start_duty_cycle=65535, transition_duration=0.5, end_duty_cycle=6000, steps=10)
