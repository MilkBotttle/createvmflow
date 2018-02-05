from django.db import models

from viewflow.models import Process

class CreatevmProcess(Process):
    order_username = models.CharField(max_length=150)
    order_cpu = models.PositiveIntegerField(default=0)
    order_disk = models.PositiveIntegerField(default=0)
    order_memory = models.PositiveIntegerField(default=0)
    order_os = models.CharField(max_length=50)

class ProcessApprovers(models.Model):
    
