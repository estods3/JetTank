#/usr/bin/env python3
from tkinter import *
import rospy
from std_msgs.msg import Int16

RCpub = rospy.Publisher('cc_remotecontrol_command', Int16, queue_size=10)
CCpub = rospy.Publisher('cc_modeselection_command', Int16, queue_size=10)

def LFCallBack():
   r = rospy.Rate(5)
   print("--------- In Line Following Mode ----------")
   CCpub.publish(1)
   r.sleep()

def WSCallBack():
   r = rospy.Rate(5)
   print("---------   In Workspace Mode    ----------")
   CCpub.publish(2)
   #RCpub.publish(command)
   r.sleep()

def RCCallBack():
   r = rospy.Rate(5)
   print("--------- In Remote Control Mode ----------")
   CCpub.publish(3)
   r.sleep()

def StopCallBack():
   r = rospy.Rate(5)
   print("---------        STOPPED         ----------")
   CCpub.publish(4)
   r.sleep()

def main():
    window = Tk()
    window.title("JetTank Command Center")
    window.geometry("330x125")
    B_LF = Button(window, text = "Line Following Mode", width = 37, command = LFCallBack)
    B_LF.place(x = 5,y = 0)
    B_WS = Button(window, text = "Workspace Mode", width = 37, command = WSCallBack)
    B_WS.place(x = 5, y = 30)
    B_RC = Button(window, text = "Remote Control Mode", width = 37, command = RCCallBack)
    B_RC.place(x = 5, y = 60)
    B_ES = Button(window, text = "STOP!", width = 37, command = StopCallBack)
    B_ES.place(x = 5, y = 90)
    window.mainloop()

if __name__ == '__main__':
    try:
        rospy.init_node('command_center', anonymous=True)
        main()
    except(KeyboardInterrupt,SystemExit):
        print("---- Exiting ----")

