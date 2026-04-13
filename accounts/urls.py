from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IndividualMemberViewSet, ProGroupViewSet, GroupMemberViewSet, AdminLoginView,
    MembershipUserViewSet, MembershipGroupViewSet, AdminDashboardViewSet
)

router = DefaultRouter()
# Existing routes
router.register(r'members', IndividualMemberViewSet, basename='member')
router.register(r'groups', ProGroupViewSet, basename='group')
router.register(r'group-members', GroupMemberViewSet, basename='group-member')

# Membership system routes
router.register(r'membership/users', MembershipUserViewSet, basename='membership-user')
router.register(r'membership/groups', MembershipGroupViewSet, basename='membership-group')
router.register(r'admin/dashboard', AdminDashboardViewSet, basename='admin-dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
]
