"""Module which implements the environmantal sensors functionality."""
from sensors.sensor import Sensor

import logging
import time

import board
import busio
import adafruit_bme280
import adafruit_bme680


logging.basicConfig(level=logging.INFO)


class EnvironmentalSensor(Sensor):
    """Class which implements the environmantal sensor functionality."""

    def __init__(self, sensor="undefined", name="undefined"):
        """
        Initialise the environmental sensor data.

        Each type of this sensor has a name, the actual sensor which was
        discovered after probing and the data which will be collected using it.

        :return: None
        """
        super().__init__(sensor, name)

    def set_sea_level_pressure(self, sea_level_pressure) -> None:
        """Determine altitude based on this."""
        self.sensor.sea_level_pressure = sea_level_pressure

    def collect_data(self) -> None:
        """
        Collect the data from this sensor.

        The data is formed of a set of temperature, humidity, pressure and
        altitude values.

        :return: None
        """
        self.data = {'temperature': self.sensor.temperature,
                     'humidity': self.sensor.humidity,
                     'pressure': self.sensor.pressure,
                     'altitude': self.sensor.altitude
                     }

        try:
            self.data['gas'] = self.sensor.gas
        except AttributeError:
            pass


class EnvironmentalSensorProbe:
    """Class which implements proving for multiple environmantal sensors."""

    I2C = busio.I2C(board.SCL, board.SDA)
    ADDRESSES = [0x77, 0x76]

    def __init__(self) -> None:
        """Initialise the list of sensors for the probing.

        :return: None
        """
        self.__sensors = []

        self.probe_sensors()

    def probe_sensors(self) -> None:
        """
        Probe for multiple possible sensors.

        Function which iterates over multiple I2C addresses and sensors probing
        in the case we have multiple types on the same device (eg. BME280,
        BME680, etc.). In case multiple sensors are connected to the same
        device, we need to correctly assign the sensor to its I2C address.

        :return: None
        """
        sensor_choices = {
            (adafruit_bme280.Adafruit_BME280_I2C, "bme280"),
            (adafruit_bme680.Adafruit_BME680_I2C, "bme680")
        }

        for address in self.ADDRESSES:
            for sensor in sensor_choices:
                sensor_probe_function = sensor[0]
                sensor_name = sensor[0]
                try:
                    found_sensor = sensor_probe_function(self.I2C, address)
                    environmental_sensor = EnvironmentalSensor(found_sensor,
                                                               sensor_name)
                    self.__sensors.append(environmental_sensor)
                    logging.info("Environmental Sensor {} found at {}".format(
                        sensor_name, hex(address)))
                except ValueError as ve:
                    logging.debug(ve)
                except RuntimeError as re:
                    logging.info("These are not the sensors"
                                 "you're looking for")
                    logging.debug(re)

    def get_sensors(self):
        """Return the list of found sensors."""
        return self.__sensors

