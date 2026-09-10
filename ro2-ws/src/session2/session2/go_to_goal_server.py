import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool


class Go_to_goal_server(Node):

    def __init__(self):
        super().__init__("go_to_goal_server")
        # ---- 1. DECLARE ----
        self.declare_parameter('target_x', 5.5)
        self.declare_parameter('target_y', 5.5)
        self.declare_parameter('linear_gain', 1.0)
        self.declare_parameter('angular_gain', 2.0)
        self.declare_parameter('distance_tolerance', 0.1)
        self.declare_parameter('angle_tolerance', 0.1)
        self.declare_parameter('loop_rate_hz', 10.0)

        # ---- 2. READ (once) ----
        self.target_x     = self.get_parameter('target_x').value
        self.target_y     = self.get_parameter('target_y').value
        self.linear_gain  = self.get_parameter('linear_gain').value
        self.angular_gain = self.get_parameter('angular_gain').value
        self.dist_tol     = self.get_parameter('distance_tolerance').value
        self.angle_tol    = self.get_parameter('angle_tolerance').value
        self.rate_hz      = self.get_parameter('loop_rate_hz').value

        # Publisher: sends velocity commands to the turtle
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.moving_active = False

        self.cmd_vel_pub = self.create_publisher(
            Twist,
            "/turtle1/cmd_vel",
            10
        )

        # Subscriber: receives the turtle's current position
        self.pose_sub = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.pose_callback,
            10
        )
        #create service server 
        self.srv = self.create_service(
            SetBool,
            'toggle_movement',
            self.handle_toggle
        )

        # Run the control loop every 0.05 seconds
        self.timer = self.create_timer(
            1.0/self.rate_hz,
            self.control_loop
        )
    def handle_toggle(self, request, response):
        #only flip the flag 
        self.moving_active = request.data
        response.success = True
        response.message = f"movement {'enabled' if request.data else 'disabled'}"
        self.get_logger().info(f"[service] {response.message}")
        return response
     
    def pose_callback(self, msg):
        # Store the latest turtle position
        self.current_x = msg.x
        self.current_y=msg.y
        self.current_theta=msg.theta

    def control_loop(self):

        # Difference between target and current position
        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y

        # Distance to the target
        distance = math.sqrt(dx * dx + dy * dy)

        # Angle the turtle should face
        desired_angle = math.atan2(dy, dx)

        # Difference between desired and current angle
        # atan2(sin(), cos()) keeps the error between -pi and pi
        angle_error = math.atan2(
            math.sin(desired_angle - self.current_theta),
            math.cos(desired_angle - self.current_theta)
        )

        # Create velocity message
        msg = Twist()

        if not self.moving_active:
            self.cmd_vel_pub.publish(msg)   # zero velocity → turtle stops
            return

        if abs(angle_error) > self.angle_tol:
            msg.angular.z= self.angular_gain * angle_error
            msg.linear.x=0.0
        elif distance > self.dist_tol:
            msg.linear.x=self.linear_gain * distance 
            msg.angular.z=self.angular_gain* angle_error  

        else :
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.get_logger().info('target reached!')
            self.moving_active = False  #stop trying

        self.cmd_vel_pub.publish(msg)   


def main():
    rclpy.init()

    node = Go_to_goal_server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()