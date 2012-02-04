from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from debt.forms import DebtForm, DebtMulti
from debt.models import *
from django.contrib.auth.models import User

def index(request):
    users = User.objects.all()
    numUsers = users.count()
    matrix = [[{"amount":0,"payee":i.first_name,"payer":j.first_name} for i in users] for j in users]
    debtForm = DebtForm(initial={"payee":request.user})
    debtMulti = DebtMulti(initial={"payee":request.user,"payers":[request.user.id]})
    if request.POST:
        if 'multi' in request.POST:
            debtMulti = DebtMulti(request.POST)
            if debtMulti.is_valid():
                amount = debtMulti.cleaned_data['amount']
                users = debtMulti.cleaned_data['payers']
                amountEach = float(amount)/users.count()
                for user in users:
                    debt = Debt.objects.create(payee=debtMulti.cleaned_data['payee'],
                                               payer=user,
                                               amount=amountEach,
                                               memo=debtMulti.cleaned_data['memo'])
                debtMulti = DebtMulti(initial={"payee":request.user,"payers":[request.user.id]})
        else:
            debtForm = DebtForm(request.POST)
            if debtForm.is_valid():
                debtForm.save()
                debtForm = DebtForm(initial={"payee":request.user})
    debts = Debt.objects.all()
    for debt in debts:
        forward = matrix[debt.payer.id-1][debt.payee.id-1]
        backward = matrix[debt.payee.id-1][debt.payer.id-1]
        if backward["amount"] > 0:
            backward["amount"] -= debt.amount
            if backward["amount"] < 0:
                forward["amount"] -= backward["amount"]
                backward["amount"] = 0
        else:
            forward["amount"] += debt.amount
    return render_to_response('debt/index.html',context_instance=RequestContext(request,{'matrix':matrix,
                                                                                         'users':users,
                                                                                         'form':debtForm,
                                                                                         'multiform':debtMulti}))

def removeDebt(request,id):
    try:
        Debt.objects.get(id=id).delete()
    except:
        pass
    return HttpResponseRedirect("/debts/")

def settleDebt(request,id1,id2):
    try:
        Debt.objects.filter(Q(payer_id=id1,payee_id=id2)|Q(payer_id=id2,payee_id=id1)).delete()
    except:
        pass
    return HttpResponseRedirect("/debts/")
