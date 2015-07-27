#! /usr/bin/env python3

import asyncio
import subprocess
import numpy as np
import time

comm = None

class Camera:
    def __init__(self, notify):
        self._process = None
        self._now_pos = np.array([0., 0., 0.])
        self._running = False
        self._notify = notify

    @asyncio.coroutine
    def connect(self):
        self._process = yield from asyncio.create_subprocess_exec(
            'python2', 'camera.py',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        self._running = True

    @asyncio.coroutine
    def run(self):
        while self._running:
            data = yield from self._process.stdout.readline()
            print(data)
            self._now_pos = np.array(list(map(float, data.split())))
            yield from self._notify(time.time(), self._now_pos)

    def stop(self):
        self._running = False
        self._process.terminate()

