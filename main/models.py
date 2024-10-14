from django.db import models

# Create your models here.
class Main(models.Model):
    page_width      = models.IntegerField(default=227)
    page_higth      = models.IntegerField(default=1350)
    padding         = models.IntegerField(default=9)
    font            = models.FileField(upload_to="media", null=True, blank=True)
    font_size       = models.IntegerField(default=12)
    toko            = models.CharField(default="Toko Kue", max_length=100)
    brand           = models.CharField(default="Brand Test", max_length=100)
    alamat          = models.CharField(max_length=225, null=True, blank=True)
    telp            = models.CharField(max_length=225, blank=True, null=True)
    ucapan          = models.TextField(blank=True, null=True)
    wifi            = models.CharField(max_length=225, blank=True, null=True)
    password_wifi   = models.CharField(max_length=225, blank=True, null=True)
    utama           = models.BooleanField(default=False)
    
    def __str__(self):
        return self.toko

class FieldMenu(models.Model):
    main            = models.ForeignKey(Main, on_delete=models.CASCADE, blank=True, null=True)
    urutan          = models.IntegerField()
    nama            = models.CharField(max_length=225, blank=True, null=True)
    def __str__(self):
        return str(self.urutan) + ". "+self.nama

