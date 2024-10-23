import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from .forms import ReportForm
import pytz

def report_view(request):
    form = ReportForm(request.POST or None)
    data = []
    column_headers = []  # Initialize as an empty list

    if form.is_valid():
        # Get cleaned data
        local_tz = pytz.timezone('Africa/Lusaka')
        start_date = form.cleaned_data['start_date'].strftime('%Y-%m-%d 00:00:00.000')  # Adjusting for the specified format
        end_date = form.cleaned_data['end_date'].strftime('%Y-%m-%d 23:59:59.999')    # Adjusting for the specified format
        institution_code = form.cleaned_data['institution_code']
        database = form.cleaned_data['database_instance']
        nrc = form.cleaned_data.get('nrc')

        # Fetch the fields selected in the form
        selected_fields = form.cleaned_data['fields']
        print(form.cleaned_data)
        # Build the SQL SELECT statement dynamically based on selected fields
        field_map = {
            'SID': "s.Student_number AS \"SID\"",
            'LOAN NUMBER': "s.Loan_number AS \"LOAN NUMBER\"",
            'BRANCH CODE': "b.branch_code AS \"BRANCH CODE\"",
            'ACCOUNT NUMBER': "s.Bank_account AS \"ACCOUNT NUMBER\"",
            'NAME': "UPPER(s.Last_name + ' ' + s.First_Name) AS \"NAME\"",
            'NRC': "s.NRC AS \"NRC\"",
            'GENDER': "s.Sex AS \"GENDER\"",
            'YOS': "r.Year_of_programme AS \"YOS\"",
            'SCHOOL CODE': "sc.School_code AS \"SCHOOL CODE\"",
            'SCHOOL NAME': "sc.School_name AS \"SCHOOL\"",
            'PROGRAMME': "p.Programme_name AS \"PROGRAMME\"",
            'REG DATE': "r.Registration_date AS \"REG DATE\"",
            'PERCENT': "r.sponsor_rate * 100 AS \"PERCENT\"",
            'CELL': "s.Cell AS \"CELL\"",
            'INSTITUTION NAME': "i.Institution_name AS \"INSTITUTION NAME\"",
        }
        
        # Map selected fields to their SQL expressions
        sql_selected_fields = [field_map[field] for field in selected_fields]
        # search = input()
        # or s.nrc = search
        # Construct the SQL query
        query = f"""
        SELECT 
            {', '.join(sql_selected_fields)}
        FROM 
            STUDENT s
        LEFT JOIN 
            Registration r ON r.Student_serial_no = s.Student_serial_no
        LEFT JOIN 
            Institution i ON i.Institution_code = r.Institution_code
        LEFT JOIN 
            School sc ON sc.School_code = r.School_code
        LEFT JOIN 
            Programme p ON p.Programme_code = r.Programme_code
        LEFT JOIN 
            bank_branch b ON b.branch_code = s.branch_code
        WHERE 
            r.Institution_code = {institution_code}
            AND r.Registration_date BETWEEN '{start_date}' AND '{end_date}'   
        """
        # Add NRC filter if provided
        if nrc:
            query += f" AND s.NRC = '{nrc}'"
        # Fetch data from the database
        with connection.cursor() as cursor:
            cursor.execute(query)
            column_headers = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
        
        # Check if download as CSV is requested
        if 'download_csv' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            writer = csv.writer(response)
            writer.writerow(column_headers)  # Write header row
            for row in data:
                writer.writerow(row)

            return response
        
        #print(data)  # This will show the fetched data in the console for debugging
        print(f"Fetched {len(data)} records.")
    return render(request, 'report.html', {
        'form': form,
        'data': data,
        'column_headers': column_headers
    })
