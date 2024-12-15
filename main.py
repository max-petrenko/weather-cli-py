import requests
import click
from termcolor import colored
import time
import sys
import os

API_URL = "https://api.openweathermap.org/data/2.5/weather"

WEATHER_ICONS = {
    "clear": "\u2600",  # ☀
    "clouds": "\u2601",  # ☁
    "rain": "\u2614",  # ☂
    "snow": "\u2744",  # ❄
    "thunderstorm": "\u26A1",  # ⚡
    "mist": "\u1F32B"  # 🌫
}

COLORS = {
    "clear": "yellow",
    "clouds": "white",
    "rain": "blue",
    "snow": "cyan",
    "thunderstorm": "magenta",
    "mist": "grey"
}

@click.command()
@click.option('--api-key', default=lambda: os.getenv('WEATHER_API_KEY'), prompt='Your OpenWeatherMap API key', help='API key for OpenWeatherMap.')
@click.option('--city', default=None, help='City name (e.g., London).')
@click.option('--lat', default=None, type=float, help='Latitude for your location.')
@click.option('--lon', default=None, type=float, help='Longitude for your location.')
def get_weather(api_key, city, lat, lon):
    """Display current weather information."""

    if not city and (lat is None or lon is None):
        click.echo("You must provide either a city name or latitude and longitude coordinates.")
        return

    params = {
        'appid': api_key,
        'units': 'metric',
    }

    if city:
        params['q'] = city
    else:
        params['lat'] = lat
        params['lon'] = lon

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

        # Extract weather condition
        condition = weather_data['weather'][0]['main'].lower()
        icon = WEATHER_ICONS.get(condition, "?")
        color = COLORS.get(condition, "white")

        # Display the weather information with color and icons
        click.echo(colored(f"Weather in {weather_data['name']}:", attrs=['bold']))
        click.echo(colored(f"  {icon} Temperature: {weather_data['main']['temp']} °C", color))
        click.echo(colored(f"  {icon} Condition: {weather_data['weather'][0]['description'].capitalize()}", color))
        click.echo(colored(f"  {icon} Humidity: {weather_data['main']['humidity']}%", color))
        click.echo(colored(f"  {icon} Wind Speed: {weather_data['wind']['speed']} m/s", color))

        # Simple animation for better UX
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.5)
        click.echo(" Done!")

    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching weather data: {e}")

if __name__ == '__main__':
    get_weather()
