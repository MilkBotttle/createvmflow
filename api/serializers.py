from rest_framework import serializers
from viewflow.models import Process, Task, SubProcess, SubProcessTask
from viewflow import fields
from rest_framework import serializers

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        exclude = ('flow_class',)

class FlowSerializer(serializers.Serializer):
    
    #title = serializers.SerializerMethodField('get_process_title')
    process_title = serializers.CharField()
    start = serializers.SerializerMethodField('get_start_url')
    def get_start_url(self, start):
        pass
    def get_process_title(self,obj):
        return obj.process_title
