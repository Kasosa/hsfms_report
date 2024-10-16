from django import forms

class ReportForm(forms.Form):
    # Choices for the fields to select in the report
    FIELD_CHOICES = [
        ('SID', 'Student Number (SID)'),
        ('LOAN NUMBER', 'Loan Number'),
        ('BRANCH CODE', 'Branch Code'),
        ('ACCOUNT NUMBER', 'Account Number'),
        ('NAME', 'Name'),
        ('NRC', 'NRC'),
        ('GENDER', 'Gender'),
        ('YOS', 'Year of Study (YOS)'),
        ('SCHOOL CODE', 'School Code'),
        ('SCHOOL NAME', 'School Name'),
        ('PROGRAMME', 'Programme'),
        ('REG DATE', 'Registration Date'),
        ('PERCENT', 'Sponsor Rate Percent'),
        ('CELL', 'Cell Number'),
        ('INSTITUTION NAME', 'Institution Name'),
    ]

    fields = forms.MultipleChoiceField(
        choices=FIELD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Data Fields"
    )
    
    start_date = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%d %H:%M:%S.%f'],
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS.sss'}),
        label="Start Date"
    )
    
    end_date = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%d %H:%M:%S.%f'],
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS.sss'}),
        label="End Date"
    )
