import matplotlib.pyplot as plt
import math
import numpy as np

x_r=0.0;
y_r=0.0;
x_b=0.0;
y_b=0.0;
x_g=0.00;
y_g=0.0;
theta=0.0;
x_dot=0.0;
y_dot=0.0;

theta_r=0.0;
theta_gb=0.0;
t=0.1;
omega=0.0;
v=0.0;
v_r=0.0;
v_l=0.0;
aL=15.4;
R=3.5;
i=0.0;
X=[];
Y=[];
V_R=[];
V_L=[];
T=[];
THETA=[];
X_DOT=[];
Y_DOT=[];
OMEGA=[];
phi=0.0
theta_prev=0.0
phi_dot=0.0
PHI=[];

ku=0.1
kw=0.1  
L=2
k1=0.3

x=0.0
y=0.0
j=0


##def input_data():
##    global x_r, y_r, x_b, y_b, theta, x_g, y_g;
##    
##    x_r = float(input('x_r: '));
##    y_r = float(input('y_r: '));
##    x_b = float(input('x_b: '));
##    y_b = float(input('y_b: '));
##    theta = float(input('Theta: '));
##    x_g = float(input('x_g: '));
##    y_g = float(input('y_g: '));

def velocity():
    global theta,v,x_dot,y_dot,x,y, theta_gb, x_r, y_r, x_g, y_g

    x=x_r-x_b
    y=y_r-y_b

    theta_gb = math.atan2((y_g-y_b),(x_g-x_b));
    if theta_gb<0:
        theta_gb = theta_gb + 3.14
 
    
    
    x_dot=ku*math.tanh(math.pow(x,2)+math.pow(y,2))*math.cos(theta)
    y_dot=ku*math.tanh(math.pow(x,2)+math.pow(y,2))*math.sin(theta)

    v = math.pow((math.pow(x_dot,2)+math.pow(y_dot,2)),0.5)
    

def bot_wheel():
    global omega, theta, theta_r, v_r, v_l, v, L, R, x,y,phi, x_r, y_r, x_g, y_g, theta_prev, phi_dot, x_dot, y_dot, theta_gb;

    x=x_r-x_b
    y=y_r-y_b
    
    Fy=(L-1)*math.sin(theta_gb)*math.pow(y,2) + L*math.cos(theta_gb)*x*y - math.sin(theta_gb)*math.pow(x,2)
    Fx=(L-1)*math.cos(theta_gb)*math.pow(x,2) + L*math.sin(theta_gb)*x*y - math.cos(theta_gb)*math.pow(y,2)
    
    Fy_dot = (2*y*y_dot*(L-1)*math.sin(theta_gb) + L*math.cos(theta_gb)*x*y_dot + L*math.cos(theta_gb)*y*x_dot - 2*math.sin(theta_gb)*x*x_dot)
    Fx_dot = (2*x*x_dot*(L-1)*math.cos(theta_gb) + L*math.sin(theta_gb)*x*y_dot + L*math.sin(theta_gb)*y*x_dot - 2*math.cos(theta_gb)*y*y_dot)

    phi_dot=(Fx*Fy_dot - Fy*Fx_dot)/(math.pow(Fy,2) + math.pow(Fx,2))
    
                                                                                
    phi = math.atan2(Fy,Fx)
##    if phi<0:
##        phi = phi + 3.14
    
    omega = -kw*(theta-phi)+ phi_dot
    
    v_r = (2*v + aL*omega)/(2*R);
    v_l = (2*v - aL*omega)/(2*R);
    
    V_R.append(v_r);
    V_L.append(v_l);
    OMEGA.append(omega);



def graph_field(xr, yr, xb, yb, alpha, xg, yg):
    global x_r, y_r, x_g, y_g, theta, x_b, y_b, x_dot, y_dot, t, theta_prev

    x_r = xr
    y_r = yr
    x_b = xb
    y_b = yb
    theta = alpha
    x_g = xg
    y_g = yg

input_data()
    for i in range(0,100000,1):
        
        velocity();
        bot_wheel();
        
        X_DOT.append(x_dot);
        Y_DOT.append(y_dot);
        
        X.append(x_r);
        Y.append(y_r);
        T.append(i);
        THETA.append(theta);
        PHI.append(phi)
        
        #updating 3 variables
        x_r = x_r + x_dot*t;
        y_r = y_r + y_dot*t;
        
        theta_prev=theta
        theta = theta + omega*t;

        if theta > (2*3.1415):
            theta = theta % (2*3.1415)
        
        


    print(' ')
    print('Expected Orientaion: ',theta_gb)
    print('x_r: ',x_r)
    print('y_r: ',y_r)
    print('theta: ',theta)
    print('x_dot: ',x_dot)
    print('omega: ',omega)
    print('v_r: ',v_r)
    print('Phi dot: ', phi)

        
    fig, ax = plt.subplots(nrows=3, ncols=3)


    plt.subplot(1,3,1)
    plt.plot(Y,X)
    plt.axis([-5,7,-5,7])

    plt.subplot(1,3,2)
    plt.plot(T,V_R)

    plt.subplot(1,3,3)
    plt.plot(X,V_L)

    plt.show()

    return (v_r, v_l)

    

    
    
    
    
