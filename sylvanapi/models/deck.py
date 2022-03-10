from django.db import models

class Deck(models.Model):
    """Defining the deck model 
    """
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    play_style = models.ForeignKey("PlayStyle", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    commander = models.CharField(max_length=1000)
    creatures = models.CharField(max_length=1000)
    artifacts = models.CharField(max_length=1000)
    enchantments = models.CharField(max_length=1000)
    instants = models.CharField(max_length=1000)
    sorceries = models.CharField(max_length=1000)
    lands = models.CharField(max_length=3000)
    wins = models.IntegerField(max_length=500)
    losses = models.IntegerField(max_length=500)
    powerLevel = models.IntegerField(max_length=10)
    primer = models.CharField(max_length=5000)