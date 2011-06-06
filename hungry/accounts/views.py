"""
Views for the account application
"""
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from hungry import settings
from hungry.media.models import Media
from hungry.media.forms import TransloaditUploadForm, TransloaditResponseForm

from hungry.accounts.models import UserProfile
from hungry.accounts.forms import ProfileForm, ProfilePhotoForm


def profile(request, username):
    if username:
        user = User.objects.select_related().get(username=username)
        if user is None:
            raise Http404
        template = 'accounts/account_profile.html'
    else:
        if request.user.is_authenticated():
            user = request.user
        else:
            return redirect('auth_login')
        template = 'accounts/account_profile_update_form.html'

    profile = None
    try:
        profile = user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile()
        profile.user = user
        profile.save()

    if profile == None:
        raise Http404

    if (user == request.user):
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

    user_albums = user.useralbum_set.select_related()

    return render_to_response(template,
                                {'profile': profile,
                                 'form': form,
                                 'transloadit_form': transloadit_form,
                                 'transloadit_url': settings.TRANSLOADIT_URL,
                                 'user_albums': user_albums},
                                context_instance=RequestContext(request))

def profile_photo(request, username):
    """ Callback handler for Transloadit uploads """
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
            profile.profile_album.media.add(avatar)
        except:
            raise

        return redirect('hungry.accounts.views.profile')




				

