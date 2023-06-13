from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .api_resource.user_resource import UserResource
import json


class UserLogin:
    '''
    for login ,logout ,creating_user ,updating_user action function 
    '''

    rescource = UserResource()

    @csrf_exempt
    def login(request):
        '''
        login action function
        '''
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        username = data.get('username')
        password = data.get('password')
        if request.method == 'POST':
            response, status, cookie = UserLogin.rescource.login(
                username, password)
        else:
            response, status, cookie = {
                'error msg': 'Invalid request method'
            }, 400, None

        response = JsonResponse(response, status=status, safe=False)
        if cookie:
            response.set_cookie('authtoken', cookie['authtoken'])
        return response

    @csrf_exempt
    def logout(request):
        '''
        logout action function
        '''
        if request.method == 'POST':
            response, status, cookie = UserLogin.rescource.logout(request)
        else:
            response, status, cookie = {
                'error msg': 'Invalid request method'
            }, 400, None
        response = JsonResponse(response, status=status, safe=False)
        if cookie:
            response.set_cookie('authtoken', cookie['authtoken'], expires=0)
        return response

    @csrf_exempt
    def profile(request):
        '''
        Creating, Updating, Listing profile
        '''
        if request.method == 'POST':
            response, status, cookie = UserLogin.rescource.create_profile(request)
        elif request.method == 'GET':
            response, status, cookie = UserLogin.rescource.listing_profile(request)
        elif request.method == 'PATCH':
            response, status, cookie = UserLogin.rescource.updating_profile(request)
        else:
            response, status, cookie = {'error msg': 'Invalid request method'}, 400, None
        return JsonResponse(response, status=status, safe=False)

    @csrf_exempt
    def updating_profile_picture(request):
        '''
        Creating, Updating, Listing profile
        '''
        if request.method == 'POST':
            response, status, cookie = UserLogin.rescource.updating_profile_picture(request)
        else:
            response, status, cookie = {'error msg': 'Invalid request method'}, 400, None
        return JsonResponse(response, status=status, safe=False)

    @csrf_exempt
    def updating_profile_to_super_user(request):
        '''
        Creating, Updating, Listing profile
        '''
        if request.method == 'POST':
            response, status, cookie = UserLogin.rescource.updating_profile_to_super_user(request)
        else:
            response, status, cookie = {'error msg': 'Invalid request method'}, 400, None
        return JsonResponse(response, status=status, safe=False)
    