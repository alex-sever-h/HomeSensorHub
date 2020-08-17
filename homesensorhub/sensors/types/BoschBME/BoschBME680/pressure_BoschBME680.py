"""Module which implements the Bosch680BME pressure sensor module logic."""
from sensors.types.pressure import Pressure


class PressureBoschBME680(Pressure):
    """Class which implements the pressure paired with AdafruitBME680."""

    MEASURE = 'Celsius'
    SENSOR_NAME = 'BoschBME680'

    def __init__(self, sensor, sensor_name):
        """
        Initialise the pressure.

        The object could be initialised with the physical sensor responsable
        for providing values of this type and its name. As an example, the name
        can be "adafruit_bme680".
        """
        self.__sensor = sensor
        self.__sensor_name = sensor_name

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME680, BME680 etc.).

        :return: string
        """
        return self.__sensor_name

    def get_sensor_value(self) -> float:
        """
        Return the value collected by the sensor.

        :return: float
        """
        return self.__sensor.pressure

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the pressure for this sensor module.

        :return: string
        """
        return PressureBoschBME680.MEASURE