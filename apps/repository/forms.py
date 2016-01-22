from models import Repository, Branch
from django.contrib.auth.models import User
from django.forms import ModelForm



class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        exclude = ['userprofile']


    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super(RepositoryForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.userprofile = self.userprofile
        super(RepositoryForm, self).save(*args, **kwargs)
        master_branch = Branch()
        master_branch.name = 'master'
        master_branch.repository = self.instance
        master_branch.save()
        return self.instance

    def clean(self):
        cleaned_data = super(RepositoryForm, self).clean()
        if 'name' in cleaned_data:
            name = cleaned_data['name']
            if Repository.objects.filter(userprofile=self.userprofile, name=name).exists():
                self.add_error('name', 'already exist')
        return cleaned_data
