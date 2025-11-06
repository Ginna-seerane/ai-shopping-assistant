from django.db import models

class SARetailer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    delivery_time = models.CharField(max_length=50)
    min_order = models.DecimalField(max_digits=10, decimal_places=2)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    retailer = models.ForeignKey(SARetailer, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    barcode = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.retailer.name}"
    
    @property
    def availability_text(self):
        if self.in_stock and self.stock_quantity > 0:
            return f"In stock ({self.stock_quantity} available)"
        return "Out of stock"
    
    @property
    def delivery_info(self):
        return f"Delivery: {self.retailer.delivery_time}, Min order: R{self.retailer.min_order}"