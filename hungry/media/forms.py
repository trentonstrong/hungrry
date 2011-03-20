"""
media.forms

Forms for handling media uploads
"""
from datetime import datetime, timedelta
import hashlib
import hmac
import json

from django import forms
from hungry import settings
from hungry.media.models import Media


def make_params(redirect_url=None, transloadit_template=None):
    """
    Function to create JSON params for Transloadit upload form
    """
    
    # Transloadit upload form information
    expires = datetime.utcnow()+ timedelta(minutes=10)
    expires = expires.strftime('%Y/%m/%d %H:%M:%S+00:00')

    if (redirect_url == None):
        redirect_url = reverse('media_upload')
        redirect_url = request.build_absolute_uri(redirect_url)

    template_name = transloadit_template or 'media_upload'

    transloadit_params = json.dumps({
        "auth": {
            "key": settings.TRANSLOADIT_KEY,
            "expires": expires
        },
        "template_id": settings.TRANSLOADIT_TEMPLATES[template_name],
        "redirect_url": redirect_url
    })

    return transloadit_params

def sign(params):
    """
    Transloadit signature algorithm: HMAC of auth dictionary JSON w/ secret as key using SHA1
    """
    return hmac.new(
        settings.TRANSLOADIT_SECRET,
        params,
        hashlib.sha1).hexdigest()


class TransloaditUploadForm(forms.Form):
    """
    Simple form to render a file uploader to the Transloadit service
    """
    
    def __init__(self, user, *args, **kwargs):
        """
        Overrides default form constructor to support additional arguments and
        dynamic fields
        """
        redirect_url = kwargs.pop('redirect_url', None)
        template = kwargs.pop('transloadit_template',  None)
        super(TransloaditUploadForm, self).__init__(*args, **kwargs)

        # Callback URL for Transloadit
        if (redirect_url == None):
            redirect_url = reverse('media_upload')
            redirect_url = request.build_absolute_uri(redirect_url)

        self.redirect_url = redirect_url

        params = make_params(redirect_url, template)

         # Transloadit signature algorithm: HMAC of auth dictionary JSON w/ secret as key using SHA1
        signature = hmac.new(
            settings.TRANSLOADIT_SECRET,
            params,
            hashlib.sha1).hexdigest()

        self.fields['user'] = forms.CharField(
            initial=user.username,
            widget=forms.HiddenInput()
        )

        self.fields['params'] = forms.CharField(
            initial=params,
            widget=forms.HiddenInput()
        )

        self.fields['signature'] = forms.CharField(
            initial=signature,
            widget=forms.HiddenInput()
        )

    my_file = forms.FileField()


class TransloaditResponseForm(forms.Form):
    """
    Encapsulates the Transloadit response JSON object and provides utilities for
    storing the media associated with it.
    """

    transloadit = forms.CharField()

    user = forms.CharField()

    params = forms.CharField()

    signature = forms.CharField()

    def clean(self):
        """ Check authentication signature on transloadit response """
        cleaned_data = self.cleaned_data
        signature = sign(cleaned_data.get('params'))
        if (signature != cleaned_data.get('signature')):
            raise forms.ValidationError('Could not validate signature in upload response!')
        return cleaned_data

    def get_media(self):
        """ Create a media object from the Transloadit response data """
        response = json.loads(self.cleaned_data.get('transloadit'))
        response_results = response['results']
        response_media, response_thumb = response_results['media'][0], response_results['thumb'][0]

        media = Media()
        media.name = response_media['name']
        media.url = response_media['url']
        media.thumbnail = response_thumb['url']
        media.mime_type = response_media['mime']
        media.metadata = json.dumps(response_media['meta'])

        return media

