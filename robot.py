#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

class Robot:
    """
    -- TEMPLATE --
    This class provides logic for moving the sensor and scrolling the bar code cards
    """

    def sensor_step(self,step_1,time_1):
        """
        Moves the sensor one step to read the next bar code value
        """
        m = ev3.MediumMotor("outA")
        m.reset()
        m.stop_action = "brake"
        m.speed_sp = step_1
        m.command = "run-forever"
        time.sleep(time_1)
        m.stop()
        

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        # implementation
        m = ev3.MediumMotor("outA")
        m.reset()
        m.stop_action = "brake"
        m.speed_sp = -240
        m.command = "run-forever"
        time.sleep(2.7)
        m.stop()

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        # implementation
        m = ev3.LargeMotor("outB")
        m.reset()
        m.stop_action = "brake"
        m.speed_sp = -47.5
        m.command = "run-forever"
        time.sleep(2)
        m.stop()

    def read_value(self) -> int:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        cs = ev3.ColorSensor()
        cs.mode = 'RGB-RAW'
        return cs.raw[0]
    
    def start_robot(self):
        """
        Starts the robot.
        """
        ts = ev3.TouchSensor()
        return ts.value()