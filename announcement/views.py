# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from announcement.models import Announcement, AnnouncementForm, SendForm
from sms.models import Carrier, ContentTypePhoneNumber, OutboundMessage
from sms.util import send_sms
from django.core.mail import send_mail


def index(request):
    a = Announcement.objects.all()
    form = AnnouncementForm(request.POST or None, initial={"poster":request.user})
    if request.POST and form.is_valid():
        form.save()
    sendform = SendForm()
    return render_to_response('announcement/index.html',context_instance=RequestContext(request,{'announcements':a,
                                                                                      'form':form,
                                                                                      'sendform':sendform}))
    
def send(request,id):
    announcement = Announcement.objects.get(id=id)
    form = SendForm(request.POST or None)
    if form.is_valid():
        emails = map(lambda x:x.email,form.cleaned_data["recipients"])
        phones = map(lambda x:ContentTypePhoneNumber.objects.get(object_id=x.id),form.cleaned_data["recipients"])
        if "2" in form.cleaned_data["medium"]:#email
            send_mail("An announcement from Billy",
                      "Hello. "+announcement.poster.first_name+" has made an announcement:\n "+ announcement.text,
                      "billy@cream.ly",
                      emails)
        if "1" in form.cleaned_data["medium"]:#sms
            send_sms(
                msg = announcement.poster.first_name+" says: "+announcement.text,
                from_address="billy@cream.ly",
                recipient_list=phones,
                fail_silently=False
            )
            
        return HttpResponseRedirect("/announcements")
    else:
        return HttpResponse("")
