""" All forms for /stock app """

from django import forms

class CompanyDataUploadForm(forms.Form):
    class Meta:
        fields = ['has_header', 'file']
    has_header = forms.BooleanField(label='File includes header', required=False)
    file = forms.FileField(required=True, label='Company Data File')

    # add
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.name.endswith('.csv'):
            return file
        else:
            raise forms.ValidationError('File extension needs to end with .csv')