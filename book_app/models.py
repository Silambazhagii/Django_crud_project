from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    published_date = models.DateField()
    # cover = models.ImageField(upload_to='covers/', null=True, blank=True)



    def __str__(self):
        return self.title