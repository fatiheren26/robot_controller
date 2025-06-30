import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

#bende from tf_transformations import euler_from_quaternion kodu sikinti cikardigi icin kendi fonksiyonumu yazdim
def euler_from_quaternion(x, y, z, w):
    #Quaternion'dan (x, y, z, w) Euler açılarına (roll, pitch, yaw) dönüşüm.
    
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z

class GoalMover(Node):
    def __init__(self):
        super().__init__('goal_mover')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.target_x = 0.0
        self.target_y = -0.5
        self.position_tolerance = 0.05
        self.angle_tolerance = 0.1  # radyan cinsinden, ~5.7 derece

        self.current_x = 0.0
        self.current_y = 0.0
        self.yaw = 0.0  # robotun yönü (açı)

        self.reached_goal = False
        self.timer = self.create_timer(0.1, self.move_to_goal)

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Quaternion'dan Euler açıya dönüşüm (yaw almak için)
        orientation_q = msg.pose.pose.orientation
        quaternion = (
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        )
        _, _, self.yaw = euler_from_quaternion(*quaternion)

        # Konumu terminale yazdır
        self.get_logger().info(
            f"Current Position → x: {self.current_x:.2f}, y: {self.current_y:.2f}, yaw: {math.degrees(self.yaw):.1f}°"
        )



    def move_to_goal(self):
        if self.reached_goal:
            return

        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        distance = math.sqrt(dx**2 + dy**2)
        angle_to_target = math.atan2(dy, dx)
        angle_diff = self.normalize_angle(angle_to_target - self.yaw)

        twist = Twist()

        if distance > self.position_tolerance:
            # Önce yönü düzelt
            if abs(angle_diff) > self.angle_tolerance:
                twist.angular.z = 0.4 * angle_diff  # yön düzeltme
                twist.linear.x = 0.0
            else:
                twist.linear.x = 0.2  # ileri git
                twist.angular.z = 0.0
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.reached_goal = True
            self.get_logger().info("Reached the goal and stopped.")

        self.publisher.publish(twist)

    def normalize_angle(self, angle):
        # Açıyı -pi ile pi arasına getirir
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle


def main(args=None):
    rclpy.init(args=args)
    node = GoalMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
