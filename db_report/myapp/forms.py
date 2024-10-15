from django import forms

class ReportForm(forms.Form):
    fields = forms.MultipleChoiceField(
        choices=[
            ('NAME', 'Name'),
            ('BRANCH_CODE', 'Branch Code'),
            ('SCHOOL', 'School'),
            ('PROGRAMME', 'Programme'),
            ('YOS', 'Year of Study'),
            ('MALE_COUNT', 'Male Count'),
            ('FEMALE_COUNT', 'Female Count'),
            ('AVERAGE_PERCENT', 'Average Percent')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Data Fields"
    )
    start_date = forms.DateField(required=True, widget=forms.SelectDateWidget)
    end_date = forms.DateField(required=True, widget=forms.SelectDateWidget)
