
from base.models import *
from .serializer import *
from .models import *
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from django.http import Http404, HttpResponse

from .serializer import CreateCustomUserSerializer

from rest_framework import status
from rest_framework.response import Response

import random
import string
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.parsers import MultiPartParser

import stripe
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from chat.models import *
# Create your views here.


class CustomUserViewSet(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)  # Use AllowAny permission class


class CreateCustomUserView(CreateAPIView):
    serializer_class = CreateCustomUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            print(serializer,'-------serializer admin adding user')
            if serializer.is_valid():
                print('-----starting processs')
                subject = 'Welcome to FitZone!'
                username=serializer.validated_data['username']
                email=serializer.validated_data['email']
                # Generate a random password with 8 characters (can be adjusted as needed)
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                message = f"Your password is {password}"

                email_from = settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, [email])
            
                # Create the user object with the provided username and email
                user = CustomUser.objects.create(
                    username=username,
                    email=email,
                )
                print(user,'--------user is here')
                user.set_password(password)  # Set the password
                user.is_verified = True
                user.save()

                UserProfile.objects.create(user=user)

                # serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomUserDeatiledView(APIView):
    def get_user(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            raise Http404
        

    def get(self, request, id, format=None):
        user = self.get_user(id)
        print(user,'----usergot')
        serializer = CreateCustomUserSerializer(user)
        print(serializer.data,'-------datas fetching')
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
 
        user = self.get_user(id)
        if user.is_blocked == True:
            user.is_blocked = False
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response ('User Unblocked',status=status.HTTP_200_OK)
        else:
            user.is_blocked = True
            user.is_active = False
            user.is_verified = False
            user.save()
            return Response ('User blocked',status=status.HTTP_200_OK)
    


class CourseListView(APIView):

    parser_classes = [MultiPartParser]

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseViewSerializer(courses, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):

        courseName = request.data.get('course_name')
        if Course.objects.filter(course_name__iexact=courseName.lower().replace(' ', '')).exists():
            return Response(data= 'This course already exists.', status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CourseViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CourseUpdateRetrieveDeleteView(APIView):
    def get_course(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404
        
    def get(self, request, id, format=None):
        course = self.get_course(id)
        serializer = CourseViewSerializer(course)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):

        courseName = request.data.get('course_name')
        if Course.objects.exclude(pk=id).filter(course_name__iexact=courseName.lower().replace(' ', '')).exists():
            return Response(data= 'This course already exists.Please Use Another name', status=status.HTTP_400_BAD_REQUEST)

        course = self.get_course(id)
        serializer = CourseViewSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        course = self.get_course(id)
        course.is_deleted = True
        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)




class TrainerCreateView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = VerifyTrainerFieldSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            image = serializer.validated_data['image']
            course_id = serializer.validated_data['course_id']
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Create the CustomUser object (trainer) and set the password
            user = CustomUser.objects.create_trainer(username=username, email=email, password=password)
            print(user,'----user got')
            if user:
                message = f"Your password is {password}"
                subject = 'Welcome to FitZone!'
                email_from = settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, [email])

                # Get the Course object based on the course name
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    return Response({"error": "Invalid course name."}, status=400)

                # Create the Trainer object
                Trainer.objects.create(user=user, course=course, trainer_photo=image)
                Room.objects.create(name=user.username, image=image)
                UserProfile.objects.create(user=user)
                return Response(serializer.data)

        return Response(serializer.errors, status=400)




class TrainerListView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, format=None):
        trainers = Trainer.objects.all()
        serializer = TrainerViewSerializer(trainers, many=True)
        return Response(serializer.data)
    



