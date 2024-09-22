"""
Django signals run in the same thread as the caller. This means that the function connected to the signal
is executed in the same thread where the signal was sent.
"""

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_receiver(sender, instance, **kwargs):
    print(f"Signal receiver running in thread: {threading.get_ident()}")

def test_signal():
    print(f"Signal sender running in thread: {threading.get_ident()}")
    instance = MyModel.objects.create(name="Test")

# Expected output as follows:

Signal sender running in thread: 140715153729280
Signal receiver running in thread: 140715153729280