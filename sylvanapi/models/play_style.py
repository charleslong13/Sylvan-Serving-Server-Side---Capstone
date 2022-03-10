from django.db import models

class PlayStyle(models.Model):
    """Defining playstyle model
    """
    label = models.CharField(max_length=50)
