from datetime import date
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .forms import RegisterForm

PU_SHKINO_LAT = 56.01
PU_SHKINO_LON = 37.85


def weather_description(code):
    mapping = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Инейный туман",
        51: "Лёгкая морось",
        61: "Небольшой дождь",
        63: "Дождь",
        71: "Небольшой снег",
        80: "Ливень",
        95: "Гроза",
    }
    return mapping.get(code, "Погода уточняется")


def get_weather_from_api():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": PU_SHKINO_LAT,
        "longitude": PU_SHKINO_LON,
        "current": "temperature_2m,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,weathercode",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "Europe/Moscow",
        "forecast_days": 7,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password1'])
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Неверное имя пользователя или пароль.'

    return render(request, 'auth/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    data = get_weather_from_api()

    if data:
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})

        weather_hour = {
            "temperature": current.get("temperature_2m", 18),
            "description": "Текущая погода",
            "humidity": "60",
            "wind_speed": current.get("wind_speed_10m", 3),
        }

        weather_day = {
            "temperature": daily.get("temperature_2m_max", [20])[0],
            "description": weather_description(daily.get("weathercode", [2])[0]),
            "humidity": hourly.get("relative_humidity_2m", [60])[0] if hourly.get("relative_humidity_2m") else 60,
            "wind_speed": hourly.get("wind_speed_10m", [3])[0] if hourly.get("wind_speed_10m") else 3,
        }

        week_forecast = []
        for i in range(min(7, len(daily.get("time", [])))):
            week_forecast.append({
                "date": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "description": weather_description(daily["weathercode"][i]),
            })

        if not week_forecast:
            week_forecast = [
                {"date": "Сегодня", "temp_max": 20, "temp_min": 12, "description": "Переменная облачность"},
                {"date": "Завтра", "temp_max": 21, "temp_min": 13, "description": "Ясно"},
                {"date": "Послезавтра", "temp_max": 19, "temp_min": 11, "description": "Небольшой дождь"},
            ]
    else:
        weather_hour = {
            "temperature": 18,
            "description": "Ясно",
            "humidity": 60,
            "wind_speed": 3,
        }
        weather_day = {
            "temperature": 20,
            "description": "Переменная облачность",
            "humidity": 58,
            "wind_speed": 4,
        }
        week_forecast = [
            {"date": "Сегодня", "temp_max": 20, "temp_min": 12, "description": "Переменная облачность"},
            {"date": "Завтра", "temp_max": 21, "temp_min": 13, "description": "Ясно"},
            {"date": "Послезавтра", "temp_max": 19, "temp_min": 11, "description": "Небольшой дождь"},
            {"date": "Четверг", "temp_max": 18, "temp_min": 10, "description": "Пасмурно"},
            {"date": "Пятница", "temp_max": 22, "temp_min": 14, "description": "Ясно"},
            {"date": "Суббота", "temp_max": 23, "temp_min": 15, "description": "Преимущественно ясно"},
            {"date": "Воскресенье", "temp_max": 20, "temp_min": 12, "description": "Облачно"},
        ]

    return render(request, 'weather/home.html', {
        'weather_hour': weather_hour,
        'weather_day': weather_day,
        'week_forecast': week_forecast,
        'today': date.today(),
        'city': 'Пушкино',
    })