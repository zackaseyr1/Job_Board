from django.shortcuts import render, get_object_or_404, redirect
from .models import JobApplication
from .forms import JobApplicationForm
import csv
from django.shortcuts import get_object_or_404, HttpResponse



def landing_page(request):
    return render(request, 'index.html')

def job_application_list(request):
    job_applications = JobApplication.objects.all()
    return render(request, 'job_application_list.html', {'job_applications': job_applications})

def job_application_detail(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'job_application_detail.html', {'job_application': job_application})

def job_application_create(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job_application = form.save()
            return redirect('thankyou')
    else:
        form = JobApplicationForm()
    return render(request, 'job_application_form.html', {'form': form})

def job_application_update(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job_application)
        if form.is_valid():
            job_application = form.save()
            return redirect('job_application_detail', pk=job_application.pk)
    else:
        form = JobApplicationForm(instance=job_application)
    return render(request, 'job_application_form.html', {'form': form})

def job_application_delete(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        job_application.delete()
        return redirect('job_application_list')
    return render(request, 'job_application_confirm_delete.html', {'job_application': job_application})


def download_email(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk)
    email_content = job_application.email

    # Generate a CSV response with the email content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="email.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email Content'])
    writer.writerow([email_content])

    return response


def thankyou(request):
    return render(request, 'thankyou.html')