#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time

class WallAroundTest(unittest.TestCase):
    def set_and_get(self,lf,ls,rs,rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (rf,rs,ls,lf))

        time.sleep(0.3)

        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())

        return left, right

    def test_io(self):
        left, right = self.set_and_get(60,0,0,70) #wall_front is true
        self.assertTrue(left > right,"don't curve to right")

        left, right = self.set_and_get(0,0,100,0) #too_right is true
        self.assertTrue(left < right ,"don't curve to left")

        left, right = self.set_and_get(0,100,0,0) #too_left is true
        self.assertTrue(left > right, "don't curve to right")

        left, right = self.set_and_get(5,10,10,5) # no_wall
        self.assertTrue(0 < left == right, "curve wrongly")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('test_wall_around')
    rostest.rosrun('pimouse_run_2025','test_wall_around',WallAroundTest)
