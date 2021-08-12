from django.db import models
from django.conf import settings
from django.urls import reverse


class TimesheetModel(models.Model):
    """ TimeSheet model """
    date = models.DateField(auto_now=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.author} - {self.date} - ({self.from_hour} - {self.to_hour})"

    def get_absolute_url(self):
        return reverse('overview_timesheet')

