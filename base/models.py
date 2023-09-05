# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, max_length=500)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField('Created at:', auto_now_add=True)

    def __str__(self):
        return str(self.title).capitalize()

    class Meta:
        ordering = ['created_at']
