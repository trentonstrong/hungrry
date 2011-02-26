from django import forms

	
class ProfileForm(forms.Form):
		first_name = forms.CharField(max_length = 50)
		last_name = forms.CharField(max_length = 50)
		zip_code = forms.CharField(max_length = 5)
		email = forms.EmailField()

		
class ProfilePhotoForm(forms.Form):
		profile_image = forms.ImageField(required=True)		
		
