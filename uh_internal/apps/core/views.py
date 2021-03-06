"""
.. module:: resnet_internal.apps.core.views
   :synopsis: University Housing Internal Core Views.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from datetime import datetime

from clever_selects.views import ChainedSelectFormViewMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic.base import TemplateView
from ldap_groups import ADGroup as LDAPADGroup
from srsconnector.models import ServiceRequest

from ..datatables.views import DatatablesView
from .ajax import PopulateRooms
from .forms import RoomCreateForm
from .models import SiteAnnouncements, Room, CSDMapping, ADGroup


class IndexView(TemplateView):
    template_name = "core/index.djhtml"

    def get_context_data(self, **kwargs):

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['announcements'] = SiteAnnouncements.objects.filter(Q(permission_classes__groups__users__id=self.request.user.id) | Q(permission_classes=None)).order_by('-created').distinct()[:3]
        return context


class TicketSummaryView(TemplateView):
    template_name = 'core/ticket_summary.djhtml'

    def get_context_data(self, **kwargs):
        context = super(TicketSummaryView, self).get_context_data(**kwargs)
        ticket_id = kwargs['ticket_id']
        context['ticket'] = ServiceRequest.objects.get(ticket_id=ticket_id)

        time_difference = (datetime.today() - context['ticket'].date_updated).total_seconds() / 86400

        if time_difference < 3:
            context['date_display_class'] = 'text-success'
        elif time_difference < 7:
            context['date_display_class'] = 'text-info'
        elif time_difference < 14:
            context['date_display_class'] = 'text-warning'
        else:
            context['date_display_class'] = 'text-danger'

        return context


class CSDDomainAssignmentEditView(TemplateView):
    template_name = "core/csd_assign_domain.djhtml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mapping_query = CSDMapping.objects.all()

        try:
            ldap_ad_group = LDAPADGroup(ADGroup.objects.get(display_name="CSD").distinguished_name)
            raw_member_data = ldap_ad_group.get_member_info()
        except (ADGroup.DoesNotExist, AttributeError):
            csd_choices = None
        else:
            csd_choices = [(member['userPrincipalName'], member['displayName']) for member in raw_member_data]

        context['csd_mappings'] = mapping_query
        context['csd_choices'] = csd_choices
        context['current_csds'] = [csd_choice[0] for csd_choice in csd_choices]

        return context


class RoomsView(ChainedSelectFormViewMixin, DatatablesView):
    template_name = "datatables/datatables_base.djhtml"
    form_class = RoomCreateForm
    populate_class = PopulateRooms
    model = Room
    success_url = reverse_lazy('core:rooms')


def handler500(request):
    """500 error handler which includes ``request`` in the context."""

    from django.template import loader
    from django.http import HttpResponseServerError

    template = loader.get_template('500.djhtml')

    return HttpResponseServerError(template.render(request=request))
