from django.db import models


class Week(models.Model):
    number = models.PositiveIntegerField()
    activities = models.TextField(blank=True)

    def __str__(self):
        return f"Week {self.number}"


class WorkDay(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="days")
    date = models.DateField(null=True, blank=True)
    schedule = models.CharField(max_length=100, blank=True)
    tutor_signature = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Day in week {self.week.number}"