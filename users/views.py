from rest_framework import status
from django.http import JsonResponse
from users.serializers import UserSerializer, AdminUserSerializer
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from users.models import AppUser
from search_engine.models import MovieDetails
from rest_framework.parsers import JSONParser
from search_engine.serializers import MovieDetailsSerializer
from search_engine.models import MovieDetails
@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.data['email'] = request.data.get('email').lower()
        data = request.POST
        mutable = request.POST._mutable
        data['is_agreed'] = request.POST.get('terms_condition',None)
        data['mobile_no'] = request.POST.get('mobile_number',None)
        admin_registration = request.POST.get('admin_registration',None)
        data._mutable = True    
       
        if data['password'] != data['confirm_password']:
        	return JsonResponse({'message':'Your password and confirmation password do not match'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

        data._mutable = mutable
        ''' This searializer will be for saving normal user '''
        serialized = UserSerializer(data=request.POST)
        ''' This searializer will be for saving Admin User '''
        if admin_registration == "true":
        	serialized = AdminUserSerializer(data=request.POST) 
        	
        if serialized.is_valid():
            user = serialized.save()
            token = Token.objects.create(user=user)
            json = serialized.data
            json['token'] = token.key
            return JsonResponse(json, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def login(request):
	try:
		email = request.POST.get("email")
		password = request.POST.get("password")
		if email is None or password is None:
			return JsonResponse({'error': 'Please provide both email and password'},
	                        status=status.HTTP_400_BAD_REQUEST)
		else:
			user = authenticate(username=email, password=password)

		if not user:
			return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
		Token.objects.filter(user=user).delete()
		token = Token.objects.create(user=user)
		res = {'token': token.key}
		status_code = status.HTTP_200_OK
	except Exception as e:
		print(e)
		res = {'message':'Something went wrong'}
		status_code = status.HTTP_400_BAD_REQUEST
	return JsonResponse(res,status=status_code)

@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def logout(request):
    email = request.POST.get("email")
    if email is None:
        return JsonResponse({'error': 'Please provide your email'},
                            status=status.HTTP_400_BAD_REQUEST)
    user = AppUser.objects.get(email=email)
    if not user:
        return JsonResponse({'error': 'Bad Request'},
                            status=status.HTTP_400_BAD_REQUEST)
    token = Token.objects.get(user=request.user)
    token.delete()
    return JsonResponse({'status': 'Logged out'},
                        status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST', 'PUT','DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,IsAdminUser))
def movies_details(request):
    if request.method == 'POST':
    	data = JSONParser().parse(request)
    	serialized = MovieDetailsSerializer(data=data)
    	if serialized.is_valid():
    		serialized.save()
    		return JsonResponse(serialized.data, status=status.HTTP_201_CREATED)
    	return JsonResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
    	try:
    		movie_data = MovieDetails.objects.get(pk=request.data['id'])
    	except Exception as e:
    		print(e)
    		movie_data = None
    	
    	if movie_data:
    		serialized = MovieDetailsSerializer(movie_data, data=request.data)
    		if serialized.is_valid():
    			serialized.save()
    			return JsonResponse(serialized.data,status=status.HTTP_200_OK)
    		return JsonResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    	else:
    		return JsonResponse({"message":"Movie does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
    	try:
    		movie_data = MovieDetails.objects.get(pk=request.data['id'])
    		movie_data.delete()
    		status_code = status.HTTP_200_OK
    		res = {"message":"Successfully deleted"}
    	except Exception as e:    		
    		status_code = status.HTTP_400_BAD_REQUEST
    		res = {"message":"Not Found"}
    	return JsonResponse(res,status=status_code)
    else:
    	return JsonResponse({'message':'Method not allowed'},status=status.HTTP_400_BAD_REQUEST)




