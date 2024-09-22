"""
By default, Django signals are executed synchronously. 
This means that the receiver function connected to a signal will be executed immediately when the signal is sent, 
blocking further code execution until the signal receiver is finished.
"""

import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal receiver started")
    time.sleep(5)
    print("Signal receiver finished")

def test_signal():
    print("Before saving the model")
    instance = MyModel.objects.create(name="Test")
    print("After saving the model")

# Expected output as follows:

Before saving the model
Signal receiver started
Signal receiver finished
After saving the model