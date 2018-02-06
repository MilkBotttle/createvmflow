from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from viewflow.flow.views import FlowMixin
from . import models, forms


class AssignApproverView(FlowMixin, generic.FormView):
    form_class = forms.AssignApproverForm

    def form_valid(self, form):
        for user in form.cleaned_data.get('users'):
            self.object = models.ProcessApproverAndAns.save(commit=False)
            self.object.process = self.activation.process
            self.object.user = form.cleaned_data.get('users')
            self.object.save()

        self.success('Assign approver complete')
        self.activation.done()
        return HttpResponseRedirect(self.get_success_url())


class ApproveView(FlowMixin, generic.UpdateView):
    model = models.ProcessApproverAndAns
    fields = ['approve']

    def get_objects(self):
        owner = self.activation.process.owner()
        return self.model.filter(username=owner.username)
