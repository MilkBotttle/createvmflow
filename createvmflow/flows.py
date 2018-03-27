from django.utils.translation import ugettext_lazy as _

from viewflow import flow, frontend, lock
from viewflow.base import this, Flow
from viewflow.flow import views as flow_views
import api
from . import models, views, nodes

@api.register
@frontend.register
class CreatevmFlow(Flow):
    process_class = models.CreatevmProcess
    task_class = models.CreatvmTask

    start = (
        flow.Start(flow_views.CreateProcessView, fields=[
            'username',
            'cpu_cores',
            'disk_size',
            'memory_size',
            'os_type'])
        .Permission('createvmflow.can_start_request')
        .Next(this.assign_approve)
    )

    assign_approve = (
        flow.View(views.AssignApproverView)
            .Permission('createvmflow.can_assign_approver')
            .Next(this.make_approver_task)
    )

    make_approver_task = (
        nodes.ApproverSplit(this.approvers_handler)
             .Next(this.make_approve)
    )

    make_approve = (
        flow.View(views.ApproveView)
            .Permission('createvmflow.can_approve_request')
            .Next(this.check_approve)
    )
    check_approve = (
        flow.If(this.caculate_approve)
            .Then(this.provision_instance)
            .Else(this.reject)
    )

    provision_instance = (
        flow.Handler(this.provision_fun)
            .Next(this.end)
    )

    reject = (
        flow.Handler(this.reject_fun)
            .Next(this.end)
    )

    end = flow.End()

    def provision_fun(self, activation, *args, **kwargs):

        print("Provision request sended")

    def caculate_approve(self, activation):
        answers = activation.process.processapproverandans_set.all()
        for ans in answers:
            if not ans.approve:
                return False
        return True

    def reject_fun(self, activation, **kwargs):

        print("Provision request reject")

    def approvers_handler(self, activation):
        approvers = activation.process.processapproverandans_set.all()
        users = []
        for user in approvers:
            users.append(user.user)
        return users
