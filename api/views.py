from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from viewflow.models import Process, Task, SubProcess, SubProcessTask
from .serializers import ProcessSerializer
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route
from rest_framework import viewsets

class ProcessViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


class FlowListViewSet(viewsets.ViewSet):
	pass
