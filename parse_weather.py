import math
import requests
import logging.config
from lexicon import CODE_TO_SMILE

logging.config.fileConfig("config/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def get_weather(city: str, api_id: str) -> str:
    try:
        logger.info(f"Getting weather for {city}")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={api_id}"
        response = requests.get(url)
        weather_data = response.json()

        city_name = weather_data["name"]
        temperature = round(weather_data["main"]["temp"])
        feels_like = round(weather_data["main"]["feels_like"])
        weather_main = weather_data["weather"][0]["main"]
        weather_description = weather_data["weather"][0]["description"]
        wind_speed = round(weather_data["wind"]["speed"])
        pressure = math.ceil(weather_data["main"]["pressure"] / 1.333)
        humidity = weather_data['main']['humidity']

        result = (f"Погода на сегодня в городе {city_name}:\n"
                  f"Температура: {temperature}°C\n"
                  f"Ощущается как: {feels_like}°C\n"
                  f"{CODE_TO_SMILE.get(weather_main, '')} ({weather_description})\n"
                  f"Ветер: {wind_speed} м/с\n"
                  f"Давление: {pressure} мм.рт.ст\n"
                  f"Влажность: {humidity}%")

        return result
    except requests.RequestException as req_err:
        logger.error(f"Ошибка при запросе погоды: {req_err}")
        return "Неудалось получить данные (возможно некорректно введен город)"
    except KeyError as key_err:
        logger.error(f"Ошибка в данных погоды: {key_err}")
        return "Ошибка (возможно некорректно введен город)"
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return "Ошибка (повторите попытку)"
