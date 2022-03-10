from django.db import models

class Deck(models.Model):
    """Defining the deck model 
    """
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    playStyle = models.ForeignKey("PlayStyle", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    commander = models.CharField(max_length=1000)
    creatures = models.CharField(max_length=1000)
    artifacts = models.CharField(max_length=1000)
    enchantments = models.CharField(max_length=1000)
    instants = models.CharField(max_length=1000)
    sorceries = models.CharField(max_length=1000)
    lands = models.CharField(max_length=3000)
    wins = models.IntegerField()
    losses = models.IntegerField()
    powerLevel = models.IntegerField()
    primer = models.CharField(max_length=5000)