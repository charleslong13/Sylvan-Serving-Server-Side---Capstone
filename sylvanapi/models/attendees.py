from django.db import models

class Attendees(models.Model):
    """defining attendees model
    """
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
