# coding=utf-8
import time
from time import sleep

from pylgbst import *
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK, COLOR_PURPLE, \
    COLOR_BLUE

from bleak import BleakScanner

from pylgbst.hubSpecific import ExpressPassengerTrain

"""
   Class implementing Lego SmartHub specifics, abstract low level calls
   Implements for "Express Passenger Train":
   https://www.lego.com/en-pt/product/express-passenger-train-60337
   With hub:
   https://www.lego.com/en-pt/product/hub-88009
"""

log = logging.getLogger("demoExpressTrain")


async def discover_bluetooth_devices():
   print("Searching Bluetooth devices...")
   devices = await BleakScanner.discover()
   if devices:
       print("\nDevices founded:")
       for device in devices:
           print(f"Name: '{device.name or 'Unknown'}' | Address: {device.address}")
   else:
       print("Any Bluetooth devices found.")


def demo_led_colors(movehub):
   # LED colors demo
   log.info("LED colors demo")

   # We get a response with payload and port, not x and y here...
   def colour_callback(named):
       log.info("LED Color callback: %s", named)

   movehub.led.subscribe(colour_callback)
   for color in list(COLORS.keys())[1:] + [COLOR_BLACK]:
       log.info("Setting LED color to: %s", COLORS[color])
       movehub.led.set_color(color)
       sleep(1)


def demo_ligths(hub):
   log.info("Light test.")
   hub.lightOn(100)
   sleep(2)
   hub.lightOn(50)
   sleep(2)
   hub.lightOff()

def demo_motors(hub):
   log.info("Motor test. Rotate motor forward and backward, variation velocity.")
   hub.motorForward(1)
   hub.motorForward(20)
   sleep(2)
   hub.motorForward(50)
   sleep(2)
   hub.motorForward(100)
   sleep(2)
   hub.motorStop()
   sleep(2)
   hub.motorBackward(20)
   sleep(2)
   hub.motorBackward(50)
   sleep(2)
   hub.motorBackward(100)
   sleep(2)
   hub.motorStop()


def demo_voltage(movehub):
   def callback1(value):
       log.info("Amperage: %s", value)

   def callback2(value):
       log.info("Voltage: %s", value)

   movehub.current.subscribe(callback1, mode=Current.CURRENT_L, granularity=0)
   movehub.current.subscribe(callback1, mode=Current.CURRENT_L, granularity=1)

   movehub.voltage.subscribe(callback2, mode=Voltage.VOLTAGE_L, granularity=0)
   movehub.voltage.subscribe(callback2, mode=Voltage.VOLTAGE_L, granularity=1)
   time.sleep(5)
   movehub.current.unsubscribe(callback1)
   movehub.voltage.unsubscribe(callback2)


def demo_all(movehub):
   demo_ligths(movehub)
   demo_motors(movehub)
   demo_led_colors(movehub)
   demo_voltage(movehub)


DEMO_CHOICES = {
   'all': demo_all,
   'voltage': demo_voltage,
   'led_colors': demo_led_colors,
   'motors': demo_motors,
   'lights': demo_ligths
   }


def get_options():
   import argparse
   arg_parser = argparse.ArgumentParser(
       description='Demonstrate move-hub communications',
   )
   arg_parser.add_argument(
       '-c', '--connection',
       default='auto://',
       help='''Specify connection URL to use, `protocol://mac?param=X` with protocol in:
   "gatt","pygatt","gattlib","gattool", "bluepy","bluegiga"'''
   )
   arg_parser.add_argument(
       '-d', '--demo',
       default='all',
       choices=sorted(DEMO_CHOICES.keys()),
       help="Run a particular demo, default all"
   )
   return arg_parser


def connection_from_url(url):
   import pylgbst
   if url == 'auto://':
       return None
   try:
       from urllib.parse import urlparse, parse_qs
   except ImportError:
       from urlparse import urlparse, parse_qs
   parsed = urlparse(url)
   name = 'get_connection_%s' % parsed.scheme
   factory = getattr(pylgbst, name, None)
   if not factory:
       msg = "Unrecognised URL scheme/protocol, expect a get_connection_<protocol> in pylgbst: %s"
       raise ValueError(msg % parsed.protocol)
   params = {}
   if parsed.netloc.strip():
       params['hub_mac'] = parsed.netloc
   for key, value in parse_qs(parsed.query).items():
       if len(value) == 1:
           params[key] = value[0]
       else:
           params[key] = value
   return factory(
       **params
   )


if __name__ == '__main__':
   logging.basicConfig(level=logging.INFO, format='%(relativeCreated)d\t%(levelname)s\t%(name)s\t%(message)s')
   parser = get_options()
   options = parser.parse_args()
   parameters = {}

   #Uncomment for discover bluetooth devices
   #asyncio.run(discover_bluetooth_devices())

   try:
       connection = get_connection_bleak(hub_name="HUB NO.4")
       parameters['connection'] = connection
   except ValueError as err:
       parser.error(err.args[0])


   hub = ExpressPassengerTrain(**parameters)
   #hub = ExpressPassengerTrain(hub_name="HUB NO.4")

   try:
       demo = DEMO_CHOICES[options.demo]
       demo(hub)
   finally:
       hub.disconnect()