class TrainerAvailabilitiesView(APIView):
    def get_trainer(self, id):
        try:
            user = CustomUser.objects.get(id=id)
            return Trainer.objects.get(user=user)
        except Trainer.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        trainer = self.get_trainer(id)
        if trainer:
            serializer = TrainerTimeViewSerializer(trainer)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, id, format=None):
        trainer = self.get_trainer(id)
        if trainer:
            serializer = TrainerTimeViewSerializer(trainer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


    


class CourseRelatedTrainersListView(APIView):
    
    def get(self, request, id):
        course = Course.objects.get(id=id)
        trainers = Trainer.objects.filter(course=course)
        serializer = TrainerViewSerializer(trainers, many=True)
        return Response(serializer.data)
    



stripe.api_key=settings.STRIPE_SECRET_KEY

API_URL=settings.DJANGO_SERVER


class CreateCheckOutSession(APIView):

    def post(self, request, id, *args, **kwargs):
        course_id=id
        selected_trainer_id = request.data.get('selectedTrainerId')
        current_user_id = request.data.get('currentUserId')
        selectedTime = request.data.get('selectedTime')
        print(selected_trainer_id,'---------trainer')
        print(current_user_id,'---------user')
        print(selectedTime,'---------time')
        print(course_id,'---------course')
        try:
            course=Course.objects.get(id=course_id)
            user = CustomUser.objects.get(id=current_user_id)
            if PurchasedOrder.objects.filter(selected_course=course, user=user).exists():
                purchased_order = PurchasedOrder.objects.get(selected_course=course, user=user)
                if purchased_order.valid_up_to and purchased_order.valid_up_to > timezone.now():
                    print("Already exists, but valid date is not over")
                    # Redirect to the cancel URL
                    return redirect(settings.SITE_URL + f'/classesdetails/{course_id}')
                
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'inr',
                             'unit_amount':int(course.course_fee) * 100,
                             'product_data':{
                                 'name':course.course_name,
                                 
                                 
                             }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "course_id":course.id,
                    "user_id": current_user_id,
                    "trainer_id" : selected_trainer_id,
                    "selectedTime" : selectedTime,
                },
                mode='payment',
                success_url=settings.SITE_URL + '/profile',
                cancel_url=settings.SITE_URL + f'/classesdetails/{course_id}',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'msg': 'something went wrong while creating stripe session', 'error': str(e)}, status=500)




@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None
    end_point = settings.STRIPE_SECRET_WEBHOOK

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, end_point
        )
    except ValueError as e:
        print('Invalid payload',e)
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Invalid signature',e)
        # Invalid signature
        return HttpResponse(status=400)
    
    if event["type"] == "checkout.session.completed":
        session = event['data']['object']

        customer_email = session['customer_details']['email']
        course_id = session['metadata']['course_id']
        user_id = session['metadata']['user_id']
        trainer_id = session['metadata']['trainer_id']
        selectedTime = session['metadata']['selectedTime']

        course = Course.objects.get(id=course_id)
        user = CustomUser.objects.get(id=user_id)
        trainer = Trainer.objects.get(id=trainer_id)
        amount_paid = course.course_fee

        print(course,'--------11111111')
        print(user,'-----22222222')
        print(trainer,'-----3333333333333')
        print(amount_paid,'---------444444444')

        #sending confimation mail

        #creating payment object

        validupto = timezone.now() + timedelta(days=30)

        PaymentHistory.objects.create(user=user ,amount_paid=amount_paid, trainer=trainer , payment_status=True)
        PurchasedOrder.objects.create(user=user, selected_trainer=trainer, selected_course=course, time_slot=selectedTime, valid_up_to=validupto )

    return HttpResponse(status=200)






class PaymentListView(APIView):

    def get(self, request, format=None):
        payments = PaymentHistory.objects.all()
        serializer = PaymentViewSerializer(payments, many=True)
        return Response(serializer.data)
    


class TrainerStudentsListView(APIView):

    def get_trainer(self, id):
        try:
            user = CustomUser.objects.get(id=id)
            return Trainer.objects.get(user=user)
        except Trainer.DoesNotExist:
            raise Http404
        

    def get(self, request, id, format=None):
        trainer = self.get_trainer(id)
        print(trainer,'-----trainer')
        students = PurchasedOrder.objects.filter(selected_trainer_id = trainer.id, valid_up_to__gte=timezone.now() )
        print(students,'---studentssssss')
        serializer = PurchasedOrderaSerializer(students, many=True)
        return Response(serializer.data)
    

class UserPurchasedCoursesListView(APIView):
    def get(self, request, id, format=None):
        user = CustomUser.objects.get(id=id)
        purchasedCourses = PurchasedOrder.objects.filter(user = user)
        print(purchasedCourses)
        serializer = PurchasedOrderaSerializer(purchasedCourses, many=True)
        return Response(serializer.data)
        


class CheckCoursePurchase(APIView):
    def get(self, request, id): 
        user_id = request.query_params.get('userId')
       # Assuming you are using authentication
        
        try:
            purchased_order = PurchasedOrder.objects.get( user_id =user_id,  selected_course_id=id)
            if purchased_order.valid_up_to >= timezone.now():
                return Response({"message": "User has already purchased this course and it's valid."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User has already purchased this course but it's expired."}, status=201)
        except PurchasedOrder.DoesNotExist:
            return Response({"message": "User has not purchased this course."}, status=status.HTTP_404_NOT_FOUND)
        


class MonthlyPaymentDataView(APIView):
    def get(self, request):
        data = PaymentHistory.objects.annotate(
            month=ExtractMonth('purchased_date'),
            year=ExtractYear('purchased_date')
        ).values('month', 'year').annotate(
            total_payment=Sum('amount_paid')
        ).order_by('year', 'month')

        serializer = MonthlyPaymentSerializer(data, many=True)

        return Response(serializer.data)