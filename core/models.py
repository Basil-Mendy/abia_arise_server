from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    """
    Model for government achievements
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class News(models.Model):
    """
    Model for news/updates
    """
    CATEGORY_CHOICES = [
        ('development', 'Development'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('economy', 'Economy'),
        ('governance', 'Governance'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='news/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.excerpt and self.content:
            self.excerpt = self.content[:500]
        super().save(*args, **kwargs)


class Message(models.Model):
    """
    Model for tracking sent emails/messages
    """
    RECIPIENT_TYPE_CHOICES = [
        ('all', 'All Members & Groups'),
        ('members', 'All Members'),
        ('groups', 'Specific Groups'),
        ('specific', 'Specific Members'),
    ]

    subject = models.CharField(max_length=200)
    message = models.TextField()
    recipients = models.JSONField(default=list)  # List of email addresses
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ])
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {len(self.recipients)} recipients"


class Leadership(models.Model):
    """
    Model for Abia ARISE leadership
    """
    LEADERSHIP_LEVEL_CHOICES = [
        ('state', 'State Level'),
        ('local_government', 'Local Government Level'),
        ('ward', 'Ward Level'),
    ]

    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    leadership_level = models.CharField(max_length=30, choices=LEADERSHIP_LEVEL_CHOICES)
    picture = models.ImageField(upload_to='leadership/')
    bio = models.TextField(blank=True)
    lga = models.CharField(max_length=200, blank=True)  # For LG/Ward level leaders
    ward = models.CharField(max_length=200, blank=True)  # For Ward level leaders
    order = models.PositiveIntegerField(default=0)  # For ordering leaders
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['leadership_level', 'order', '-created_at']
        verbose_name_plural = 'Leadership'

    def __str__(self):
        return f"{self.name} - {self.role}"
