from rest_framework import serializers
from .models import Achievement, News, Message, Leadership

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'title', 'description', 'image', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

class NewsSerializer(serializers.ModelSerializer):
    # Map content_type from frontend to category field
    content_type = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'excerpt', 'image', 'category', 'content_type', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'excerpt', 'created_by']

    def create(self, validated_data):
        """Override create to handle content_type mapping"""
        # If content_type is provided, use it as category, otherwise default to 'other'
        content_type = validated_data.pop('content_type', 'other')
        if content_type:
            validated_data['category'] = content_type
        return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'subject', 'message', 'recipients', 'recipient_type', 'status', 'sent_by', 'created_at']
        read_only_fields = ['id', 'created_at', 'status', 'sent_by']


class LeadershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadership
        fields = ['id', 'name', 'role', 'leadership_level', 'picture', 'bio', 'lga', 'ward', 'order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

