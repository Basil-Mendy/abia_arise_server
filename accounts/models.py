from django.db import models
from django.contrib.auth.models import User
import uuid
import hashlib
from .id_number_generator import generate_individual_id, generate_group_license_number

class IndividualMember(models.Model):
    """
    Model for individual members of Abia Arise
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    # Identification
    abia_arise_id = models.CharField(max_length=20, unique=True, db_index=True)
    nin = models.CharField(max_length=11, unique=True, db_index=True)
    voters_card_no = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, db_index=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    occupation = models.CharField(max_length=100, blank=True)

    # Origin Details
    state_of_origin = models.CharField(max_length=100, blank=True)
    lga_of_origin = models.CharField(max_length=100, blank=True)
    country_of_origin = models.CharField(max_length=100, default='Nigeria', blank=True)

    # Location Details
    lga_of_residence = models.CharField(max_length=100, blank=True)
    state_of_residence = models.CharField(max_length=100, blank=True)
    country_of_residence = models.CharField(max_length=100, default='Nigeria', blank=True)
    electoral_ward = models.CharField(max_length=100, blank=True)
    polling_unit = models.CharField(max_length=100, blank=True)

    # Membership Status
    ACCOUNT_STATUS_CHOICES = [
        ('pending_activation', 'Pending Activation'),
        ('active', 'Active'),
    ]
    is_individual = models.BooleanField(default=True, help_text="True if self-registered as individual member")
    is_group_member = models.BooleanField(default=False, help_text="True if added via Pro-Group Excel upload")
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='pending_activation', help_text="PENDING_ACTIVATION if via Excel only, ACTIVE if individually registered")
    
    # Membership
    membership_purpose = models.TextField(blank=True, null=True, help_text="Purpose for joining")
    password_hash = models.CharField(max_length=255, blank=True)  # Last 4 digits of phone

    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Generated ID Card
    id_card_file = models.FileField(upload_to='generated/id_cards/', null=True, blank=True, help_text="Path to generated ID card")

    # Bank Information
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    bvn = models.CharField(max_length=11, blank=True, null=True)

    # Security PIN (default 0000)
    pin = models.CharField(max_length=256, default='0000')  # Will be hashed

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.abia_arise_id})"

    def get_full_name(self):
        """Get full name combining first, middle, and last names"""
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join([n for n in names if n]).strip()

    def save(self, *args, **kwargs):
        if not self.abia_arise_id:
            # Generate Abia Arise ID in format: AB/{LGA_ACRONYM}/{SERIAL_NUMBER}
            self.abia_arise_id = generate_individual_id(self.lga_of_origin)

        # Set password_hash if individual and not set
        if self.is_individual and not self.password_hash:
            # Store last 4 digits of phone as password
            self.password_hash = self.phone_number[-4:]
        
        # Set account_status based on membership type
        if self.is_individual and not self.is_group_member:
            self.account_status = 'active'
        elif self.is_group_member and not self.is_individual:
            self.account_status = 'pending_activation'

        super().save(*args, **kwargs)


class ProGroup(models.Model):
    """
    Model for pro-group registrations
    """
    # Group Information
    group_license_number = models.CharField(max_length=30, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, blank=True)
    lga = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria', blank=True)
    address = models.TextField()
    total_members = models.IntegerField()
    logo = models.ImageField(upload_to='group_logos/', null=True, blank=True)

    # Chairman Information
    chairman_name = models.CharField(max_length=200)
    chairman_phone = models.CharField(max_length=20, unique=True)
    chairman_email = models.EmailField()
    chairman_residential_address = models.TextField()
    chairman_passport = models.ImageField(upload_to='passports/chairman/')
    chairman_password_hash = models.CharField(max_length=255)  # Last 4 digits

    # Secretary Information
    secretary_name = models.CharField(max_length=200)
    secretary_phone = models.CharField(max_length=20, unique=True)
    secretary_email = models.EmailField()
    secretary_residential_address = models.TextField()
    secretary_passport = models.ImageField(upload_to='passports/secretary/')
    secretary_password_hash = models.CharField(max_length=255)  # Last 4 digits

    # Members Database
    members_database = models.FileField(upload_to='member_databases/', null=True, blank=True)
    
    # Excel File (current uploaded members file)
    excel_file = models.FileField(upload_to='group_excel_files/', null=True, blank=True)

    # Generated Certificate
    certificate_file = models.FileField(upload_to='generated/certificates/', null=True, blank=True, help_text="Path to generated certificate")

    # Reset PIN (for managing members - 6 digits)
    reset_pin = models.CharField(max_length=6, blank=True, null=True, help_text="PIN for reset/admin mode")
    pending_reset_pin = models.CharField(max_length=6, blank=True, null=True)  # Temp storage during OTP verification
    pending_reset_pin_otp = models.CharField(max_length=6, blank=True, null=True)  # OTP to verify
    pending_reset_pin_expiry = models.DateTimeField(blank=True, null=True)  # OTP expiry time

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.group_license_number})"

    def save(self, *args, **kwargs):
        if not self.group_license_number:
            # Generate Group License Number in format: AB/PRG/{LGA_ACRONYM}/{SERIAL_NUMBER}
            self.group_license_number = generate_group_license_number(self.lga)

        if not self.chairman_password_hash:
            self.chairman_password_hash = self.chairman_phone[-4:]

        if not self.secretary_password_hash:
            self.secretary_password_hash = self.secretary_phone[-4:]

        super().save(*args, **kwargs)


class GroupMember(models.Model):
    """
    Model to link individual members to pro-groups
    """
    ROLE_CHOICES = [
        ('chairman', 'Chairman'),
        ('secretary', 'Secretary'),
        ('member', 'Member'),
    ]

    group = models.ForeignKey(ProGroup, on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey(IndividualMember, on_delete=models.CASCADE, related_name='pro_groups')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    is_group_member = models.BooleanField(default=False)  # Star indicator

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group', 'member')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member.abia_arise_id} in {self.group.name} ({self.role})"


# ==========================================
# NEW MEMBERSHIP SYSTEM MODELS
# For flexible user-group membership management
# ==========================================

class MembershipUser(models.Model):
    """
    User model for flexible membership system.
    Users are uniquely identified by NIN and can belong to multiple groups.
    """
    REGISTRATION_STATUS_CHOICES = [
        ('partial', 'Partial - Imported from group'),
        ('complete', 'Complete - Fully registered'),
    ]
    
    SOURCE_CHOICES = [
        ('group_import', 'Group Excel Import'),
        ('self_signup', 'Self Sign-up'),
    ]
    
    # Core Identifiers
    nin = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        help_text="National Identification Number - must be unique"
    )
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(null=True, blank=True)
    
    # Registration Status
    registration_status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS_CHOICES,
        default='partial'
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='self_signup'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['nin']),
            models.Index(fields=['registration_status']),
            models.Index(fields=['source']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.nin})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class MembershipGroup(models.Model):
    """
    Group model for organizing users into multiple groups.
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    
    # Admin Information
    created_by = models.CharField(max_length=200)  # Admin username or email
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def total_members(self):
        """Get total number of members in this group"""
        return self.members.count()
    
    @property
    def complete_count(self):
        """Get count of users with complete registration"""
        return self.members.filter(
            user__registration_status='complete'
        ).count()
    
    @property
    def partial_count(self):
        """Get count of users with partial registration"""
        return self.members.filter(
            user__registration_status='partial'
        ).count()


class GroupMembership(models.Model):
    """
    Many-to-many relationship between users and groups.
    Handles linking users to groups with optional roles.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('moderator', 'Moderator'),
    ]
    
    # Foreign Keys
    user = models.ForeignKey(
        MembershipUser,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    group = models.ForeignKey(
        MembershipGroup,
        on_delete=models.CASCADE,
        related_name='members'
    )
    
    # Optional Role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
    
    # Timestamp
    added_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        unique_together = ('user', 'group')
        indexes = [
            models.Index(fields=['user', 'group']),
            models.Index(fields=['group', 'added_at']),
        ]
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} in {self.group.name} ({self.role})"
