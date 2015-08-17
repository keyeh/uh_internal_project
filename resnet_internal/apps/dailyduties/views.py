"""
.. module:: resnet_internal.apps.dailyduties.views
   :synopsis: ResNet Internal DailyDuties Views.

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""
import regex

from resnet_internal.apps.dailyduties.utils import VoicemailManager

from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.core.cache import cache


class VoicemailListView(TemplateView):
    template_name = "dailyduties/voicemail_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(VoicemailListView, self).get_context_data(**kwargs)
        
        with VoicemailManager() as voicemail_manager:
            context["voicemails"] = voicemail_manager.get_all_voicemail()
        
        return context


class VoicemailAttachmentRequestView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        message_uuid = self.kwargs["message_uuid"]
        cached_filedata = cache.get('voicemail:' + message_uuid)
        response = HttpResponse()
        
        if (cached_filedata is None):
            with VoicemailManager() as voicemail_manager:
                    filedata = voicemail_manager.get_attachment_uuid(message_uuid)[1]
            cache.set('voicemail:' + message_uuid, filedata, 7200)
        else:
            filedata = cached_filedata
         
        # Safari Media Player does not like its range requests
        # ignored so handle this.
        if self.request.META['HTTP_RANGE']:
            http_range_regex = regex.compile('bytes=(\d*)-(\d*)$')
            regex_match = http_range_regex.match(self.request.META['HTTP_RANGE'])
            response_start = int(regex_match.groups()[0])
            response_end = int(regex_match.groups()[1] if len(regex_match.groups()[1]) > 0 else (len(filedata) - 1))
        else:
            response_start = 0
            response_end = len(filedata) - 1

        response.write(filedata[response_start:response_end + 1])
        response["Accept-Ranges"] = 'bytes'
        response["Content-Length"] = response_end - response_start + 1
        response["Content-Type"] = 'audio/wav'
        response["Content-Range"] = 'bytes ' + str(response_start) + '-' + str(response_end) + '/' + str(len(filedata))

        return response
