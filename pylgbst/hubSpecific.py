from pylgbst.hub import SmartHub, MoveHub
from pylgbst.peripherals import COLORS
from pylgbst import *


log = logging.getLogger("hubSpecific")

class ExpressPassengerTrain(SmartHub):
    """
    Class implementing Lego SmartHub specifics, abstract low level calls
    Implements for "Express Passenger Train":
    https://www.lego.com/en-pt/product/express-passenger-train-60337
    With hub:
    https://www.lego.com/en-pt/product/hub-88009


    Attached peripheral SYSTEM_TRAIN_MOTOR => TrainMotor on port 0x0 -> motor
    Attached peripheral LED_LIGHT => LEDLight on port 0x1 -> lights
    Attached peripheral RGB_LIGHT => LEDRGB on port 0x32 -> Connection light
    Attached peripheral CURRENT => Current on port 0x3b
    Attached peripheral VOLTAGE => Voltage on port 0x3c


    :type led: LEDRGB
    :type current: Current
    :type voltage: Voltage
    :type port_A: TrainMotor
    :type port_B: LEDLight

    """
    DEFAULT_NAME = "HUB NO.4"



    def __init__(self, connection=None, hub_name=DEFAULT_NAME):
        if connection is None:
            connection = get_connection_auto(hub_name=hub_name)

        super().__init__(connection)


    def lightOff(self):
        log.info("ExpressPassengerTrain: Lights off")
        self.port_B.set_brightness(0)


    def lightOn(self, intensityPercentage):
        log.info(f"ExpressPassengerTrain: Lights on. Percentage: {intensityPercentage}%.")
        self.port_B.set_brightness(intensityPercentage)

    def getLightBrigthness(self):
        return self.brigthness()

    def motorStop(self):
        log.info("ExpressPassengerTrain: Motor stop.")
        self.port_A.stop()

    def motorForward(self, velocityPercentage):
        log.info(f"ExpressPassengerTrain: Motor forward. Percentage: {velocityPercentage}%. ")
        percent= velocityPercentage / 100
        self.port_A.power(percent)

    def motorBackward(self, velocityPercentage):
        log.info(f"ExpressPassengerTrain: Motor backward. Percentage: {velocityPercentage}%. ")
        percent= velocityPercentage / 100
        self.port_A.power(-percent)



    def led_color(self,color):
        """
        Example hub.led_color(COLOR_PURPLE)
        :param color: from pylgbst.peripherals.COLORS
        :return: NONE
        """
        # We get a response with payload and port, not x and y here...
        def colour_callback(named):
            log.info("LED Color callback: %s", named)

        self.led.subscribe(colour_callback)
        self.led.set_color(color)

class PorscheGT4(MoveHub):
    """
    Class implementing Lego Hub Move specifics, abstract low level calls
    Implements for "Porsche GT4 e-Performance Race Car":
    https://www.lego.com/en-pt/product/porsche-gt4-e-performance-race-car-42176
    With Lego Move Hub (88006):
    https://www.lego.com/en-pt/product/move-hub-88006


    Attached peripheral SYSTEM_TRAIN_MOTOR => TrainMotor on port 0x0
    Attached peripheral LED_LIGHT => LEDLight on port 0x1
    Attached peripheral RGB_LIGHT => LEDRGB on port 0x32
    Attached peripheral CURRENT => Current on port 0x3b
    Attached peripheral VOLTAGE => Voltage on port 0x3c

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

Desconocidos:


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
    DEFAULT_NAME = "Technic Move  "



    def __init__(self, connection=None, hub_name=DEFAULT_NAME):
        log.info(f"PorscheGT4: Initialicing. Hub_name: '{hub_name}', connection: {connection}")
        if connection is None:
            log.info(f"PorscheGT4: Obtaining connection. Hub_name: '{hub_name}'")
            connection = get_connection_auto(hub_name=hub_name)

        super().__init__(connection)

    def lightsFrontOff(self):
        log.info("PorscheGT4: Lights front off")
        self.port_A.set_brightness(0)


    def lightsFrontOn(self, intensityPercentage):
        log.info(f"PorscheGT4: Lights front on. Percentage: {intensityPercentage}%.")
        self.port_A.set_brightness(intensityPercentage)

    def lightsBackOff(self):
        log.info("PorscheGT4: Lights back off")
        self.port_B.set_brightness(0)


    def lightsBackOn(self, intensityPercentage):
        log.info(f"PorscheGT4: Lights back on. Percentage: {intensityPercentage}%.")
        self.port_B.set_brightness(intensityPercentage)


    def lightsOff(self):
        log.info("PorscheGT4: Lights off")
        self.lightsBackOff()
        self.lightsFrontOff()


    def lightsOn(self, intensityPercentage):
        log.info(f"PorscheGT4: Lights on. Percentage: {intensityPercentage}%.")
        self.lightsFrontOn(intensityPercentage)
        self.lightsBackOn(intensityPercentage)

    def getLightBrigthness(self):
        return self.brigthness()

    def steeringWheelCenter(self):
        log.info("PorscheGT4: Steer center.")
        self.port_A.stop()

    def steeringWheelRight(self, turnPercentage = 100):
        log.info(f"PorscheGT4: Motor forward. Percentage: {turnPercentage}%. ")
        percent= turnPercentage / 100
        self.port_A.power(percent)

    def steeringWheelLeft(self, turnPercentage = 100):
        log.info(f"PorscheGT4: Motor backward. Percentage: {turnPercentage}%. ")
        percent= turnPercentage / 100
        self.port_A.power(-percent)

    def motorStop(self):
        log.info("PorscheGT4: Motor stop.")
        self.port_A.stop()

    def motorForward(self, velocityPercentage):
        log.info(f"PorscheGT4: Motor forward. Percentage: {velocityPercentage}%. ")
        percent= velocityPercentage / 100
        self.port_A.power(percent)

    def motorBackward(self, velocityPercentage):
        log.info(f"PorscheGT4: Motor backward. Percentage: {velocityPercentage}%. ")
        percent= velocityPercentage / 100
        self.port_A.power(-percent)



    def led_color(self,color):
        """
        Example hub.led_color(COLOR_PURPLE)
        :param color: from pylgbst.peripherals.COLORS
        :return: NONE
        """
        # We get a response with payload and port, not x and y here...
        def colour_callback(named):
            log.info("LED Color callback: %s", named)

        self.led.subscribe(colour_callback)
        self.led.set_color(color)



