from django.db import models
from django.core.mail import send_mail

class JobApplication(models.Model):
    EDUCATION_CHOICES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('degree', 'Degree'),
        ('master', 'Master'),
        ('other', 'Other'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    AVAILABLE_TIME_CHOICES = (
        ('free', 'Free'),
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    )

    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    available_time = models.CharField(max_length=100, choices=AVAILABLE_TIME_CHOICES)
    education = models.CharField(max_length=100, choices=EDUCATION_CHOICES)
    skills = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']






class EmailCampaign(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    recipients = models.ManyToManyField('JobApplication')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_emails()
        
    def send_emails(self):
        recipient_emails = self.recipients.values_list('email', flat=True)
        send_mail(self.subject, self.message, 'zackaseyr@gmail.com', recipient_emails, fail_silently=False)



