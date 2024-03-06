"""Provides weather data based on zipcode."""

import requests
import json
from typing import Union


class Weather:
    """Obtain local weather information based on zipcode.

    Args:
        zipcode (str): The location's zipcode for weather information.
    """

    def __init__(self, zipcode: str) -> None:
        """Instantiate a Weather Class instance."""
        self.zipcode = zipcode
        self.data = self._load_json_data()
        self.latitude, self.longitude = self._get_latitude_longitude()
        self.forecast_url = self._get_weather_forecast_url()
        self.weather_details = self._get_weather_data()

    def _load_json_data(self) -> dict:
        """Load the JSON data set of zipcodes, latitudes and longitudes.

        Returns:
            dict: Data set of zipcodes, latitudes, and longitudes.
        """
        with open("data/2022_gazetteer_zcta_national.json", "r") as json_file:
            gazetteer_data = json.load(json_file)

            return gazetteer_data

    def _get_latitude_longitude(self) -> tuple:
        """Get latitude and longitude based on the zipcode provided.

        Returns:
            tuple: Latitude and longitude coordinates.
        """
        for dictionary in self.data:
            if self.zipcode == (dictionary["zipcode"]):
                latitude = dictionary["latitude"]
                longitude = dictionary["longitude"]

                return latitude, longitude

        raise ValueError(f"Invalid Zip Code: {self.zipcode}")

    def _get_weather_forecast_url(self) -> str:
        """Get National Weather Forecast Office forecast url.

        Returns:
            str: URL of the local weather office obtained by the latitude and longitude coordinates.
        """
        url = f"https://api.weather.gov/points/{self.latitude},{self.longitude}"

        weather_station_response = requests.get(url, timeout=10)
        weather_station_data = weather_station_response.json()
        forecast_url = weather_station_data["properties"]["forecastHourly"]

        return forecast_url

    def _get_weather_data(self) -> dict:
        """Get current weather forecast data.

        Returns:
            dict: Weather related items.
        """
        weather_data_response = requests.get(self.forecast_url, timeout=10)
        weather_data = weather_data_response.json()
        current_weather = weather_data["properties"]["periods"][0]

        weather_information = {
            "short_forecast": current_weather["shortForecast"],
            "detailed_forecast": current_weather["detailedForecast"],
            "temperature": current_weather["temperature"],
            "probability_of_precipitation": current_weather["probabilityOfPrecipitation"]["value"],
            "temperature_unit": current_weather["temperatureUnit"],
            "wind_speed": current_weather["windSpeed"],
            "wind_direction": current_weather["windDirection"],
        }

        return weather_information

    def get_short_forecast(self) -> str:
        """Get the current short weather forecast.

        Returns:
            str: Current short weather forecast.
        """
        short_forecast = self.weather_details["short_forecast"]

        return short_forecast

    def get_detailed_forecast(self) -> str:
        """Get the current detailed weather forecast.

        Returns:
            str: Current detailed weather forecast.
        """
        detailed_forecast = self.weather_details["detailed_forecast"]

        return detailed_forecast

    def get_temperature_in_fahrenheit(self, temperature_unit: bool = False) -> Union[int, str]:
        """Get the current temperature in fahrenheit.

        Args:
            temperature_unit (bool): Indicate whether to include the temperature unit.

        Returns:
            int: Union[int, str]: Current temperature in Fahrenheit as an integer or a string with the unit.
        """
        temperature_in_fahrenheit = self.weather_details["temperature"]
        if temperature_unit:
            return f"{temperature_in_fahrenheit}F"

        return temperature_in_fahrenheit

    def get_temperature_in_celsius(self, temperature_unit: bool = False) -> Union[float, str]:
        """Get the current temperature in celsius.

        Args:
            temperature_unit (bool): Indicate whether to include the temperature unit.

        Returns:
            Union[float, str]: Current temperature in Celsius as a float or a string with the unit.
        """
        temperature_in_celsius = (self.weather_details["temperature"] - 32) / 1.8
        if temperature_unit:
            return f"{temperature_in_celsius}C"

        return f"{temperature_in_celsius:.2f}"

    def get_probability_of_precipitation(self) -> str:
        """Get the current probability of precipitation.

        Returns:
            str: Current probability of precipitation.
        """
        probability_of_precipitation = self.weather_details["probability_of_precipitation"]

        if probability_of_precipitation is None:
            return "0%"

        return f"{probability_of_precipitation}%"

    def get_wind(self) -> str:
        """Get the current wind speed and wind direction.

        Returns:
            str: Current wind speed and wind direction.
        """
        wind_speed = self.weather_details["wind_speed"]
        wind_direction = self.weather_details["wind_direction"]

        return f"{wind_speed} {wind_direction}"
