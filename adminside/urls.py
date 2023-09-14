from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.routers import DefaultRouter



# router = DefaultRouter()
# router.register(r'schedules', ScheduleViewSet)



urlpatterns = [
    path('users/', CustomUserViewSet.as_view(), name='userlist'),
    path('add-user/', CreateCustomUserView.as_view(), name='add-user'),
    path('edit-user/<int:id>/', CustomUserDeatiledView.as_view(), name='edit-user'),
    path('courses/',CourseListView.as_view(), name='view_courses'),
    path('coursemanage/<int:id>/',CourseUpdateRetrieveDeleteView.as_view(),name='usermanage'),
    path('create-trainer/',TrainerCreateView.as_view(), name='create-trainer'),
    path('trainers/',TrainerListView.as_view(), name='trainers_list'),
    path('related-trainers/<int:id>/',CourseRelatedTrainersListView.as_view(), name='related_trainers_list'),
    path('create-checkout-session/<int:id>/', csrf_exempt(CreateCheckOutSession.as_view()), name='checkout_session'),
    path('webhook/',stripe_webhook_view, name='stripe_webhook'),
    path('payments/',PaymentListView.as_view(), name='all payments'),
    path('trainer-students/<int:id>/',TrainerStudentsListView.as_view(), name='trainer_related_students'),
    path('purchasedcourses/<int:id>/',UserPurchasedCoursesListView.as_view(), name='purchased-courses'),
    path('timechange/<int:id>/', TrainerAvailabilitiesView.as_view(), name='trainer-partial-update'),
    path('check-status/<int:id>/', CheckCoursePurchase.as_view(), name="check_course_status"),
    path('monthly-purchase/',MonthlyPaymentDataView.as_view(), name="Monthly_payment_data"),
    # path('', include(router.urls)),

]