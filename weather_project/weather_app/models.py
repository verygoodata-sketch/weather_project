from django.db import models

class WeatherRecord(models.Model):
    PERIOD_CHOICES = [
        ('hour', 'На ближайший час'),
        ('day', 'На день'),
        ('week', 'На неделю'),
    ]

    city = models.CharField(max_length=100, default='Пушкино')
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    date = models.DateField()
    temperature = models.IntegerField()
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()

    def __str__(self):
        return f"{self.city} — {self.get_period_display()} — {self.date}"