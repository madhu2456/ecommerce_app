from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.conf import settings

from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from .utils import Mailchimp
from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', None)


# Create your views here.

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email'
    success_message = 'Your email preferences settings have been updated'

    # def dispatch(self, *args, **kwargs):
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         # return HttpResponse('Not Allowed', status=400)
    #         return redirect('/login/?next=/settings/email/')
    #     return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


# fired_at: 2018-04-30 13:02:09
# data[list_id]: 8eb179af30
# data[email]: madhu.kumar245@gmail.com
# data[merges][FNAME]:
# data[reason]: manual
# data[email_type]: html
# data[merges][BIRTHDAY]:
# data[id]: 189097b027
# data[web_id]: 4327407
# data[ip_opt]: 123.201.115.91
# data[merges][EMAIL]: madhu.kumar245@gmail.com
# data[merges][ADDRESS]:
# data[merges][PHONE]:
# type: # unsubscribe
# data[merges][LNAME]:

class MailchimpWebhookView(CsrfExemptMixin, View):  # HTTP GET def get()
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get('type')
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
                # qs = MarketingPreference.objects.filter(user__email__iexact=email)
                # if qs.exists():
                #     qs.update(subscribed=True, mailchimp_subscribed=True, mailchimp_msg=str(data))
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)
            # qs = MarketingPreference.objects.filter(user__email__iexact=email)
            # if qs.exists():
            #     qs.update(subscribed=False, mailchimp_subscribed=False, mailchimp_msg=str(data))
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                        subscribed=is_subbed,
                        mailchimp_subscribed=is_subbed,
                        mailchimp_msg=str(data)
                    )

        return HttpResponse('Thank You', status=200)

# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get('type')
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed':
#             is_subbed, mailchimp_subbed = (True, True)
#             # qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             # if qs.exists():
#             #     qs.update(subscribed=True, mailchimp_subscribed=True, mailchimp_msg=str(data))
#         elif sub_status == 'unsubscribed':
#             is_subbed, mailchimp_subbed = (False, False)
#         # qs = MarketingPreference.objects.filter(user__email__iexact=email)
#         # if qs.exists():
#         #     qs.update(subscribed=False, mailchimp_subscribed=False, mailchimp_msg=str(data))
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(
#                     subscribed=is_subbed,
#                     mailchimp_subscribed=is_subbed,
#                     mailchimp_msg=str(data)
#                 )
#
#     return HttpResponse('Thank You', status=200)
