"""
.. module:: resnet_internal.technicians.ajax
   :synopsis: University Housing Internal Technicians AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax
from ldap_groups import ADGroup
from srsconnector.models import AccountRequest


@ajax
@require_POST
def remove_resnet_tech(request):
    """ Removes members from both the resnet tech groups.

    :param account_name: The member's account name.
    :type account_name: str
    :param group_dn: The distinguished name of the active directory group to be modified.
    :type group_dn: str

    """

    # Pull post parameters
    account_name = request.POST["account_name"]
    group_dn = request.POST["group_dn"]

    context = {}
    context["success"] = True
    context["error_message"] = None

    # Prevent a user from removing himself/herself from the group
    if account_name == request.user.username:
        context["success"] = False
        context["error_message"] = "For security reasons, one cannot delete oneself from a group."
        return context

    ad_group_instance = ADGroup(group_dn)

    # Remove from SRS
    ticket = AccountRequest(subject_username=account_name)
    ticket.request_type = 'Account Modification'
    ticket.action = 'Please remove from ResNet team.'
    ticket.save()

    sr_number = ticket.ticket_id
    context["sr_number"] = sr_number

    # Remove from AD
    ad_group_instance.remove_member(account_name)

    return context
