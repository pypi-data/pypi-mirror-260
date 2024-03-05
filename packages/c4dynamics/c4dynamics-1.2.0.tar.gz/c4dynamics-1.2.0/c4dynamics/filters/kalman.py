import numpy as np

class kalman:
    # x = 0   # state vector. 
    # P = 0   # covariance matrix, nxn
    # Q = 0   # process noise covariance matrix, nxn 
    # H = 0   # measurement matrix, pxn 
    # R = 0   # measurement noise covariance matrix, pxp 
    
    Kinf = None 

    def __init__(self, P0, A, H, Q, R, dt, b = None, steadystate = False): 
        self.P  = P0   # Initial error covariance matrix
        self.A  = A    # State transition matrix
        self.H  = H    # Measurement matrix
        self.Q  = Q    # Process noise covariance matrix
        self.R  = R    # Measurement noise covariance matrix
        self.dt = dt 
        self.b  = b  
        self.F = np.eye(len(A)) + dt * A

        if steadystate: 
            R_inv = np.linalg.inv(R)
            # Compute the solution to the Riccati equation
            P = np.linalg.solve(-(A.T @ R_inv @ H.T @ H @ A) + A.T @ R_inv @ A, -Q)
            self.Kinf = P @ H.T @ R_inv

      
    def predict(self, x, u = None):
        #
        # Predict 
        ##
        x = self.F @ x

        if u is not None and self.b is not None:
            x += self.b @ u

        if self.Kinf is not None:
            self.P = self.F @ self.P @ self.F.T + self.Q
        
        return x 
        
 
    def correct(self, x, z):
        # 
        # Correct 
        # // assumes called immediately after a predict. 
        ## 
        if self.Kinf is None:
            K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
            self.P = self.P - K @ self.H @ self.P

        x += K @ (z - self.H @ x)


        return x 


