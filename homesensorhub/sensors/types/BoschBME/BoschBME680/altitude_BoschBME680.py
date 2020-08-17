"""Module which implements the Bosch680BME altitude sensor module set up."""
from sensors.types.altitude import Altitude


class AltitudeBoschBME680(Altitude):
    """Class which implements the altitude collected from BoschBME680 sensor module."""

    MEASURE = 'Meters'
    SENSOR_NAME = 'BoschBME680'

    def __init__(self, sensor, sensor_name):
        self.__sensor = sensor
        self.__sensor_name = sensor_name

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME680, BME680 etc.).

        :return: string
        """
        return self.__sensor_name

    def get_sensor_value(self) -> int:
        """
        Return the value collected by the sensor.

        :return: int
        """
        return self.__sensor.altitude

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the altitude for this sensor module.

        :return: string
        """
        return AltitudeBoschBME680.MEASURE
