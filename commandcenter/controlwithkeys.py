import sys
import rospy
from std_msgs.msg import Int16
import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get(pub):
        inkey = _Getch()
        command = 0
        r = rospy.Rate(3)
        while(not rospy.is_shutdown()):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                print("forward")
                command = 1
        elif k=='\x1b[B':
                print("backward")
                command = 2
        elif k=='\x1b[C':
                print("right")
                command = 3
        elif k=='\x1b[D':
                print("left")
                command = 4
        else:
                print("stop")
                command = 0
        # Publish Command
        pub.publish(command)
        r.sleep()
def main():
    try:
        rospy.init_node('RC_CommandsPub', anonymous=True)
        pub = rospy.Publisher('RC_Command', Int16, queue_size=10)
        #r = rospy.Rate(3) # 3hz
        while not rospy.is_shutdown():
            get(pub)
    except(KeyboardInterrupt,SystemExit):
        print("---- Exiting ----")

if __name__=='__main__':
        main()
