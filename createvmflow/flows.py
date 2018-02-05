from django.utils.translation import ugettext_lazy as _

from viewflow import flow, frontend, lock
from viewflow.base import this, Flow
from viewflow.flow import views as flow_views

class CreatevmFlow(Flow):
    process_class = CreatevmProcess
    
    start = (
        flow.Start(StartCreatevmView)
            .Next(this.assign_approve)
            
    )

    assign_approve = (
        flow.View(AssignApproverView)
            .Permission()
            .Next(this.make_approve)
    )

    make_approve = (
        
    )

    check_approve = ()
    

    provision_instance = (
        flow.Handler(this.provision)
            .Next(this.end)
    )

    end = flow.End()

    def provision(self, activation, **kwargs):
        pass    
