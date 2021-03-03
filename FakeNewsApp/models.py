from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

class Dominio(models.Model):
    CONFID_CHOICES = (
    ('C', 'Confiable'),
    ('I', 'Intermedio'),
    ('N', 'No confiable')
    )
    url= models.TextField()
    confianza = models.IntegerField(default=50, validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    blacklist = models.CharField(choices=CONFID_CHOICES, max_length=128)

    def publish(self):
        self.save()

    def __str__(self):
        return self.url

class Verbo(models.Model):

    verbo= models.TextField()
    radicalRegular= models.TextField(null=True, blank=True)
    radicalIrrecular_0= models.TextField(null=True, blank=True)
    radicalIrrecular_1= models.TextField(null=True, blank=True)



    def publish(self):
        self.save()

    def __str__(self):
        return self.radicalRegular