"""
Views for the account application
"""
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from hungry import settings
from hungry.media.models import Media
from hungry.media.forms import TransloaditUploadForm, TransloaditResponseForm

from hungry.accounts.models import UserProfile
from hungry.accounts.forms import ProfileForm, ProfilePhotoForm


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

    # Callback URL for Transloadit
    redirect_url = reverse('account_profile_photo', kwargs={ 'username': request.user.username })
    redirect_url = request.build_absolute_uri(redirect_url)
    transloadit_form = TransloaditUploadForm(
        user,
        redirect_url=redirect_url,
        transloadit_template='profile_photo'
    )

    return render_to_response('accounts/account_profile_update_form.html',
                                {'profile': profile,
                                'form': form,
                                'transloadit_form': transloadit_form,
                                'transloadit_url': settings.TRANSLOADIT_URL},
                                context_instance=RequestContext(request))


def profile_photo(request, username):
    profile = request.user.get_profile()

    if(request.method == 'POST'):
        response_form = TransloaditResponseForm(request.POST)
        if (not response_form.is_valid()):
            raise Http500
    
        try:
            avatar = response_form.get_media()
            avatar.save()
        except:
            raise

        try:
            profile.avatar = avatar
            profile.save()
        except:
            raise

        return redirect('hungry.accounts.views.profile')




				

