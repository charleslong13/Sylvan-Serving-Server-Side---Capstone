from django.db import models

class EventPlayer(models.Model):
    """defining attendees model
    """
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
