from django import forms

class TargetDocumentForm(forms.Form):
	target_doc = forms.CharField(max_length=1000)
