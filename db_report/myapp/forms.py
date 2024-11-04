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
        widget=forms.CheckboxSelectMultiple
            (attrs={
            'class': 'horizontal-checkbox-container'  # Using a class for custom vertical styling
        }),
        required=True,
        label="Select Data Fields"
    )

    institution_code = forms.ChoiceField(
        choices=[
            ('0', 'UNZA'),
            ('1', 'CBU'),
            ('2', 'KMU'),
            ('3', 'MKU'),
            ('4', 'MUL'),
            ('5', 'CHAU'),
            ('6', 'KNU')
        ],
        required=True,
        label="Select Institution"
    )

    database_instance = forms.ChoiceField(
        choices=[('default', 'UNZA'), ('CBU', 'CBU'), ('KMU', 'KMU'), ('MKU', 'MKU'), ('MUL', 'MUL'), ('CHAU', 'CHAU'), ('KNU', 'KNU')],
        label="Select Database Instance"
    )

    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date"
    )
    
    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date"
    )

    YOS= forms.ChoiceField(
        choices=[
            ('', 'select yos'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        required=False,
        label='Year of Study'
    )

    nrc = forms.CharField(required=False, label="Search by NRC")
