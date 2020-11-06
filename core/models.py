from django.db import models


class List(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)


class Card(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True)
    position = models.IntegerField()
    card_list = models.ForeignKey(List, on_delete=models.CASCADE)

    class Meta:
        ordering = ['position', '-updated_at']
