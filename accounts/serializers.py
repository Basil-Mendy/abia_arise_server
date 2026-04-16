from rest_framework import serializers
from .models import IndividualMember, ProGroup, GroupMember, MembershipUser, MembershipGroup, GroupMembership

class IndividualMemberSerializer(serializers.ModelSerializer):
    # Full name for convenience
    full_name = serializers.SerializerMethodField()
    # Get group ID if member is part of a group
    group_id = serializers.SerializerMethodField()
    # Date joined alias
    date_joined = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = IndividualMember
        fields = [
            'id', 'abia_arise_id', 'nin', 'voters_card_no', 'first_name', 'middle_name',
            'last_name', 'full_name', 'email', 'phone_number', 'age', 'gender', 'occupation',
            'state_of_origin', 'lga_of_origin', 'country_of_origin',
            'lga_of_residence', 'state_of_residence', 'country_of_residence',
            'electoral_ward', 'polling_unit', 'membership_purpose', 'profile_picture',
            'bank_account_number', 'bank_name', 'bvn', 'pin',
            'is_individual', 'is_group_member', 'account_status',
            'created_at', 'date_joined', 'group_id'
        ]
        read_only_fields = ['id', 'abia_arise_id', 'created_at', 'date_joined', 'pin', 'account_status']

    def get_full_name(self, obj):
        """Get full name combining first, middle, and last names"""
        names = [obj.first_name, obj.middle_name, obj.last_name]
        return ' '.join([n for n in names if n]).strip()

    def get_group_id(self, obj):
        """Get the first group ID if member is part of a group"""
        group_member = obj.pro_groups.first()
        return group_member.group_id if group_member else None

class ProGroupSerializer(serializers.ModelSerializer):
    # Nested members
    members = serializers.SerializerMethodField()
    reset_pin = serializers.CharField(max_length=6, min_length=6, write_only=False, required=False)

    class Meta:
        model = ProGroup
        fields = [
            'id', 'group_license_number', 'name', 'state', 'lga', 'country', 'logo', 'address', 'total_members',
            'chairman_name', 'chairman_phone', 'chairman_email', 'chairman_residential_address',
            'chairman_passport',
            'secretary_name', 'secretary_phone', 'secretary_email', 'secretary_residential_address',
            'secretary_passport',
            'reset_pin', 'created_at', 'members'
        ]
        read_only_fields = ['id', 'group_license_number', 'created_at', 'members']

    def get_members(self, obj):
        """Get members in this group"""
        group_members = obj.members.all()
        return GroupMemberDetailSerializer(group_members, many=True).data

class GroupMemberDetailSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.get_full_name', read_only=True)

    class Meta:
        model = GroupMember
        fields = ['id', 'member', 'member_name', 'role', 'is_group_member', 'created_at']
        read_only_fields = ['id', 'created_at']

class GroupMemberSerializer(serializers.ModelSerializer):
    member_details = IndividualMemberSerializer(source='member', read_only=True)
    member_name = serializers.CharField(source='member.get_full_name', read_only=True)
    
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'member', 'member_details', 'member_name', 'role', 'is_group_member', 'created_at']
        read_only_fields = ['id', 'created_at']


class MemberActivationSerializer(serializers.Serializer):
    """
    Serializer for member activation
    """
    nin = serializers.CharField(max_length=11)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True)
    membership_purpose = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)


class ExcelMemberImportSerializer(serializers.Serializer):
    """
    Serializer for Excel member import
    """
    group_id = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=255)  # Last 4 digits of phone for verification
    excel_file = serializers.FileField()


class GenerateResetPinSerializer(serializers.Serializer):
    """
    Serializer for generating reset PIN
    """
    group_id = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=255)  # Chairman or secretary password
    desired_pin = serializers.CharField(max_length=6, min_length=6)  # 6 digit PIN


class VerifyResetPinOtpSerializer(serializers.Serializer):
    """
    Serializer for verifying OTP during reset PIN generation
    """
    group_id = serializers.CharField(max_length=30)
    otp = serializers.CharField(max_length=6, min_length=6)


class VerifyResetPinSerializer(serializers.Serializer):
    """
    Serializer for verifying reset PIN (activating reset mode)
    """
    group_id = serializers.CharField(max_length=30)
    reset_pin = serializers.CharField(max_length=6, min_length=6)


# ==========================================
# INDIVIDUAL MEMBER PIN RESET SERIALIZERS
# ==========================================

