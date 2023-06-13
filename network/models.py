from django.core.exceptions import ValidationError
from django.db import models


class Contact(models.Model):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Product(models.Model):
    title = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    date_release = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Provider(models.Model):
    class Types(models.IntegerChoices):
        Factory = 0, 'Factory'
        RetailNetwork = 1, 'Retail network'
        IE = 2, 'Individual Entrepreneur'

    title = models.CharField(max_length=50, unique=True)
    type = models.PositiveSmallIntegerField(choices=Types.choices, default=0)
    level = models.SmallIntegerField(default=0)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='providers')
    debt = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'

    def save(self, *args, **kwargs):
        if not self.supplier:
            self.level = 0
        else:
            self.level = self.supplier.level + 1
        super().save(*args, **kwargs)

    def clean(self):
        if self.type == 0 and self.supplier:
            raise ValidationError(f"{self} is a factory and cannot have suppliers.")
        if self.supplier and self.supplier.level == 2:
            raise ValidationError(f"{self.supplier} cannot be a supplier for {self}, because their level is 2.")

    def __str__(self):
        return self.title
