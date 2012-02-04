from django.contrib.auth.models import User
from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django import forms

class Announcement(models.Model):
    poster = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    class Meta:
        ordering = ["-date"]

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        exclude = ('date')
        widgets = {
            'poster':HiddenInput(),
        }

MEDIUMS = (
    (1,"sms"),
    (2,"email")
)

class Bluser(User):
	class Meta:
		proxy = True
	def __unicode__(self):
		return self.first_name

class SendForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(queryset=Bluser.objects.all(),widget=forms.CheckboxSelectMultiple())
    medium = forms.MultipleChoiceField(choices=MEDIUMS,widget=forms.CheckboxSelectMultiple())
