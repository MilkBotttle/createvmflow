from django.db import models

from viewflow.models import Process, Task, SubProcess, SubProcessTask

class MainProcess(Process):
    text = models.CharField(max_length=150)

class MainTask(Task):
    """MainTask"""

class SubP(SubProcess):
    text = models.CharField(max_length=150)

class SubT(SubProcessTask):
    """SubTask"""
