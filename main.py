#! /usr/bin/env python3

import asyncio
import pymavlink
import camera3

PORT = "/dev/ttyUSB0"

@asyncio.coroutine
def run(mavlink, camera):
    yield from mavlink.connect()
    yield from camera.connect()
    print("connected.")
    yield from camera.run()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    mavlink = pymavlink.Mavlink(PORT)

    @asyncio.coroutine
    def notify(time, pos):
        mavlink.set_position_estimated([pos[0], pos[1], pos[2], 0., 0., 0.])
        data = yield from mavlink.read_sensors()
        # print(data)

    camera = camera3.Camera(notify)
    loop.run_until_complete(run(mavlink, camera))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        camera.stop()
        loop.run_until_complete(mavlink.close())
    finally:
        loop.close()
        print('exit.')
        

