"""
By default, Django signals run in the same database transaction as the caller. 
This means that the signal handler and the caller are part of the same transaction. 
If the caller's transaction is rolled back, the signal's database operations will also be rolled back.
"""


from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class MyModel(models.Model):
    name = models.CharField(max_length=100)

class AnotherModel(models.Model):
    description = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal receiver running and modifying AnotherModel")
    AnotherModel.objects.create(description="Created from signal")

def test_signal():
    try:
        with transaction.atomic():
            print("Before saving the model")
            instance = MyModel.objects.create(name="Test")
            print("Model saved")

            raise ValidationError("Forcing transaction rollback!")
            
    except ValidationError:
        print("Transaction rolled back due to exception")

    print("AnotherModel entries:", AnotherModel.objects.all())

# Expected output as follows:

Before saving the model
Signal receiver running and modifying AnotherModel
Transaction rolled back due to exception
AnotherModel entries: <QuerySet []>