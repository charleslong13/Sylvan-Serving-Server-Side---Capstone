from django.db import models

class Event(models.Model):
    """defining event Model
    """
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    organizer = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='organizing')
    attendees = models.ManyToManyField("Player", through="EventPlayer", related_name="attending")
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value