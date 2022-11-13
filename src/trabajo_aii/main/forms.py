# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')
    
class TermsForm(forms.Form):
    terms = forms.CharField(label='Términos')