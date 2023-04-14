from django.db import models


# Create your models here.
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=6)
    profile_image = models.ImageField(upload_to='images', null=True)  # images stored in src/media/images

    def __str__(self):
        # to string object
        return f"{self.first_name} {self.last_name}"

