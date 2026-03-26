#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotorWatchdog(Node):
    def __init__(self):
        super().__init__('motor_watchdog')
        # 로봇이 최종적으로 모터 드라이버로 보내는 cmd_vel 토픽 구독
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        # 같은 토픽에 0.0 속도 명령을 덮어쓰기 위해 발행
        self.pub = self.create_publisher(Twist, '/cmd_vel_watchdog', 10)
        
        # 0.1초(10Hz)마다 상태를 확인하는 타이머
        self.timer = self.create_timer(0.1, self.timer_callback) 
        self.last_cmd_time = self.get_clock().now()
        self.zero_twist = Twist()
        
        # 워치독이 스스로 발행한 0.0 명령인지 확인하기 위한 플래그
        self.is_watchdog_active = False

    def cmd_callback(self, msg):
        # 움직이라는 명령(0이 아닌 값)이 들어올 때만 타이머를 갱신합니다.
        # 이렇게 하면 워치독이 스스로 발행한 0.0 명령에 의해 타이머가 갱신되는 것을 방지합니다.
        # [수정된 부분] 임계값을 0.001에서 0.02 (2cm/s)로 상향 조정
        # 이 속도 이하면 워치독이 즉시 개입해서 모터를 완전히 꺼버립니다.
        if abs(msg.linear.x) > 0.2 or abs(msg.angular.z) > 0.2:
            self.last_cmd_time = self.get_clock().now()
            if self.is_watchdog_active:
                # self.get_logger().info("주행 명령 수신: 워치독 비활성화")
                self.is_watchdog_active = False

    def timer_callback(self):
        now = self.get_clock().now()
        # 0.5초 동안 새로운 주행 명령이 없었다면 정지 명령 발행
        if (now - self.last_cmd_time).nanoseconds > 5e8: 
            if not self.is_watchdog_active:
                # self.get_logger().warn("명령 끊김 감지! 로봇 정지 명령을 발행합니다.")
                self.is_watchdog_active = True
            
            self.pub.publish(self.zero_twist)

def main(args=None):
    rclpy.init(args=args)
    node = MotorWatchdog()
    node.get_logger().info("Motor Watchdog Started! 유령 움직임 방지 모드 활성화.")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
