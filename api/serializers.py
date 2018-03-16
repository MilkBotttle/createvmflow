from rest_framework import serializers
from viewflow.models import Process, Task, SubProcess, SubProcessTask

from rest_framework import serializers

class ProcessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        fields = ('__all__')
