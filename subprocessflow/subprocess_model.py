from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from viewflow.activation import STATUS, STATUS_CHOICES
from viewflow.fields import FlowReferenceField
from viewflow.models import AbstractProcess, AbstractTask

class SubProcess(AbstractProcess):
    """Default SubProcess Process"""
    parent_process= models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        verbose_name=_('ParentProcess'))

    class Meta:  # noqa D101
        ordering = ['-created']
        verbose_name = _('SubProcess')
        verbose_name_plural = _('SubProcess list')

class SubProcessTask(AbstractTask):
    """ Default SubProcess Task"""
    process = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        verbose_name=_('SubProcess'))

    class Meta:  # noqa D101
        verbose_name = _('SubTask')
        verbose_name_plural = _('SubTasks')
        ordering = ['-created']
