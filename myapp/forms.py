from django import forms
from django.db.models import fields
from .models import Document,Document_ATS

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
        widgets = {
            'filename': forms.HiddenInput(),
        }

class ATS_Form(forms.ModelForm):
    class Meta:
        model = Document_ATS
        fields = ('document','content')
        widgets = {
            'filename': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 30}),
        }