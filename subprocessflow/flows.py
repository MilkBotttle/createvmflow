from django.utils.translation import ugettext_lazy as _

from viewflow import flow, frontend, lock
from viewflow.base import this, Flow
from viewflow.flow import views as flow_views

from . import models, views
from .subprocess_node import SubProcess, StartSubProcess

@frontend.register
class AddText(Flow):
    process_class =models.SubP
    task_class = models.SubT
    
    start = StartSubProcess().Next(this.inserttext)
    inserttext = flow.View(flow_views.UpdateProcessView, fields=['text']).Next(this.end)
    end = flow.End()



@frontend.register
class InSubprocessFlow(Flow):
    process_class = models.MainProcess
    task_class = models.MainTask

    start = (
        flow.Start(flow_views.CreateProcessView, fields=['text']).Next(this.sub_prorcess)
    )
    sub_prorcess = (
        SubProcess(AddText.start).Next(this.printtext)
    ) 
    printtext = (
        flow.Handler(this.printfunc).Next(this.end)
    )
    end = flow.End()
   
    def printfunc(self, activation):
        print(activation.process.text) 
