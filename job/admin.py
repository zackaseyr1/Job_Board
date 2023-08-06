from django.contrib import admin
from .models import JobApplication, EmailCampaign
from django.http import HttpResponse
import csv
import smtplib

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'email', 'phone_number', 'date')
    list_filter = ('education', 'available_time', 'date')
    search_fields = ('name', 'location', 'email', 'phone_number')
    ordering = ('-date',)

    actions = ['download_emails', 'download_all_information']

    def download_emails(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="job_applications_emails.csv"'

        writer = csv.writer(response)
        writer.writerow(['Email'])

        for job_application in queryset:
            if job_application.email:
                writer.writerow([job_application.email])

        return response

    download_emails.short_description = "Download selected email addresses"


    def download_all_information(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Location', 'Email', 'Phone Number', 'Available Time', 'Education', 'Skills', 'Age', 'Gender', 'Date'])

        for job_application in queryset:
            writer.writerow([
                job_application.name,
                job_application.location,
                job_application.email,
                job_application.phone_number,
                job_application.available_time,
                job_application.education,
                job_application.skills,
                job_application.age,
                job_application.gender,
                job_application.date
            ])

        return response

    download_all_information.short_description = "Download all information"


admin.site.register(JobApplication, JobApplicationAdmin)








class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message')
    filter_horizontal = ('recipients',)



    def save_model(self, request, obj, form, change):
        # Test SMTP server connection
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        
        try:
            # Save the EmailCampaign model first
            super().save_model(request, obj, form, change)
            
            # Access the recipients field after saving the model
            recipient_emails = obj.recipients.values_list('email', flat=True)
            
            for recipient_email in recipient_emails:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.ehlo()
                    server.starttls()
                    server.login('zackaseyr@gmail.com', 'xljgqaxnfvsctety')
                    server.sendmail('zackaseyr@gmail.com', recipient_email, obj.message)
                
            self.message_user(request, 'Emails sent successfully')
        except Exception as e:
            self.message_user(request, f'Failed to send emails: {str(e)}')


            


admin.site.register(EmailCampaign, EmailCampaignAdmin)