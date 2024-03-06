# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weather_wise']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'weather-wise',
    'version': '0.1.2',
    'description': 'Obtain local weather information based on zipcode.',
    'long_description': '# Weather Wise\n\n## Overview\n\nGet the current weather forecast and other weather related information from a zipcode.  This module uses the U.S. Census 2022 Gazetteer (Zip Code Tabulation Areas).  The original file has been modified to JSON.\n\n## Usage\n\n```python\nimport json\nfrom weather_wise.weather_wise import Weather\n\nweather = Weather("32904")\n\n# Internal weather methods.\nprint(weather._load_json_data())\nprint(weather._get_latitude_longitude())\nprint(weather._get_weather_forecast_url())\nprint(json.dumps(weather._get_weather_data(), indent=2))\n\n# Get the short forecast.\nshort_forecast = weather.get_short_forecast()\nprint(short_forecast)\n\n# Get the detailed forecast.\ndetailed_forecast = weather.get_detailed_forecast()\nprint(detailed_forecast)\n\n# Get the temperature in fahrenheit.\ntemperature_in_fahrenheit = weather.get_temperature_in_fahrenheit(temperature_unit=True)\nprint(temperature_in_fahrenheit)\n\n# Get the temperature in celsius.\ntemperature_in_celsius = weather.get_temperature_in_celsius()\nprint(temperature_in_celsius)\n\n# Get the chance of rain.\nchance_of_rain = weather.get_probability_of_precipitation()\nprint(chance_of_rain)\n\n# Get the wind.\nwind = weather.get_wind()\nprint(wind)\n```\n\n## References\n\n- ### Gazetteer Files\n\n  - <https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html>\n\n- ### API Documentation\n\n  - <https://www.weather.gov/documentation/services-web-api>\n\n- ### API Discussion\n\n  - <https://github.com/weather-gov/api/discussions>\n\n- ### Outage & Status Messages\n\n  - <https://www.nco.ncep.noaa.gov/status/messages/>\n\n## TODO\n\n- Get severe weather alerts.\n  - Active Alerts\n    - <https://api.weather.gov/alerts/active?point=38.9807,-76.9373>\n  - All Alerts\n    - <https://api.weather.gov/alerts?point=38.9807,-76.9373>\n',
    'author': 'Aaron Britton',
    'author_email': 'brittonleeaaron@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
