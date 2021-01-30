from django.db import models
from django.conf import settings


class Food(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField()

    def __str__(self):
        return self.name


class Fridge(models.Model):
    foods = models.ManyToManyField(Food, through="FridgeFood")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class FridgeFood(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.IntegerField()
