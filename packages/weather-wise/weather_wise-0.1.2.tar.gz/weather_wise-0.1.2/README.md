# Weather Wise

## Overview

Get the current weather forecast and other weather related information from a zipcode.  This module uses the U.S. Census 2022 Gazetteer (Zip Code Tabulation Areas).  The original file has been modified to JSON.

## Usage

```python
import json
from weather_wise.weather_wise import Weather

weather = Weather("32904")

# Internal weather methods.
print(weather._load_json_data())
print(weather._get_latitude_longitude())
print(weather._get_weather_forecast_url())
print(json.dumps(weather._get_weather_data(), indent=2))

# Get the short forecast.
short_forecast = weather.get_short_forecast()
print(short_forecast)

# Get the detailed forecast.
detailed_forecast = weather.get_detailed_forecast()
print(detailed_forecast)

# Get the temperature in fahrenheit.
temperature_in_fahrenheit = weather.get_temperature_in_fahrenheit(temperature_unit=True)
print(temperature_in_fahrenheit)

# Get the temperature in celsius.
temperature_in_celsius = weather.get_temperature_in_celsius()
print(temperature_in_celsius)

# Get the chance of rain.
chance_of_rain = weather.get_probability_of_precipitation()
print(chance_of_rain)

# Get the wind.
wind = weather.get_wind()
print(wind)
```

## References

- ### Gazetteer Files

  - <https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html>

- ### API Documentation

  - <https://www.weather.gov/documentation/services-web-api>

- ### API Discussion

  - <https://github.com/weather-gov/api/discussions>

- ### Outage & Status Messages

  - <https://www.nco.ncep.noaa.gov/status/messages/>

## TODO

- Get severe weather alerts.
  - Active Alerts
    - <https://api.weather.gov/alerts/active?point=38.9807,-76.9373>
  - All Alerts
    - <https://api.weather.gov/alerts?point=38.9807,-76.9373>
