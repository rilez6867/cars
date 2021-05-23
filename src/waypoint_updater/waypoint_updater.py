#!/usr/bin/env python
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint
from scipy.spatial import KDTree
from std_msgs.msg import Int32

import math



LOOKAHEAD_WPS = 20 # Number of waypoints  published. 
MAX_DECEL = 0.5


class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')
        
         # TODO: Add other member variables you need below
        self.pose = None
        self.base_lane = None
        self.stopline_wp_idx = -1
        self.waypoints_2d = None
        self.waypoint_tree = None
        
        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below

        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)

        self.loop()
        
    def loop(self):
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            if self.pose and self.base_lane:
                self.publish_waypoints()
            rate.sleep()
            
    def get_closest_waypoint_idx(self):
        x = self.pose.pose.position.x
        y = self.pose.pose.position.y
        closest_idx = self.waypoint_tree.query([x, y], 1)[1]
        
        # Check if closest is ahead or behind vehicle
        closest_coord = self.waypoints_2d[closest_idx]
        prev_coord = self.waypoints_2d[closest_idx - 1]
        
        # Equation for hyperplane through closest_coord
        cl_vect = np.array(closest_coord)
        prev_vect = np.array(prev_coord)
        pos_vect = np.array([x, y])
        
        val = np.dot(cl_vect - prev_vect, pos_vect - cl_vect)
        
        if val > 0:
            closest_idx = (closest_idx + 1) % len(self.waypoints_2d)
        return closest_idx
        
    def publish_waypoints(self):
        final_lane = self.generate_lane()
        self.final_waypoints_pub.publish(final_lane)
        
    def generate_lane(self):
        lane = Lane()
        
        closest_idx = self.get_closest_waypoint_idx()
        farthest_idx = closest_idx + LOOKAHEAD_WPS
        base_waypoints = self.base_lane.waypoints[closest_idx:farthest_idx]
        
        if self.stopline_wp_idx == -1 or (self.stopline_wp_idx >= farthest_idx):
            lane.waypoints = base_waypoints
        else:
            lane.waypoints = self.decelerate(base_waypoints, closest_idx)
        
        return lane
        
    def decelerate(self, waypoints, closest_idx):
        """
        Decelerate waypoints.
        Args:
          waypoints: list of (sliced) waypoints
          closest_idx: closest waypoint index of self
        Returns:
          new list of decelerated waypoints
        """
        # determine waypoint index for stopping in front of red light stopline
        stop_idx = max(self.stopline_wp_idx - closest_idx - 4, 0)

        # if self.distance(waypoints, closest_idx, stop_idx) > 50:
        #    return waypoints

        # vstart = self.get_waypoint_velocity(waypoints[0])
        vstart = self.stopline_wp_idx
        D = vstart / (2 * math.pi * MAX_DECEL)

        # calculate the required distance to slowe down based on current speed
        brakedist = math.pi * math.pi * D
        distcur = self.distance(waypoints, 0, stop_idx)

        rospy.loginfo("WPU brakedist= %d curdist= %d v= %d D= %d", brakedist, distcur, vstart, D)

        # if we aren't within slow down distance, return the original waypoints
        if distcur >= brakedist:
            rospy.loginfo("WPU no decel") # %d / %d   v=%d", brakedist, distcur, vstart)
            return waypoints

        temp = []
        for i, wp in enumerate(waypoints):

            p = Waypoint()
            p.pose = wp.pose

            dist = self.distance(waypoints, i, stop_idx)
            #vel = math.sqrt(2 * MAX_DECEL * dist)
            vel = 0.5 * self.get_waypoint_velocity(wp) * (1 - math.cos( dist/math.pi / D))

            if vel < 1.:
                vel = 0

#            p.twist.twist.linear.x = min(vel, wp.twist.twist.linear.x)
            p.twist.twist.linear.x = vel
            temp.append(p)

        return temp

    def cross_track_error(self, closest_idx):
        if (closest_idx > len(self.waypoints_2d)-2):
            return 0
        
        x0 = self.pose.pose.position.x
        y0 = self.pose.pose.position.y

        closest_coord_1 = self.waypoints_2d[closest_idx - 1]
        closest_coord_2 = self.waypoints_2d[closest_idx + 1]

        point_1 = np.array(closest_coord_1)
        point_2 = np.array(closest_coord_2)

        # line that pass through the two waypoints, find the coefficients for ax + by + c = 0
        b = 1
        a = -(point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
        c = - point_1[1] - (point_2[1] - point_1[1]) / (point_2[0] - point_1[0]) * (-point_1[0])

        # distance between the actual position and the line that passes through the next two waypoints
        # cte = abs(a * x0 + b * y0 + c) / math.sqrt(a**2 + b**2)
        cte = (a * x0 + b * y0 + c) / math.sqrt(a**2 + b**2) 
        return cte
    def pose_cb(self, msg):
        self.pose = msg
        
    def waypoints_cb(self, waypoints):
        self.base_lane = waypoints
        if not self.waypoints_2d:
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in waypoints.waypoints]
            self.waypoint_tree = KDTree(self.waypoints_2d)

    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        self.stopline_wp_idx = msg.data

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
