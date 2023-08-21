from django.db import models

# Create your models here.


class MyModel(models.Model):
    class Meta:
        verbose_name = "MyModel"
        verbose_name_plural = "MyModels"

    def __str__(self):
        return self.id
