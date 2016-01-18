from models import UserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self):
        data = self.clean()
        new_user = User.objects.create_user(username=data['username'],
                                            password=data['password'])
        return new_user


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
