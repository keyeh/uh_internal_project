"""
.. module:: resnet_internal.printers.ajax
   :synopsis: ResNet Internal Printers AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from srsconnector.models import STATUS_CHOICES, PrinterRequest

from .models import Request, Toner, Part
from .utils import can_fulfill_request, send_replenishment_email, send_delivery_confirmation


@dajaxice_register
def change_request_status(request, request_id, current_status):
    """ Updates the status of a printer request based on a drop-down value.

    :param request_id: The id of the request to process.
    :type request_id: str
    :param status: The new status value.
    :type status: str

    """

    dajax = Dajax()

    send_replenishment_email()

    status = int(current_status) + 1

    STATUS_MAP = {
        Request.STATUSES.index('Acknowledged'): 'Work In Progress',
        Request.STATUSES.index('Delivered'): 'Closed',
    }

    request_instance = Request.objects.get(id=request_id)

    if status in STATUS_MAP:
        # Handle inventory decrementation for acknowledge requests
        if status == Request.STATUSES.index('Acknowledged'):
            if can_fulfill_request(request_id):
                # Decrement each cartridge quantity
                for cartridge in request_instance.toner.all():
                    cartridge.quantity = cartridge.quantity - 1
                    cartridge.save()

                # Decrement each part quantity
                for part in request_instance.parts.all():
                    part.quantity = part.quantity - 1
                    part.save()
            else:
                dajax.alert("Cannot acknowledge request: Insufficient Inventory.")
                return dajax.json()

        # Update the SRS ticket
        ticket = PrinterRequest.objects.get(ticket_id=request_instance.ticket_id)

        # Grab the correct value for the srs ticket status
        ticket_status = STATUS_MAP[status]
        for choice in STATUS_CHOICES:
            if ticket_status in choice:
                srs_status_value = choice[1]  # The status won't accept the int values

        ticket.status = srs_status_value

        if status == Request.STATUSES.index('Delivered'):
            ticket.solution = "Item delivered by %s." % request.user.get_full_name()
            send_delivery_confirmation(request_instance)

        if "TONER" in ticket.request_type:
            request_list = []
            for cartridge in request_instance.toner.all():
                request_list.append(cartridge)
        elif "PARTS" in ticket.request_type:
            request_list = []
            for part in request_instance.parts.all():
                request_list.append(part)

        ticket.request_list = request_list  # Must include in update; gets blanked otherwise
        ticket.work_log = "Updated ticket status."
        ticket.save()

    request_instance.status = status
    request_instance.save()

    dajax.redirect(reverse('printer_request_list'))

    return dajax.json()


@dajaxice_register
def update_toner_inventory(request, toner_id, quantity=None, ordered=None):
    """ Updates the inventory quantity of a toner cartridge.

    :param toner_id: The id of the toner cartridge to process.
    :type toner_id: str
    :param quantity: The updated quantity.
    :type quantity: str

    """

    dajax = Dajax()

    toner_instance = Toner.objects.get(id=toner_id)
    if quantity:
        toner_instance.quantity = int(quantity)
    if ordered:
        toner_instance.ordered = int(ordered)
    toner_instance.save()

    return dajax.json()


@dajaxice_register
def update_part_inventory(request, part_id, quantity=None, ordered=None):
    """ Updates the inventory quantity of a printer part.

    :param part_id: The id of the toner cartridge to process.
    :type part_id: str
    :param quantity: The updated quantity.
    :type quantity: str

    """

    dajax = Dajax()

    part_instance = Part.objects.get(id=part_id)
    if quantity:
        part_instance.quantity = int(quantity)
    if ordered:
        part_instance.ordered = int(ordered)
    part_instance.save()

    return dajax.json()