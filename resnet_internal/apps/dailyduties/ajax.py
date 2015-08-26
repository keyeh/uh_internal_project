"""
.. module:: resnet_internal.apps.dailyduties.ajax
   :synopsis: ResNet Internal Daily Duties AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from datetime import datetime

from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.core.cache import cache

from django_ajax.decorators import ajax

from .models import DailyDuties
from .utils import GetDutyData, VoicemailManager

logger = logging.getLogger(__name__)


@ajax
def refresh_duties(request):
    duty_data = cache.get('duty_data')

    if not duty_data:
        with GetDutyData() as duty_data_manager:
            duty_data = {
                'printer_requests': duty_data_manager.get_printer_requests(),
                'voicemail': duty_data_manager.get_messages(),
                'email': duty_data_manager.get_email(),
                'tickets': duty_data_manager.get_tickets(request.user),
            }
            cache.set('duty_data', duty_data, 120)

    def duty_dict_to_link_text(daily_duty_dict, name):
        return_string = name

        if daily_duty_dict['count'] > 10:
            return_string += ' <strong class="text-danger">(' + str(daily_duty_dict['count']) + ')</strong>'
        elif daily_duty_dict['count'] > 0:
            return_string += ' <strong>(' + str(daily_duty_dict['count']) + ')</strong>'

        return return_string

    def duty_dict_to_popover_html(daily_duty_dict):
        popover_html = """
            Last Checked:
            <font color='""" + daily_duty_dict["status_color"] + """'>""" + daily_duty_dict["last_checked"] + """</font>
            <br />
            (<span style='text-align: center;'>""" + daily_duty_dict["last_user"] + """</span>)
            """
        return popover_html

    data = {
        'inner-fragments': {
            '#printer_requests_text': duty_dict_to_link_text(duty_data['printer_requests'], 'Printer Requests'),
            '#voicemail_text': duty_dict_to_link_text(duty_data['voicemail'], 'Voicemail'),
            '#email_text': duty_dict_to_link_text(duty_data['email'], 'Email'),
            '#ticket_text': duty_dict_to_link_text(duty_data['tickets'], 'Ticket Manager'),
        },
        'printer_requests_content': duty_dict_to_popover_html(duty_data['printer_requests']),
        'voicemail_content': duty_dict_to_popover_html(duty_data['voicemail']),
        'email_content': duty_dict_to_popover_html(duty_data['email']),
        'tickets_content': duty_dict_to_popover_html(duty_data['tickets']),
    }

    return data


@ajax
@require_POST
def update_duty(request):
    """ Update a particular duty.

    :param duty: The duty to update.
    :type duty: str

    """

    # Pull post parameters
    duty = request.POST["duty"]

    data = DailyDuties.objects.get(name=duty)
    data.last_checked = datetime.now()
    data.last_user = get_user_model().objects.get(username=request.user.username)
    data.save()


@ajax
@require_POST
def remove_voicemail(request):
    """ Removes computers from the computer index if no pinhole/domain name records are associated with it.

    :param message_uuid: The voicemail's uuid.
    :type message_uuid: int

    """
    # Pull post parameters
    message_uuid = request.POST["message_uuid"]

    context = {}
    context["success"] = True
    context["error_message"] = None
    context["message_uuid"] = message_uuid

    with VoicemailManager() as voicemail_manager:
        voicemail_manager.delete_message(message_uuid)

    return context
