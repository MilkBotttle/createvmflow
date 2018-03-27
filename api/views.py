import json
from django.utils.timezone import now 
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from viewflow.models import Process, Task, SubProcess, SubProcessTask
from .serializers import ProcessSerializer, FlowSerializer
from rest_framework import viewsets
from django.apps import apps
from rest_framework import generics
from django.utils.decorators import method_decorator
from .utils import get_next_task_url
from viewflow.decorators import flow_start_view
import datetime
class ProcessViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer



@api_view(['GET'])
def flow_list(request):
    serializers_class = FlowSerializer 
    if request.method == 'GET':
        api = apps.get_app_config('api')
        flows = api.flows
        return Response(FlowSerializer(flows,many=True).data)

class RestFlowViewSet(viewsets.ViewSet):
    flows = apps.get_app_config('api').flows
    serializer_class = FlowSerializer

    def list(self, request, format=None):
        """
        GET/ Return all flows title
        """
        flows_titles = [flow.process_title for flow in api.flows]
        return Response(flows_titles)

    def start(self, requst):
        """
        POST/
        """

class BaseStartFlowMixin(object):
    """ Mixin for start api."""
    def get_success_url(self):
        return get_next_task_url(self.request, self.activation.process)

    @method_decorator(flow_start_view)
    def dispatch(self ,request, **kwargs):
        """Check user permissions, and prepare flow for execution."""
        self.activation = request.activation
        import ipdb
        ipdb.set_trace()
        data = json.loads(request.body)
        data['_viewflow_activation-started']=now()
        self.activation.prepare(data or None, user=request.user)
        if not self.activation.has_perm(request.user):
            raise PermissionDenied
        
        #kwargs['flow_class'] = self.activation.flow_class.__name__
        #kwargs['status'] = self.activation.status
        return super().dispatch(request, **kwargs)

class CreateProcessView(BaseStartFlowMixin, generics.UpdateAPIView):
    """POST create a new process"""
    serializer_class = ProcessSerializer()

#    @property
#    def queryset(self):
#        return self.activation.flow_calss.process_class.objects.all()

#    def get_objcet(self): #override get_object don't need queryset(?)
#        return self.activation.process
    
    def activation_done(self, *args, **kwargs):
        """Finish task activation"""
        self.activation.done()

    def get_serializer_class(self):
        """Get serializer class and set process model"""
        ProcessSerializer.Meta.model = self.activation.flow_class.process_class
        return ProcessSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        #kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """compelete start task."""
        #valid data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rr = self.activation_done(*args, **kwargs)
            import ipdb
            ipdb.set_trace()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class FlowListView(APIView):
#    """GET list all flows"""
#    pass        
#    
        
        
    
