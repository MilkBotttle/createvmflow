from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from viewflow.flow.views import FlowMixin
from . import models, forms


class AssignApproverView(FlowMixin, generic.FormView):
    form_class = forms.AssignApproverForm

    def form_valid(self, form):
        for user in form.cleaned_data.get('users'):
            self.object = models.ProcessApproverAndAns()
            self.object.process = self.activation.process
            self.object.user = user
            self.object.save()

        self.success('Assign approver complete')
        self.activation.done()
        return HttpResponseRedirect(self.get_success_url())


class ApproveView(FlowMixin, generic.UpdateView):
    model = models.ProcessApproverAndAns
    fields = ['approve']

    def get_object(self):
        # This is will be task.owner != approverans obj user
        return models.ProcessApproverAndAns.objects.get(
            task=self.activation.task, process=self.activation.process)
