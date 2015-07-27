from setuptools import setup, Extension

m = Extension(
    'pymavlink',
    include_dirs=['mavlink/include/mavlink/v1.0'],
    libraries=['pthread'],
    sources=['pymavlink.cpp', 'serial_port.cpp',
             'autopilot_interface.cpp'],
)

setup(
    name='PyMavlink',
    version='1.0',
    description='Mavlink communication for python',
    ext_modules=[m],
)
