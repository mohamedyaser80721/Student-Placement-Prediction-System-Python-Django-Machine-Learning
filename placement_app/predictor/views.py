from django.shortcuts import render, redirect
import joblib
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Load the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'placement_model.pkl')
model = joblib.load(model_path)

# Home page view
def home(request):
    return render(request, 'home.html')

# Result page view
def result(request):
    if request.method == 'POST':
        IQ = float(request.POST['IQ'])
        Prev_Sem_Result = float(request.POST['Prev_Sem_Result'])
        CGPA = float(request.POST['CGPA'])
        Academic_Performance = float(request.POST['Academic_Performance'])
        Internship_Experience = int(request.POST['Internship_Experience'])
        Extra_Curricular_Score = float(request.POST['Extra_Curricular_Score'])
        Communication_Skills = float(request.POST['Communication_Skills'])
        Projects_Completed = int(request.POST['Projects_Completed'])

        prediction = model.predict([[IQ, Prev_Sem_Result, CGPA, Academic_Performance,
                                     Internship_Experience, Extra_Curricular_Score,
                                     Communication_Skills, Projects_Completed]])

        result_text = "Student got Placement" if prediction[0] == 1 else "Student did not get Placement"

        context = {
            'result': result_text,
            'IQ': IQ,
            'Prev_Sem_Result': Prev_Sem_Result,
            'CGPA': CGPA,
            'Academic_Performance': Academic_Performance,
            'Internship_Experience': Internship_Experience,
            'Extra_Curricular_Score': Extra_Curricular_Score,
            'Communication_Skills': Communication_Skills,
            'Projects_Completed': Projects_Completed,
        }

        return render(request, 'result.html', context)
    else:
        return redirect('home')

# PDF download view
def download_pdf(request):
    if request.method == 'POST':
        context = {
            'result': request.POST.get('result'),
            'IQ': request.POST.get('IQ'),
            'Prev_Sem_Result': request.POST.get('Prev_Sem_Result'),
            'CGPA': request.POST.get('CGPA'),
            'Academic_Performance': request.POST.get('Academic_Performance'),
            'Internship_Experience': request.POST.get('Internship_Experience'),
            'Extra_Curricular_Score': request.POST.get('Extra_Curricular_Score'),
            'Communication_Skills': request.POST.get('Communication_Skills'),
            'Projects_Completed': request.POST.get('Projects_Completed'),
        }

        template_path = 'pdf_template.html'  # Make sure this exists in templates folder
        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF <pre>' + html + '</pre>')
        return response
    return redirect('home')
