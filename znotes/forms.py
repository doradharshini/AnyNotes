from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Email"
    }))
    first_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"First Name"
    }))
    last_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Last Name",
        "style":"'width:100%'",
    }))

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control p-2'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer.</small></span>'

       
        self.fields['password1'].widget.attrs['class'] = 'form-control p-2'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control p-2'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


choice_list=[]
# Comment these below 3 lines when you migrate and makemigrations for first time
choices = models.Department.objects.all().values_list('name','name')
for i in choices:
    choice_list.append(i)

class UploadNotesForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['title','body','department']

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':' form-control','style':"resize: none;","maxlength":"1000"}),
            'department' : forms.Select(attrs={'class':'form-control'},choices=choice_list ),
        }


class UpdateUserForm(forms.ModelForm):
    # username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Email Address"}))
    first_name = forms.CharField(max_length=100, label="First Name",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"First Name"}))
    last_name = forms.CharField(max_length=100, label="Last Name",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name"}))
    

    class Meta:
        model = User
        # fields=('username','first_name','last_name','email')
        fields=('first_name','last_name','email')

class ProfileImageForm(forms.ModelForm):
    profile_pic =  forms.ImageField(label="",required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control','id': 'profile-image-input'}))
    
    class Meta:
        model = models.Profile
        fields = ('profile_pic', )

class ProfileLinkForm(forms.ModelForm):
    bio = forms.CharField(required=False,max_length=500, label="Add Bio",widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Bio"}))
    website_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Website Link"}))
    facebook_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Facebook Link"}))
    instagram_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Instagram Link"}))
    linkedin_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Linkedin Link"}))

    class Meta:
        model = models.Profile
        fields = ('bio','website_link','facebook_link','instagram_link','linkedin_link', )
