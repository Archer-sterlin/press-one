from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"
