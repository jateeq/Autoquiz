from django import forms

# Upper bound on submitted text. The bound keeps a single request from tying up the
# summarization step once that step exists; roughly 100 printed pages of prose.
MAX_DOCUMENT_CHARS = 200_000


class TargetDocumentForm(forms.Form):
    target_doc = forms.CharField(
        label="Text to study",
        max_length=MAX_DOCUMENT_CHARS,
        strip=True,
        widget=forms.Textarea(
            attrs={
                "rows": 20,
                "class": "form-control",
                "placeholder": "Paste a chapter, article, or notes here",
            }
        ),
    )
