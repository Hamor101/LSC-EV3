import keyboard
import socket

state = {
    'w':False,
    'a':False,
    's':False,
    'd':False
}

def send(v, t):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.98', 8000))
        s.sendall(f"{v} {t}\n".encode('utf-8'))
        data = s.recv(1024)
        print(data)
        pass


def handle(k):
    if k.name not in state:
        return
    eventtype = k.event_type == keyboard.KEY_DOWN
    if state[k.name] == eventtype:
        return
    state[k.name] = eventtype
    print(state)
    v = 100 * (state['w'] - state['s'])
    t = 100 * (state['d'] - state['a'])
    send(v, t)

def main():
    keyboard.hook(handle)
    input()


if __name__ == "__main__":
    main()