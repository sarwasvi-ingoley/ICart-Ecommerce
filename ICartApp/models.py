from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=200)
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    #linking Subcategory with Category
    category=models.ForeignKey(Category, on_delete=models.CASCADE)


class Color(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class FilterPrice(models.Model):
    FILTER_PRICE = (
        ('> 500', '> 500'),
        ('500 to 2000', '500 to 2000'),
        ('2000 to 5000', '2000 to 5000'),
        ('5000 to 10000', '5000 to 10000'),
        ('10000 to 50000', '10000 to 50000'),
        ('50000 <', '50000 <'),
    )
    price = models.CharField(choices=FILTER_PRICE, max_length=60)
    def __str__(self):
        return self.price

class Product(models.Model):
    STOCK=(('Instock', 'Instock'), ('Out of Stock', 'Out of Stock'))
    STATUS=(('Publish', 'Publish'), ('Draft', 'Draft'))
    CONDITION=(('New', 'New'), ('Old', 'Old'))
    product_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image=models.ImageField(upload_to='ProductImages/images')
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    condition=models.CharField(choices=CONDITION, max_length=200)
    annotations=models.TextField() # product attributes such as color, type, brand etc. semicolon separated
    description=models.TextField()
    stock=models.CharField(choices=STOCK, max_length=200)
    status=models.CharField(choices=STATUS, max_length=200) # if we publish it, that product would be visible for all. If we keep it as draft, then it won't be visible for all
    created_on=models.DateTimeField(default=timezone.now)

    #linking product with foreign keys
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    color=models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price=models.ForeignKey(FilterPrice, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.product_id is None and self.created_on and self.id:
            self.product_id=self.created_on.strftime('90%Y%m%d23')+str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Images(models.Model):
    image=models.ImageField(upload_to='ProductImages/images')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)

class ImageUpload(models.Model):
    user_image=models.ImageField(upload_to='static/uploaded')
    def __str__(self) -> str:
        return self.image.url
    

