from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from debt.models import Debt

class Bluser(User):
	class Meta:
		proxy = True
	def __unicode__(self):
		return self.first_name

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="alert-message error">%s</div>' % e for e in self])

class DebtForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DebtForm, self).__init__(*args, **kwargs)
        self.error_class = DivErrorList
	self.fields['payee'].queryset = Bluser.objects.all()
	self.fields['payer'].queryset = Bluser.objects.all()
    class Meta:
        model = Debt

class DebtMulti(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DebtMulti, self).__init__(*args, **kwargs)
        self.error_class = DivErrorList
    payee = forms.ModelChoiceField(queryset=Bluser.objects.all())
    payers = forms.ModelMultipleChoiceField(queryset=Bluser.objects.all(),widget=forms.CheckboxSelectMultiple())
    amount = forms.IntegerField(label="Amount to Split")
    memo = forms.CharField(widget=forms.Textarea)

    
