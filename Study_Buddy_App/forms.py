from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']


class TopicForm(forms.Form):
    name = forms.CharField(max_length=255, label='Topic name')


class TaskForm(forms.Form):
    name = forms.CharField(label='Task Name', max_length=255, required=True)
    deadline = forms.DateField(label='Deadline', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
