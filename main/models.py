from django.db import models

# Create your models here.
class Main(models.Model):
    page_width      = models.IntegerField(default=227)
    page_higth      = models.IntegerField(default=1350)
    padding         = models.IntegerField(default=9)
    font            = models.FileField(upload_to="media", null=True, blank=True)
    font_size       = models.IntegerField(default=12)
    toko            = models.CharField(default="Toko Kue", max_length=100)
    def __str__(self):
        return self.toko
        