import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
import simplejson
from sms.models import ContentTypePhoneNumber
from debt.models import *
from grocery.models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.forms.models import modelformset_factory, BaseFormSet, BaseModelFormSet

def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))
    
class BaseItemFormSet(BaseModelFormSet):
	def add_fields(self,form,index):
		super(BaseItemFormSet,self).add_fields(form,index)
		form.fields['quantity'].widget.attrs['class'] = 'span1'
    
def redeem(request,id):
	redeem = Redeem.objects.create(trade_id=id)
	return HttpResponseRedirect("/weekly")

def weekly(request):
	week = datetime.now().isocalendar()[1]
	users = User.objects.all()
	numusers = len(users)
	shoppers = [users[week%numusers],users[(week%numusers+1)%numusers]]
	totalTrades = []
	for index, shopper in enumerate(shoppers):
		trades = Trade.objects.filter(date__range=(datetime.now()+timedelta(-7),datetime.now()),giver=shopper,redeem__isnull=True)
		totalTrades.extend(Trade.objects.filter(taker=shopper,redeem__isnull=True))
		if trades:
			shoppers[index]=trades[0].taker
		else:
			redeems = Redeem.objects.filter(date__range=(datetime.now()+timedelta(-7),datetime.now()),trade__taker=shopper)
			if redeems:
				shoppers[index] = redeems[0].trade.giver
	
	cleaners = [users[(week+numusers/2)%numusers],users[((week+numusers/2)%numusers+1)%numusers]]
	addGroup = GroupForm()
	addItem = ItemAdd()
	tradingForm = TradeForm()
	shoppersQS = User.objects.filter(Q(id=week%numusers+1)|Q(id=(week%numusers+1)%numusers+1))
	unshoppersQS = User.objects.exclude(Q(id=week%numusers+1)|Q(id=(week%numusers+1)%numusers+1))
	tradingForm.fields['giver'].queryset = shoppersQS
	tradingForm.fields['taker'].queryset = unshoppersQS
	if request.POST:
		if 'itemadd' in request.POST:
			form = ItemAdd(request.POST)
			if form.is_valid():
				item = form.save()
				addItem.initial = {"group":item.group}
			else:
				addItem = form
		if 'groupadd' in request.POST:
			form = GroupForm(request.POST)
			if form.is_valid():
				group = form.save()
				addItem.initial = {"group":group}
			else:
				addGroup = form
		if 'trade' in request.POST:
			form = TradeForm(request.POST)
			if form.is_valid():
				form.save()
			else:
				tradingForm = form
	items = Item.objects.all()
	itemFormSet = modelformset_factory(Item,exclude=('group','name'),formset=BaseItemFormSet,
				  	   extra=0)
	
	if request.POST:
		if 'groceries' in request.POST:
			itemForms = itemFormSet(request.POST)
			if itemForms.is_valid():
				itemForms.save()
		else:
			if 'clear' in request.POST:
				for item in items:
					item.need = False;
					item.save()
			itemForms = itemFormSet(queryset=items)
	else:
		itemForms = itemFormSet(queryset=items)
	return render_to_response('weekly.html',context_instance=RequestContext(request,
										{"shoppers":shoppers,
										 "shoppersQS":shoppersQS,
										 "cleaners":cleaners,
										 "addGroup":addGroup,
										 "addItem":addItem,
										 "items":itemForms,
										 "tradingForm":tradingForm,
										 "redeemables":totalTrades}))

def getMemos(request):
    if request.POST:
        id1 = request.POST.get('id1')
        id2 = request.POST.get('id2')
        debts = Debt.objects.filter(Q(payer_id=id1,payee_id=id2)|Q(payer_id=id2,payee_id=id1)).values()
        for debt in debts:
            debt["date"] = debt["date"].strftime("%A %B %d, %Y ")
            debt["payer"] = User.objects.get(id=debt["payer_id"]).username
            debt["payee"] = User.objects.get(id=debt["payee_id"]).username
        print debts
        return HttpResponse(simplejson.dumps(list(debts)))
    else:
        return HttpResponse("")

class NameForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','email')

class PhoneForm(ModelForm):
    class Meta:
        model = ContentTypePhoneNumber
        fields = ('carrier','phone_number','object_id','content_type')
        widgets = {
            'object_id':HiddenInput(),
            'content_type':HiddenInput(),

        }

def update(request):
    phoneinstance = ContentTypePhoneNumber.objects.filter(object_id=request.user.id)
    phoneinstance = len(phoneinstance) > 0 and phoneinstance.get() or None
    data = {'object_id':request.user.id,
            'content_type':ContentType.objects.get_for_model(User),
            }
    form_collection = (
        (NameForm, request.user, "nameform",None),
        (PhoneForm, phoneinstance, "phoneform",data),
    )

    forms = dict(
        ("%s_form" % name, form_class(
            request.POST or None, instance=instance, prefix=name,initial=initial
        ))
        for form_class, instance, name, initial in form_collection
    )

    if request.POST and all(form.is_valid() for form in forms.values()):
        saved_objects = [form.save() for form in forms.values()]
        return HttpResponseRedirect("/")
    return render_to_response('update.html',context_instance=RequestContext(request,{"forms":forms}))
