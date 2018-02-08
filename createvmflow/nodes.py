from copy import copy

from viewflow import Gateway, mixins, ThisObject
from viewflow.exceptions import FlowRuntimeError
from viewflow.activation import AbstractGateActivation
from viewflow.token import Token
from viewflow.flow import views

from .models import ProcessApproverAndAns


class ApproverSplitActivation(AbstractGateActivation):
    def calculate_next(self):
        self._approvers = self.flow_task.approvers_handler(self)

    def activate_next(self):
        if self._approvers:
            token_source = Token.split_token_source(
                self.task.token, self.task.pk)
            for user in self._approvers:
                next_task = self.flow_task._next.activate(
                    prev_activation=self, token=next(token_source))
                next_task.assign(user)
                self.update_approve_task(next_task.task)
        else:
            raise FlowRuntimeError("{} activated with zero nodes specified"
                                   .format(self.flow_task.name))

    def update_approve_task(self, task):
        obj = ProcessApproverAndAns.objects.get(process=self.process)
        obj.task = task
        obj.save()


class ApproverSplit(mixins.NextNodeMixin,
                    mixins.UndoViewMixin,
                    mixins.CancelViewMixin,
                    mixins.PerformViewMixin,
                    mixins.DetailViewMixin,
                    Gateway):
    """
    Activates several outgoing task instances depends on callback value
    Example::
        spit_on_decision = flow.ApproverSplit(lambda act: act.process.users) \\
            .Next(this.make_decision)
        make_decision = flow.View(MyView) \\
            .Next(this.join_on_decision)
        join_on_decision = flow.Join() \\
            .Next(this.end)
    """
    task_type = 'SPLIT'

    cancel_view_class = views.CancelTaskView
    detail_view_class = views.DetailTaskView
    perform_view_class = views.PerformTaskView
    undo_view_class = views.UndoTaskView

    activation_class = ApproverSplitActivation

    def __init__(self, approvers):
        super(ApproverSplit, self).__init__()
        self._approvers = approvers
        self._ifnone_next_node = None

    @property
    def approvers_handler(self):
        if isinstance(self._approvers, ThisObject):
            self._approvers = getattr(
                self.flow_class.instance, self._approvers.name)
        return self._approvers
