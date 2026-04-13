from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Achievement, News, Message, Leadership
from .serializers import AchievementSerializer, NewsSerializer, MessageSerializer, LeadershipSerializer
import logging

logger = logging.getLogger(__name__)

class AchievementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing achievements
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Set the creator to the current admin user"""
        serializer.save(created_by=self.request.user)

class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing news
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter news by category if provided
        """
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def perform_create(self, serializer):
        """Set the creator to the current admin user"""
        serializer.save(created_by=self.request.user)


class SendEmailView(APIView):
    """
    API endpoint for sending emails to members and group leaders
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Send emails to specified recipients
        
        Expected data:
        {
            "subject": "Email subject",
            "message": "Email content",
            "recipients": ["email1@example.com", "email2@example.com"],
            "recipient_type": "specific|members|groups|all"
        }
        """
        try:
            subject = request.data.get('subject')
            message_content = request.data.get('message')
            recipients = request.data.get('recipients', [])
            recipient_type = request.data.get('recipient_type', 'specific')

            # Validation
            if not subject or not subject.strip():
                return Response({
                    'success': False,
                    'error': 'Subject is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not message_content or not message_content.strip():
                return Response({
                    'success': False,
                    'error': 'Message content is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not recipients or len(recipients) == 0:
                return Response({
                    'success': False,
                    'error': 'At least one recipient is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Remove duplicates and filter out invalid emails
            unique_recipients = list(set(recipients))
            unique_recipients = [email for email in unique_recipients if '@' in email]

            if len(unique_recipients) == 0:
                return Response({
                    'success': False,
                    'error': 'No valid email addresses provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Prepare email list
            email_messages = []
            for recipient in unique_recipients:
                email_messages.append((
                    subject,
                    message_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient]
                ))

            # Send emails
            try:
                send_mass_mail(tuple(email_messages), fail_silently=False)
                
                # Save message record
                message = Message.objects.create(
                    subject=subject,
                    message=message_content,
                    recipients=unique_recipients,
                    recipient_type=recipient_type,
                    status='sent',
                    sent_by=request.user
                )

                return Response({
                    'success': True,
                    'message': f'Email sent successfully to {len(unique_recipients)} recipient(s)',
                    'recipients_count': len(unique_recipients),
                    'message_id': message.id
                }, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f'Error sending emails: {str(e)}')
                # Save failed message record
                Message.objects.create(
                    subject=subject,
                    message=message_content,
                    recipients=unique_recipients,
                    recipient_type=recipient_type,
                    status='failed',
                    sent_by=request.user
                )

                return Response({
                    'success': False,
                    'error': 'Failed to send emails. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f'Unexpected error in send email: {str(e)}')
            return Response({
                'success': False,
                'error': f'An unexpected error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeadershipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Abia ARISE leadership
    """
    queryset = Leadership.objects.filter(is_active=True)
    serializer_class = LeadershipSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        """
        Allow unauthenticated access to list and retrieve leadership
        Only authenticated admins can create/update/delete
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Filter leadership by level or return all
        """
        queryset = super().get_queryset()
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(leadership_level=level)
        return queryset.order_by('leadership_level', 'order')
