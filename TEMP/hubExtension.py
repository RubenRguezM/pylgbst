import threading

from pylgbst import get_connection_auto
from pylgbst.hub import Hub
from pylgbst.messages import *
from pylgbst.peripherals import *
from pylgbst.utilities import queue
from pylgbst.utilities import str2hex, usbyte, ushort


class TechnicMoveHub(Hub):
    """
    Class implementing Lego Technic Move Hub (88006):
    https://www.lego.com/en-pt/product/move-hub-88006
    2771	INFO	comms-bleak	Device matched: BLEDevice(34:68:B5:7C:E8:CD, Technic Move  )
7399	WARNING	hub	Have no dedicated class for peripheral type 0x56 (UNKNOWN) on port 0x32
7430	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x32
7441	WARNING	hub	Have no dedicated class for peripheral type 0x56 (UNKNOWN) on port 0x33
7455	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x33
7466	WARNING	hub	Have no dedicated class for peripheral type 0x57 (UNKNOWN) on port 0x34
7480	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x34
7491	WARNING	hub	Have no dedicated class for peripheral type 0x58 (UNKNOWN) on port 0x35
7520	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x35
7531	WARNING	hub	Have no dedicated class for peripheral type 0x59 (UNKNOWN) on port 0x36
7531	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x36
7542	INFO	hub	Attached peripheral TECHNIC_MEDIUM_HUB_TEMPERATURE_SENSOR => Temperature on port 0x37
7553	WARNING	hub	Have no dedicated class for peripheral type 0x39 (TECHNIC_MEDIUM_HUB_ACCELEROMETER) on port 0x38
7553	INFO	hub	Attached peripheral TECHNIC_MEDIUM_HUB_ACCELEROMETER => Peripheral on port 0x38
7564	WARNING	hub	Have no dedicated class for peripheral type 0x3a (TECHNIC_MEDIUM_HUB_GYRO_SENSOR) on port 0x39
7564	INFO	hub	Attached peripheral TECHNIC_MEDIUM_HUB_GYRO_SENSOR => Peripheral on port 0x39
7575	INFO	hub	Attached peripheral TECHNIC_MEDIUM_HUB_TILT_SENSOR => TiltSensor on port 0x3a
7586	WARNING	hub	Have no dedicated class for peripheral type 0x5d (UNKNOWN) on port 0x3b
7586	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x3b
7597	INFO	hub	Attached peripheral VOLTAGE => Voltage on port 0x3c
7608	WARNING	hub	Have no dedicated class for peripheral type 0x5c (UNKNOWN) on port 0x3d
7608	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x3d
7619	WARNING	hub	Have no dedicated class for peripheral type 0x5e (UNKNOWN) on port 0x3e
7619	INFO	hub	Attached peripheral UNKNOWN => Peripheral on port 0x3e
7630	INFO	hub	Attached peripheral RGB_LIGHT => LEDRGB on port 0x3f

    :type led: LEDRGB
    :type tilt_sensor: TiltSensor
    :type button: Button
    :type current: Current
    :type voltage: Voltage
    :type vision_sensor: pylgbst.peripherals.VisionSensor
    :type port_C: pylgbst.peripherals.Peripheral
    :type port_D: pylgbst.peripherals.Peripheral
    :type motor_A: EncodedMotor
    :type motor_B: EncodedMotor
    :type motor_AB: EncodedMotor
    :type motor_external: EncodedMotor
    """

    DEFAULT_NAME = "LEGO Move Hub"

    # PORTS
    PORT_A = 0x00
    PORT_B = 0x01
    PORT_C = 0x02
    PORT_D = 0x03
    PORT_AB = 0x10
    PORT_LED = 0x32
    PORT_TILT_SENSOR = 0x3A
    PORT_CURRENT = 0x3B
    PORT_VOLTAGE = 0x3C

    # noinspection PyTypeChecker
    def __init__(self, connection=None):
        self._comm_lock = threading.RLock()
        if connection is None:
            connection = get_connection_auto(hub_name=self.DEFAULT_NAME)

        super().__init__(connection)
        self.info = {}

        # shorthand fields
        self.button = Button(self)
        self.led = None
        self.current = None
        self.voltage = None
        self.motor_A = None
        self.motor_B = None
        self.motor_AB = None
        self.vision_sensor = None
        self.tilt_sensor = None
        self.motor_external = None
        self.port_C = None
        self.port_D = None

        self._wait_for_devices()
        self._report_status()

    def _wait_for_devices(self, get_dev_set=None):
        if not get_dev_set:
            get_dev_set = lambda: (self.motor_A, self.motor_B, self.motor_AB, self.led, self.tilt_sensor,
                                   self.current, self.voltage)
        for num in range(0, 100):
            devices = get_dev_set()
            if all(devices):
                log.debug("All devices are present: %s", devices)
                return
            log.debug("Waiting for builtin devices to appear: %s", devices)
            time.sleep(0.1)
        log.warning("Got only these devices: %s", get_dev_set())

    def _report_status(self):
        # maybe add firmware version
        name = self.send(MsgHubProperties(MsgHubProperties.ADVERTISE_NAME, MsgHubProperties.UPD_REQUEST))
        mac = self.send(MsgHubProperties(MsgHubProperties.PRIMARY_MAC, MsgHubProperties.UPD_REQUEST))
        log.info("%s on %s", name.payload, str2hex(mac.payload))

        voltage = self.send(MsgHubProperties(MsgHubProperties.VOLTAGE_PERC, MsgHubProperties.UPD_REQUEST))
        assert isinstance(voltage, MsgHubProperties)
        log.info("Voltage: %s%%", usbyte(voltage.parameters, 0))

        voltage = self.send(MsgHubAlert(MsgHubAlert.LOW_VOLTAGE, MsgHubAlert.UPD_REQUEST))
        assert isinstance(voltage, MsgHubAlert)
        if not voltage.is_ok():
            log.warning("Low voltage, check power source (maybe replace battery)")

    # noinspection PyTypeChecker
    def _handle_device_change(self, msg):
        with self._comm_lock:
            super()._handle_device_change(msg)
            if (
                    isinstance(msg, MsgHubAttachedIO)
                    and msg.event != MsgHubAttachedIO.EVENT_DETACHED
            ):
                port = msg.port
                if port == self.PORT_A:
                    self.motor_A = self.peripherals[port]
                elif port == self.PORT_B:
                    self.motor_B = self.peripherals[port]
                elif port == self.PORT_AB:
                    self.motor_AB = self.peripherals[port]
                elif port == self.PORT_C:
                    self.port_C = self.peripherals[port]
                elif port == self.PORT_D:
                    self.port_D = self.peripherals[port]
                elif port == self.PORT_LED:
                    self.led = self.peripherals[port]
                elif port == self.PORT_TILT_SENSOR:
                    self.tilt_sensor = self.peripherals[port]
                elif port == self.PORT_CURRENT:
                    self.current = self.peripherals[port]
                elif port == self.PORT_VOLTAGE:
                    self.voltage = self.peripherals[port]

                if type(self.peripherals[port]) == VisionSensor:
                    self.vision_sensor = self.peripherals[port]
                elif type(self.peripherals[port]) == EncodedMotor and port not in (
                        self.PORT_A,
                        self.PORT_B,
                        self.PORT_AB,
                ):
                    self.motor_external = self.peripherals[port]
