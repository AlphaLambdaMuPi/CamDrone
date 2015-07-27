#include <Python.h>

#include <iostream>
#include <stdio.h>
#include <cstdlib>
#include <unistd.h>
#include <cmath>
#include <string.h>
#include <inttypes.h>
#include <fstream>
#include <signal.h>
#include <time.h>
#include <sys/time.h>

#include <common/mavlink.h>

#include "autopilot_interface.h"
#include "serial_port.h"

using namespace std;

static Serial_Port *serial_port = NULL;
static Autopilot_Interface *api = NULL;

static PyObject*
pymavlink_connect(PyObject *self, PyObject *args)
{
  const char *uart_name = "/dev/ttyUSB0";
	int baudrate = 57600;
  if (!PyArg_ParseTuple(args, "si", &uart_name, &baudrate))
    return NULL;
  if (serial_port != NULL)
    delete serial_port;
  if (api != NULL)
    delete api;
  char* u = const_cast<char*>(uart_name);
	serial_port = new Serial_Port(u, baudrate);
	api = new Autopilot_Interface(serial_port);

	serial_port->start();
	api->start();

  Py_RETURN_NONE;
}

static PyObject*
pymavlink_disconnect(PyObject *self, PyObject *args)
{
  if (serial_port) {
    serial_port->stop();
    delete serial_port;
    serial_port = NULL;
  }
  if (api) {
    api->stop();
    delete api;
    api = NULL;
  }

  Py_RETURN_NONE;
}

static PyObject*
pymavlink_send_position_estimated(PyObject *self, PyObject *args)
{
  float x = 0, y = 0, z = 0, roll = 0, pitch = 0, yaw = 0;
  if (!PyArg_ParseTuple(args, "ffffff", &x, &y, &z, &roll, &pitch, &yaw))
    return NULL;
  int ret = api->send_position_estimated(x, y, z, roll, pitch, yaw);
  if (ret)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyObject*
pymavlink_get_sensors(PyObject *self, PyObject *args)
{
  PyObject *ret = PyDict_New();
  Py_INCREF(ret);
	Mavlink_Messages messages = api->current_messages;
	mavlink_local_position_ned_t pos = messages.local_position_ned;
	mavlink_highres_imu_t imu = messages.highres_imu;
  PyDict_SetItemString(ret, "time", PyLong_FromLong(imu.time_usec));
  PyDict_SetItemString(ret, "xacc", PyFloat_FromDouble(imu.xacc));
  PyDict_SetItemString(ret, "yacc", PyFloat_FromDouble(imu.yacc));
  PyDict_SetItemString(ret, "zacc", PyFloat_FromDouble(imu.zacc));
  PyDict_SetItemString(ret, "ygyro", PyFloat_FromDouble(imu.xgyro));
  PyDict_SetItemString(ret, "xgyro", PyFloat_FromDouble(imu.zgyro));
  PyDict_SetItemString(ret, "zgyro", PyFloat_FromDouble(imu.zgyro));
  PyDict_SetItemString(ret, "xmag", PyFloat_FromDouble(imu.xmag));
  PyDict_SetItemString(ret, "ymag", PyFloat_FromDouble(imu.ymag));
  PyDict_SetItemString(ret, "zmag", PyFloat_FromDouble(imu.zmag));
  PyDict_SetItemString(ret, "altitude", PyFloat_FromDouble(imu.pressure_alt));
  PyDict_SetItemString(ret, "temperature", PyFloat_FromDouble(imu.temperature));
  Py_DECREF(ret);
  return ret;
}

static PyMethodDef pymavlink_methods[] = {
  {"connect", pymavlink_connect, METH_VARARGS,
    "Connect with the pixhawk via serial port."},
  {"disconnect", pymavlink_disconnect, METH_VARARGS,
    "Disconnect with the pixhawk."},
  {"send_position_estimated", pymavlink_send_position_estimated, METH_VARARGS,
    "Send position observed by other sensors."},
  {"get_sensors", pymavlink_get_sensors, METH_VARARGS,
    "Get the information from sensors."},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef pymavlink_module = {
  PyModuleDef_HEAD_INIT,
  "pymavlink",   /* name of module */
  NULL, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
               or -1 if the module keeps state in global variables. */
  pymavlink_methods
};


PyMODINIT_FUNC
PyInit_pymavlink(void)
{
  return PyModule_Create(&pymavlink_module);
}

