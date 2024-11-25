from django.db import models

class Counter(models.Model):
    value = models.IntegerField(default=0)

    def increment(self):
        self.value += 1
        self.save()