from django import forms

class TargetDocumentForm(forms.Form):
	target_doc = forms.CharField(widget=forms.Textarea(
								attrs={ 'rows': 25, 
										'class': 'form-control', 
										'placeholder': 'Enter your text here',}), 
								label=''
								)
