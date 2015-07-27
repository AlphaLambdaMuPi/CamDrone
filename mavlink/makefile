all: mavlink_control

mavlink_control: mavlink_control.cpp
	g++ -I mavlink/include/mavlink/v1.0 mavlink_control.cpp serial_port.cpp autopilot_interface.cpp -o mavlink_control -lpthread

mavlink_control_old: mavlink_control_old.cpp
	g++ -I mavlink/include/mavlink/v1.0 mavlink_control_old.cpp serial_port.cpp autopilot_interface.cpp -o mavlink_control_old -lpthread

clean:
	 rm -rf *o mavlink_control
