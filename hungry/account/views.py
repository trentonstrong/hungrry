# Account views
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from account.models import UserProfile
from account.forms import ProfileForm, ProfilePhotoForm

@login_required
def profile(request):
		profile = None
		try:
				profile = request.user.get_profile()
		except (UserProfile.DoesNotExist):
				profile = UserProfile()
				profile.user = request.user
				profile.save()

		if not profile:
				raise Http404

		return render_to_response('account/account_profile.html',
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
						return redirect('account.views.profile')
				
		else:
				form = ProfileForm()

		return render_to_response('account/account_profile_update_form.html',
								  {'profile': profile,
								   'form': form},
								  context_instance=RequestContext(request))

@login_required
def profile_upload_photo(request):
		profile = request.user.get_profile()

		if(request.method == 'POST'):
				form = ProfilePhotoForm(request.POST, request.FILES)
				if form.is_valid():
						profile.profile_image = request.FILES['profile_image']
						profile.save()
						return redirect('account.views.profile')
		else:
				form = ProfilePhotoForm()

		return render_to_response('account/account_profile_photo_form.html',
								  {'profile': profile,
							       'form': form},
								  context_instance=RequestContext(request))




				

