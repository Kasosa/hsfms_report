from django.shortcuts import render
from django.db import connection
from .forms import ReportForm

def report_view(request):
    form = ReportForm(request.POST or None)
    data = None
    column_headers = None  # To store column headers for table display

    # Dictionary to map form field choices to SQL expressions
    field_map = {
        'NAME': "UPPER(s.Last_name + ' ' + s.First_Name) AS \"NAME\"",
        'BRANCH CODE': "b.branch_code AS \"BRANCH CODE\"",
        'SCHOOL': "sc.School_name AS \"SCHOOL\"",
        'PROGRAMME': "p.Programme_name AS \"PROGRAMME\"",
        'YOS': "r.Year_of_programme AS \"YOS\"",
        'MALE COUNT': "SUM(CASE WHEN s.Sex = 'M' THEN 1 ELSE 0 END) AS \"MALE COUNT\"",
        'FEMALE COUNT': "SUM(CASE WHEN s.Sex = 'F' THEN 1 ELSE 0 END) AS \"FEMALE COUNT\"",
        'AVERAGE PERCENT': "AVG(r.sponsor_rate * 100) AS \"AVERAGE PERCENT\""
    }

    if form.is_valid():
        fields = form.cleaned_data['fields']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    
        # Map selected fields to their SQL expressions
        selected_fields = [field_map[field] for field in fields]
        sql_selected_fields = ", ".join(selected_fields)
    
       
        group_by_fields = [field for field in fields if field not in ('MALE COUNT', 'FEMALE COUNT', 'AVERAGE PERCENT')]
    
        
        if 'YOS' not in group_by_fields:
            group_by_fields.append('YOS')  

        sql_group_by_fields = ", ".join([field_map[field].split(" AS ")[0] for field in group_by_fields])

        query = f"""
        SELECT  
            {sql_selected_fields}
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
            r.Institution_code = 1
            AND r.Registration_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY 
            {sql_group_by_fields}
        ORDER BY 
            r.Year_of_programme;
        """



        # fetch data
        with connection.cursor() as cursor:
            cursor.execute(query)
            column_headers = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

    return render(request, 'report.html', {
        'form': form,
        'data': data,
        'column_headers': column_headers
    })