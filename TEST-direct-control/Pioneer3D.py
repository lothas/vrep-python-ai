# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:53:24 2015

@author: Lothas
"""

import vrep
import math


def vec_length(vec):
    length = 0
    for i in vec:
        length += i*i
    length = math.sqrt(length)
    return length
    

class Pioneer3D:
    def __init__(self, clientID, name):
        self.clientID = clientID
        self.name = name
        
        self.noDetectionDist = 0.5
        self.maxDetectionDist = 0.2
        self.detect = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.braitenbergL = [-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.braitenbergR = [-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.v0 = 2
        
        errorCode, self.left_motor_handle = vrep.simxGetObjectHandle(clientID,
                                          'Pioneer_p3dx_leftMotor'+name,
                                          vrep.simx_opmode_oneshot_wait)
                                          
        errorCode, self.right_motor_handle = vrep.simxGetObjectHandle(clientID,
                                          'Pioneer_p3dx_rightMotor'+name,
                                          vrep.simx_opmode_oneshot_wait)
            
        self.ultra_sensors = []
        for i in range(1,16):
            errorCode, sensor_handle = vrep.simxGetObjectHandle(clientID,
                                'Pioneer_p3dx_ultrasonicSensor'+str(i)+name,
                                vrep.simx_opmode_oneshot_wait)
            if not errorCode:
                self.ultra_sensors.append(sensor_handle)
                
                returnCode, detectionState, \
                detectedPoint, detectedObjectHandle, \
                detectedSurfaceNormalVector = \
                    vrep.simxReadProximitySensor(clientID, 
                                                self.ultra_sensors[i-1],
                                                vrep.simx_opmode_streaming)
            else:
                print 'Failed to connect to ultrasonic sensor '+str(i)
                
                
    def drive(self):
        Left = self.v0
        Right = self.v0
        
        for i in range(0,len(self.ultra_sensors)-1):
            res, detectionState, \
            detectedPoint, detectedObjectHandle, \
            detectedSurfaceNormalVector = \
                vrep.simxReadProximitySensor(self.clientID, 
                                            self.ultra_sensors[i],
                                            vrep.simx_opmode_buffer)
            dist = vec_length(detectedPoint)
            if (res==0) and (dist<self.noDetectionDist):
                if (dist<self.maxDetectionDist):
                    dist=self.maxDetectionDist
                self.detect[i]=1-((dist-self.maxDetectionDist)/(self.noDetectionDist-self.maxDetectionDist))
            else:
                self.detect[i]=0
    	
            Left=Left+self.braitenbergL[i]*self.detect[i]
            Right=Right+self.braitenbergR[i]*self.detect[i]
            
            
        vrep.simxSetJointTargetVelocity(self.clientID,
                                        self.left_motor_handle,
                                        Left,
                                        vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(self.clientID,
                                        self.right_motor_handle,
                                        Right,
                                        vrep.simx_opmode_streaming)