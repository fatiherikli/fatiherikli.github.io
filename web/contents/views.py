from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from contents.forms import ContactForm

class ContactView(FormView):
    form_class = ContactForm

    def get_success_url(self):
        return reverse("contact_success")

    def form_valid(self, form):

        send_mail(
            subject=_("Contact Form"),
            message=form.cleaned_data["message"],
            from_email=form.cleaned_data["email"],
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=True
        )

        return super(ContactView, self).form_valid(form)