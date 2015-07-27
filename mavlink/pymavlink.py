#! /usr/bin/env python3

import asyncio
import subprocess
import numpy as np

comm = None

class Mavlink:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self._process = None

    @asyncio.coroutine
    def connect(self):
        self._process = yield from asyncio.create_subprocess_exec(
            ['./mavlink_control', '-d', self.port, '-b', str(self.baudrate)],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )

    @asyncio.coroutine
    def read_sensors(self):
        ret = {}
        self._process.stdin.write(b'R\n')
        data = yield from self._process.stdout.readline()
        ret['pos'] = np.array(list(map(float, data.split())))
        data = yield from self._process.stdout.readline()
        ret['time'] = int(data)
        data = yield from self._process.stdout.readline()
        ret['accel'] = np.array(list(map(float, data.split())))
        data = yield from self._process.stdout.readline()
        ret['omega'] = np.array(list(map(float, data.split())))
        data = yield from self._process.stdout.readline()
        ret['mag'] = np.array(list(map(float, data.split())))
        data = yield from self._process.stdout.readline()
        ret['alt'] = float(data.split())

    def send_position_estimated(self, pos):
        '''need x, y, z, roll, pitch, yaw'''
        self._process.stdin.write(b'V\n')
        self._process.stdin.write(' '.join(map(str, pos)).encode() + b'\n')
        