class GenerateIndividualResetPinSerializer(serializers.Serializer):
    """
    Serializer for generating reset PIN for individual member
    """
    member_id = serializers.CharField(max_length=30)  # abia_arise_id
    password = serializers.CharField(max_length=255)  # Last 4 digits of phone for verification
    desired_pin = serializers.CharField(max_length=6, min_length=6)  # 6 digit PIN


class VerifyIndividualResetPinOtpSerializer(serializers.Serializer):
    """
    Serializer for verifying OTP during reset PIN generation for individual member
    """
    member_id = serializers.CharField(max_length=30)  # abia_arise_id
    otp = serializers.CharField(max_length=6, min_length=6)


class VerifyIndividualResetPinSerializer(serializers.Serializer):
    """
    Serializer for verifying reset PIN (activating reset mode) for individual member
    """
    member_id = serializers.CharField(max_length=30)  # abia_arise_id
    reset_pin = serializers.CharField(max_length=6, min_length=6)


class AddMemberToGroupSerializer(serializers.Serializer):
    """
    Serializer for adding a new member to group (manual add)
    """
    group_id = serializers.CharField(max_length=30)
    reset_pin = serializers.CharField(max_length=6, min_length=6)  # Must be in reset mode
    full_name = serializers.CharField(max_length=200)
    nin = serializers.CharField(max_length=11)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True)
    voters_card_no = serializers.CharField(max_length=50, required=False, allow_blank=True)
    occupation = serializers.CharField(max_length=100, required=False, allow_blank=True)


# ==========================================
# MEMBERSHIP SYSTEM SERIALIZERS
# For flexible user-group membership management
# ==========================================

class MembershipUserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users with minimal info"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MembershipUser
        fields = ['id', 'nin', 'first_name', 'last_name', 'full_name', 'phone', 'email', 'registration_status', 'source', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class MembershipUserDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed user info with group memberships"""
    full_name = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    
    class Meta:
        model = MembershipUser
        fields = ['id', 'nin', 'first_name', 'last_name', 'full_name', 'phone', 'email', 'registration_status', 'source', 'groups', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_groups(self, obj):
        """Get all groups this user belongs to"""
        memberships = obj.group_memberships.all()
        return GroupMembershipDetailSerializer(memberships, many=True).data


class MembershipUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user"""
    
    class Meta:
        model = MembershipUser
        fields = ['nin', 'first_name', 'last_name', 'phone', 'email', 'registration_status', 'source']
    
    def validate_nin(self, value):
        """Ensure NIN is unique and properly formatted"""
        if MembershipUser.objects.filter(nin=value).exists():
            raise serializers.ValidationError("User with this NIN already exists.")
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("NIN must be 11 digits.")
        return value


class MembershipGroupSerializer(serializers.ModelSerializer):
    """Serializer for group info and stats"""
    total_members = serializers.SerializerMethodField()
    complete_count = serializers.SerializerMethodField()
    partial_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MembershipGroup
        fields = ['id', 'name', 'description', 'created_by', 'total_members', 'complete_count', 'partial_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_members(self, obj):
        return obj.total_members
    
    def get_complete_count(self, obj):
        return obj.complete_count
    
    def get_partial_count(self, obj):
        return obj.partial_count


class GroupMembershipDetailSerializer(serializers.ModelSerializer):
    """Serializer for membership details"""
    user_details = MembershipUserListSerializer(source='user', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'user_details', 'group', 'group_name', 'role', 'added_at']
        read_only_fields = ['id', 'added_at']


class GroupMembersListSerializer(serializers.ModelSerializer):
    """Serializer for listing group members with user details"""
    user_details = MembershipUserListSerializer(source='user', read_only=True)
    
    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'user_details', 'role', 'added_at']
        read_only_fields = ['id', 'added_at']


class ExcelUploadSerializer(serializers.Serializer):
    """Serializer for Excel file upload"""
    group_id = serializers.IntegerField()
    excel_file = serializers.FileField()
    
    def validate_excel_file(self, value):
        """Validate that the file is an Excel file"""
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError("Please upload a valid Excel file (.xlsx or .xls)")
        return value


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user self-registration"""
    nin = serializers.CharField(max_length=11)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=False)
    
    def validate_nin(self, value):
        """Validate NIN format"""
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("NIN must be 11 digits.")
        return value


class AddMemberToGroupSerializer(serializers.Serializer):
    """Serializer for manually adding a member to a group"""
    user_nin = serializers.CharField(max_length=11)
    
    def validate_user_nin(self, value):
        """Validate NIN format"""
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("NIN must be 11 digits.")
        return value


class RemoveMemberFromGroupSerializer(serializers.Serializer):
    """Serializer for removing a member from a group"""
    membership_id = serializers.IntegerField()


