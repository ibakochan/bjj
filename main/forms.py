from django import forms
from main.models import Lesson, ParticipationCount
from django.core.files.uploadedfile import InMemoryUploadedFile
from accounts.models import CustomUser
from main.humanize import naturalsize



class UserPreferencesForm(forms.ModelForm):
    # This form lets you upload a profile picture and select belt, stripes, member type, gym, for a member.
    # everything about uploading pictures I got from the dj4e tutorial.
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # for uploading a picture max 2mb large.
    profile_picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'profile_picture'


    # using widgets to get it looking a little bit nicer.
    class Meta:
        model = CustomUser
        fields = ['belt', 'stripes', 'member_type', 'gym_choice', 'profile_picture']
        widgets = {
            'belt': forms.Select(attrs={'class': 'form-control col-3'}),
            'stripes': forms.Select(attrs={'class': 'form-control col-3'}),
            'member_type': forms.Select(attrs={'class': 'form-control col-3'}),
            'gym_choice': forms.Select(attrs={'class': 'form-control col-3'}),
        }


    def clean(self):
        # Enforces the upload limit and gives an error text when the file is above the limit which is 2mb.
        cleaned_data = super().clean()
        user = cleaned_data.get('profile_picture')
        if user is None:
            return
        if len(user) > self.max_upload_limit:
            self.add_error('profile_picture', "File must be < "+self.max_upload_limit_text+" bytes")

    def save(self, commit=True):
        instance = super(UserPreferencesForm, self).save(commit=False)

        # Creating an instance from the form to save it in the model.
        f = instance.profile_picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.profile_picture = bytearr

        if commit:
            instance.save()

        return instance



class ParticipationCountForm(forms.ModelForm):
    # This form lets you update a member participation count manually
    # This is so that the owner of the gym can manually add previous participationcounts that were in paper form.
    class Meta:
        model = ParticipationCount
        fields = ['user', 'white_jiu_jitsu_count', 'blue_jiu_jitsu_count', 'purple_jiu_jitsu_count', 'brown_jiu_jitsu_count', 'black_jiu_jitsu_count']

        #Using widgets again for some style.
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'white_jiu_jitsu_count': forms.TextInput(attrs={'class': 'form-control col-2'}),
            'blue_jiu_jitsu_count': forms.TextInput(attrs={'class': 'form-control col-2'}),
            'purple_jiu_jitsu_count': forms.TextInput(attrs={'class': 'form-control col-2'}),
            'brown_jiu_jitsu_count': forms.TextInput(attrs={'class': 'form-control col-2'}),
            'black_jiu_jitsu_count': forms.TextInput(attrs={'class': 'form-control col-2'}),
        }




class CreateForm(forms.ModelForm):
    # This is a form for creating a lesson in the schedule.
    # It's using the same type of code as for the picture in the UserCreateForm.
    # You can write a title, text, time, upload a picture, choose day, spot in the schedule, category, color and school
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'



    class Meta:
        model = Lesson
        fields = ['title', 'text', 'day', 'spot', 'time', 'category', 'color', 'school', 'picture']

        #Using widgets again for some style.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'spot': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        lesson = cleaned_data.get('picture')
        if lesson is None:
            return
        if len(lesson) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    def clean_text(self):
       # This part is also from the django tutorial dj4e.
       # This makes the text into paragraphs.
       text = self.cleaned_data.get('text')
       paragraphs = ['<p>{}</p>'.format(line) for line in text.splitlines()]
       cleaned_text = ''.join(paragraphs)
       return cleaned_text


    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance
