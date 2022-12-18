from django.db import models

# Create your models here.

class Adminusers(models.Model):
    id = models.AutoField(primary_key=True)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=255)

    def __str__(self):
        return self.email

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Adminusers.objects.get(email=email)
        except:
            return False

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, blank=True, null=True, default=0)
    name = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True, default=0)
    returnable_item = models.BooleanField(default=False)
    upload_image = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True, default=0)
    dimensions = models.CharField(max_length=50, blank=True, null=True, default=0)
    manufacturer = models.CharField(max_length=50, blank=True, null=True, default=0)
    upc = models.IntegerField(default=True)
    ean = models.IntegerField(default=0)
    design = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    barcode_image = models.ImageField(blank=True, null=True)
    weight = models.IntegerField(default=0)
    brand = models.CharField(max_length=50, blank=True, null=True)
    mpn = models.CharField(max_length=50, blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    agency_charge = models.IntegerField(null = True)
    price_code = models.IntegerField(default=0)
    bar_code_image = models.BinaryField(null = True)
    sales_information = models.BooleanField(default=False)
    selling_price = models.IntegerField(default=0)
    sales_account = models.CharField(max_length=50, blank=True, null=True)
    sales_description = models.TextField(max_length=255, blank=True, null=True)
    purchase_information = models.BooleanField(default=False)
    cost_price = models.CharField(max_length=50, blank=True, null=True)
    purchase_account = models.CharField(max_length=50, blank=True, null=True)
    purchase_description = models.TextField(max_length=255, blank=True, null=True)
    track_inventory =models.BooleanField(default=False)
    inventory_account = models.CharField(max_length=50, blank=True, null=True)
    reorder_point = models.CharField(max_length=50, blank=True, null=True)
    preferred_vendor = models.CharField(max_length=50, blank=True, null=True)
    warehouse_name = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mstproject1_item"

    @staticmethod
    def get_id(id):
        try:
            return Item.objects.get(id=id)
        except:
            return False




    
    


    