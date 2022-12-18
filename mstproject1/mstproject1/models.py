from django.db import models

class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    password=models.CharField(max_length=255)
    mobile_number=models.CharField(max_length=50)
    mobile_verification_status=models.IntegerField()
    email=models.CharField(max_length=50)
    email_verification_status=models.IntegerField()
    pin_code=models.IntegerField()
    locality=models.TextField(max_length=50)
    address=models.TextField(max_length=255)
    address_type=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    landmark=models.CharField(max_length=255)
    alternate_phone=models.CharField(max_length=50)
    

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customers.objects.get(email=email)
        except:
            return False