class WeatherConstants:
    WEATHER_CACHE_TTL = 1800  # 30 minutes

    WEATHER_CONDITION_CHOICES = (
        ("clear sky", "Clear sky"),
        ("few clouds", "Few clouds"),
        ("scattered clouds", "Scattered clouds"),
        ("broken clouds", "Broken clouds"),
        ("shower rain", "Shower rain"),
        ("rain", "Rain"),
        ("thunderstorm", "Thunderstorm"),
        ("snow", "Snow"),
        ("mist", "Mist"),
    )
