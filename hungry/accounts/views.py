# Account views
from datetime import datetime, timedelta
import hashlib
import hmac
import json

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from hungry import settings

from accounts.models import UserProfile
from accounts.forms import ProfileForm, ProfilePhotoForm

from media.models import Media

@login_required
def profile(request):
    profile = None
    try:
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile()
        profile.user = request.user
        profile.save()

    if profile == None:
        raise Http404

    return render_to_response('accounts/account_profile.html',
                                {'profile': profile},
                                context_instance=RequestContext(request))

@login_required
def profile_update(request):
    user = request.user
    profile = user.get_profile()

    if (request.method == 'POST'):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            profile.zip_code = form.cleaned_data['zip_code']
            user.email = form.cleaned_data['email']
            user.save()
            profile.save()
            return redirect('accounts.views.profile')
            
    else:
        form = ProfileForm()
        
        # Transloadit upload form information
        expires = datetime.utcnow()+ timedelta(minutes=10)
        expires = expires.strftime('%Y/%m/%d %H:%M:%S+00:00')
        
        # Callback URL for Transloadit
        redirect_url = reverse('account_profile_photo', kwargs={ 'username': request.user.username })
        redirect_url = request.build_absolute_uri(redirect_url)

        transloadit_params = json.dumps({
            "auth": { 
                "key": settings.TRANSLOADIT_KEY,
                "expires": expires
            },
            "template_id": settings.TRANSLOADIT_TEMPLATES['profile_photo'],
            "redirect_url": redirect_url
        })

        # Transloadit signature algorithm: HMAC of auth dictionary JSON w/ secret as key using SHA1
        transloadit_signature = hmac.new(
            settings.TRANSLOADIT_SECRET,
            transloadit_params,
            hashlib.sha1).hexdigest()

    return render_to_response('accounts/account_profile_update_form.html',
                                {'profile': profile,
                                'form': form,
                                'params': transloadit_params,
                                'signature': transloadit_signature },
                                context_instance=RequestContext(request))


def profile_photo(request, username):
    profile = request.user.get_profile()

    if(request.method == 'POST'):
        try:
            upload_info = json.loads(request.POST['transloadit'])
            upload_results = upload_info['results']
            upload_media, upload_thumb = upload_results['media'][0], upload_results['thumb'][0]

            avatar = Media()
            avatar.name = upload_media['name']
            avatar.url = upload_media['url']
            avatar.thumbnail = upload_thumb['url']
            avatar.mime_type = upload_media['mime']
            avatar.metadata = json.dumps(upload_media['meta'])
        except KeyError:
            pass

        try:
            avatar.save()
        except:
            pass

        try:
            profile.avatar = avatar
            profile.save()
        except:
            pass

        return redirect('accounts.views.profile')



				

