from django.db import models

class Comments(models.Model):
    """defining comments model
    """
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    deck = models.ForeignKey("Deck", on_delete=models.CASCADE)
    comments = models.CharField(max_length=1000)