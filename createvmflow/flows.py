from django.utils.translation import ugettext_lazy as _

from viewflow import flow, frontend, lock
from viewflow.base import this, Flow
from viewflow.flow import views as flow_views

from . import models, views

class CreatevmFlow(Flow):
    process_class = models.CreatevmProcess
    task_class =    models.CreatvmTask
 
    start = (
        flow.Start(flow_views.CreateProcessView,fields=['order_username','cpu_cores','disk_size','memory_size','os_type'])
            .Permission('createvmflow.can_start_request')
            .Next(this.assign_approve)
    )

    assign_approve = (
        flow.View(views.AssignApproverView)
            .Permission('createvmflow.can_assign_approver')
            .Next(this.make_approve)
    )

    make_approve = (
        flow.View(views.ApproveView)
            .Permission('createvmflow.can_approve_request')
            .Next(this.check_approve)
    )

    check_approve = (
        flow.Handler(this.caculate_approve)
            .Next(this.provision_or_reject)
    )
    
    provision_or_reject = (
       flow.End() 
    )
    #provision_or_reject = (
    #    flow.Handler(this.provision)
    #        .Next(this.end)
    #)

    end = flow.End()

    def provision(self, activation, **kwargs):
        pass
    def caculate_approve(self, activation, **kwargs):
        pass
