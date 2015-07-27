#! /usr/bin/env python3

import asyncio
import subprocess
import numpy as np

comm = None

class Mavlink:
    def __init__(self, port, baudrate=921600):
        self.port = port
        self.baudrate = baudrate
        self._process = None
        self._connected = asyncio.Future()
        self._pos = None
        self._loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def _read(self):
        data = yield from self._process.stdout.readline()
        try:
            data = data.decode().strip()
        except UnicodeError:
            data = ""
        return data

    @asyncio.coroutine
    def connect(self):
        cmd = ['./mavlink_control', '-d', str(self.port), '-b', str(self.baudrate)]
        cmd = ' '.join(cmd)
        self._process = yield from asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=None
        )
        res = yield from self._read()
        # print(res)
        if res == 'CONNECTED':
            self._connected.set_result(True)
        else:
            self._connected.set_result(False)
        self._loop.create_task(self.send_position())

    @asyncio.coroutine
    def read_sensors(self):
        connected = yield from self._connected
        if not connected:
            return
        ret = {}
        self._process.stdin.write(b'R\n')
        data = yield from self._read()
        ret['pos'] = np.array(list(map(float, data.split())))
        data = yield from self._read()
        ret['time'] = int(data)
        data = yield from self._read()
        ret['accel'] = np.array(list(map(float, data.split())))
        data = yield from self._read()
        ret['omega'] = np.array(list(map(float, data.split())))
        data = yield from self._read()
        ret['mag'] = np.array(list(map(float, data.split())))
        data = yield from self._read()
        ret['alt'] = float(data)

        return ret

    def set_position_estimated(self, pos):
        '''need x, y, z, roll, pitch, yaw'''
        self._pos = pos

    @asyncio.coroutine
    def send_position(self):
        while True:
            if self._pos is not None:
                self._process.stdin.write(b'V\n')
                self._process.stdin.write(' '.join(map(str, self._pos)).encode()
                                          + b'\n')
                print("Send pos:", self._pos)
                self._pos = None
            yield from asyncio.sleep(0.5)
    
    @asyncio.coroutine
    def close(self):
        self._process.stdin.write(b'E\n')
        yield from self._process.wait()

@asyncio.coroutine
def reading(mavlink):
    for i in range(20):
        print("{} runs".format(i))
        data = yield from mavlink.read_sensors()
        print(data)

def test_mavlink():
    loop = asyncio.get_event_loop()
    mavlink = Mavlink("/dev/ttyUSB1")
    loop.create_task(mavlink.connect())
    loop.create_task(reading(mavlink))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
         loop.run_until_complete(mavlink.close())
    finally:
        loop.close()
        print('exit.')

if __name__ == '__main__':
    test_mavlink()


