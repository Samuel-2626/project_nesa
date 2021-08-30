from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class NewsletterForm(forms.Form):
  name = forms.CharField(required=True, max_length=100)
  email_address = forms.EmailField(required=True)


