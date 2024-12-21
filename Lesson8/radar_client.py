import socket
import matplotlib.pyplot as plt
import numpy as np
import time
import itertools

CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONN.connect(('192.168.0.98', 8000))


def send(deg:int) -> int:
    CONN.sendall(f'{int(deg)}\n'.encode())
    d = CONN.recv(1024)
    dist = int(d)
    print(dist)
    return dist

def radar_data():
    radar_range = 180
    radar_res = 3
    data = {}
    while True:
        for deg in itertools.chain(range(0, radar_range, radar_res), range(radar_range, 0, -radar_res)):
            print(deg)
            dist = measure(deg)
            deg = deg/180*np.pi
            data[deg] = dist
            yield deg, data 

def measure(deg):
    return send(deg)

def main():
    max_d = 60
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    plt.ion()
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111, projection='polar')
    line1, *_ = ax.plot(x,y, 'x')
    line2, *_ = ax.plot(0, max_d, 'r')

    ax.set_rlim(0, max_d)


    i = 0
    for c,d in radar_data():
        line1.set_xdata(list(d.keys()))
        line1.set_ydata(list(d.values()))

        line2.set_xdata(list(d.keys()))
        l2y = [max_d if i == c else 0 for i in d.keys()]
        line2.set_ydata(l2y)
        
        if i==10:
            fig.canvas.draw()
            fig.canvas.flush_events()
            i = 0
        i+=1



main()