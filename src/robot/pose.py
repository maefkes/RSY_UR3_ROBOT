import numpy as np
import math
import rtde_control
import rtde_receive
from scipy.spatial.transform import Rotation as R

class pose:
    def __init__(self, _rtdeControl, _frame=[0,0,0,0,0,0]):
        self.jointPositions = np.asarray([0,0,0,0,0,0])

        self.transInMeters = np.asarray([0,0,0])
        self.transInMiliMeters = np.asarray([0,0,0])
        
        self.rotVector = np.asarray([0,0,0])
        self.rotEulerZYX = np.asarray([0,0,0])

        self.frame = _frame
        self.qnear = np.deg2rad([-80.91, -93.75, -51.85,-214.14,9.09,0.0])
        self.rtdeControl = _rtdeControl
        pass

    def vec_to_euler(self, rotvec):
        r = R.from_rotvec(rotvec)
        euler = r.as_euler('xyz')
        return (euler)
    
    def euler_to_vec(self, rot):
        r = R.from_euler('xyz', rot)
        vec = r.as_rotvec()
        return (vec)
    
    def setTransMili(self, trans):
        self.transInMiliMeters = trans
        self.transInMeters = np.asarray(trans) / 1000.0
        pass

    def setTransMeters(self, trans):
        self.transInMeters = trans
        self.transInMiliMeters = np.asarray(trans) * 1000.0
        pass

    def setRotEuler(self, rot, radiant=False):
        if not radiant:
            rot = np.deg2rad(rot)
        self.rotEulerZYX = rot
        self.rotVector = self.euler_to_vec(rot)

    def setRotVec(self, rot):
        self.rotEulerZYX = self.vec_to_euler(rot)
        self.rotVector = rot
            
    def setJoint(self, joint):
        self.jointPositions = joint
        cartesian = self.rtdeControl.getForwardKinematics(np.asarray(joint), self.rtdeControl.getTCPOffset())#joint)
        self.setTransMeters(cartesian[:3])
        self.setRotVec(cartesian[3:])
        pass

    def setCartesian(self, cart, *qnear):
        self.setTransMeters(cart[:3])
        self.setRotVec(cart[3:])
        cartOfRobot = self.rtdeControl.poseTrans(self.frame, cart)
        #print(cartOfRobot)
        self.jointPositions = self.rtdeControl.getInverseKinematics(cartOfRobot, qnear=qnear)
        print(np.rad2deg(self.jointPositions))
        pass

    def getJoint(self):
        cart = np.append(self.transInMeters,self.rotVector)
        cartOfRobot = self.rtdeControl.poseTrans(self.frame, cart)
        self.jointPositions = self.rtdeControl.getInverseKinematics(cartOfRobot)
        for i in range(len(self.jointPositions)):
            if self.jointPositions[i] >= 2*math.pi:
                self.jointPositions[i] -= 2*math.pi
            if self.jointPositions[i] <=  -2*math.pi:
                self.jointPositions[i] += 2*math.pi
        return(self.jointPositions)
    
    def getCartesian(self):
        return(np.append(self.transInMeters, self.rotVector))
    
    def getEulerZYX(self):
        return(self.rotEulerZYX)
    
    def getRotVec(self):
        return(self.rotVector)