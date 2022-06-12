from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class PetroleumProduct(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Year(models.Model):
    date = models.CharField(max_length=15)
    
    def __str__(self):
        return self.date

class Detail(models.Model):
    year = models.ForeignKey(Year, on_delete = models.CASCADE,related_name="year", null = True)
    petroleum_product = models.ForeignKey(PetroleumProduct, on_delete = models.CASCADE,related_name="petroleum_product", null = True)
    sale = models.CharField(max_length = 15)
    country = models.ForeignKey(Country, on_delete = models.CASCADE, related_name='country', null=True)
    
    def __str__(self):
        return self.petroleum_product.name