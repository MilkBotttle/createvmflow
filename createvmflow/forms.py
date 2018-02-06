from django import forms
from django.contrib.auth.models import Group, User

class AssignApproverForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=None, required=True)
    
    def __init__(self,*args,**kwargs):
        self.users = User.objects.filter(group__name='manager')
        self.fields['users'].queryset = self.users
