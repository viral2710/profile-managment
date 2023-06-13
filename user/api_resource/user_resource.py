from ..models import Profile, UserPermission
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import uuid
import base64
import os
import json
import re


class UserResource:
    '''
  For login, logout, create, update user profile
  '''
    def login(self, username, password):
        '''
    letting user to login
    '''
        try:
            print(username, password)
            profile = Profile.objects.filter(username=username).first()
        except:
            return {'error_msg': 'invalid username'}, 400, None
        if check_password(password, profile.password):
            uuid_str = str(uuid.uuid4())
            user_permission = UserPermission.objects.filter(
                user_profile=profile).first()
            user_permission.token = uuid_str
            user_permission.save()
            return {
                'Success_msg': 'Logged in successfully'
            }, 200, {
                'authtoken': uuid_str
            }
        else:
            return {'error_msg': 'invalid password'}, 400, None

    def logout(self, request):
        '''
    letting user to logout
    '''
        try:
            authtoken = request.COOKIES.get('authtoken')
        except:
            return {'Error_msg': 'No token persent'}, 200, None
        if UserPermission.objects.filter(token=authtoken).exists():
            user_permission = UserPermission.objects.filter(
                token=authtoken).first()
            user_permission.token = None
            user_permission.save()
            return {
                'Success_msg': 'Logged out successfully'
            }, 200, {
                'authtoken': ''
            }
        return {'Error_msg': 'Invalid Authtoken'}, 200, None

    def create_profile(self, request):
        '''
    letting user to logout
    '''
        try:
            authtoken = request.COOKIES.get('authtoken')
        except:
            return {'Error_msg': 'No token persent'}, 200, None
        flag = False
        if authtoken is None:
            flag = self.getting_authentication(request)
        else:
            flag = UserPermission.objects.filter(
                token=authtoken).values('is_super_user').first()
        if flag:
            username = request.POST.get('username',None)
            email = request.POST.get('email',None)
            password = request.POST.get('password',None)
            if not (self.check_email_format(email) and username and password):
              return {'Error_msg': 'Inviald username or email'}, 400, None
            profile = Profile(username=username,
                              email=email,
                              password=make_password(password))

            first_name = request.POST.get('first_name', None)
            if first_name:
                profile.first_name = first_name

            last_name = request.POST.get('last_name', None)
            if last_name:
                profile.last_name = last_name

            bio = request.POST.get('bio', None)
            if bio:
                profile.bio = bio

            profile_picture = request.FILES.get('profile_picture', None)
            if password:
                profile.password = profile_picture

            profile.save()
            user_permission = UserPermission(user_profile=profile)
            user_permission.save()
            return {'Success_msg': 'Profile created successfully'}, 200, None
        else:
            return {'Error_msg': 'fail to authenticate given user'}, 200, None

    def listing_profile(self, request):
        '''
    letting user to logout
    '''
        try:
            authtoken = request.COOKIES.get('authtoken')
        except:
            return {'Error_msg': 'No token persent'}, 200, None
        flag = False
        if authtoken is None:
            flag = self.getting_authentication(request)
        else:
            flag = UserPermission.objects.filter(
                token=authtoken).values('is_super_user').first()
        if flag:
            profile_list = Profile.objects.all()
            response = [{
                'username':
                profile.username,
                'email':
                profile.email,
                'first_name':
                profile.first_name,
                'last_name':
                profile.last_name,
                'bio':
                profile.bio,
                'profile_picture':
                profile.profile_picture.url
                if profile.profile_picture else 'None'
            } for profile in profile_list]
            return response, 200, None
        else:
            return {'Error_msg': 'fail to authenticate given user'}, 200, None

    def updating_profile_picture(self, request):
        '''
    letting user to logout
    '''
        try:
            authtoken = request.COOKIES.get('authtoken')
        except:
            return {'Error_msg': 'No token persent'}, 200, None
        flag = False
        if authtoken is None:
            flag = self.getting_authentication(request)
        else:
            flag = UserPermission.objects.filter(
                token=authtoken).values('is_super_user').first()
        if flag:
            profile_picture = request.FILES.get('profile_picture')
            username = request.POST.get('username',None)
            email = request.POST.get('email',None)
            if not (self.check_email_format(email) and username):
              return {'Error_msg': 'Inviald username or email'}, 400, None
            profile = Profile.objects.get(username=username, email=email)
            old_image_path = profile.image_field.path
            profile.profile_picture = profile_picture

            profile.save()
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)
            return {
                'Success_msg': 'Profile picture Updated successfully'
            }, 200, None
        else:
            return {'Error_msg': 'fail to authenticate given user'}, 200, None

    def updating_profile_to_super_user(self, request):
        '''
    letting user to logout
    '''
        try:
            authtoken = request.COOKIES.get('authtoken')
        except:
            return {'Error_msg': 'No token persent'}, 200, None
        flag = False
        if authtoken is None:
            flag = self.getting_authentication(request)
        else:
            flag = UserPermission.objects.filter(
                token=authtoken).values('is_super_user').first()
        if flag:
            json_data = request.body.decode('utf-8')
            data = json.loads(json_data)
            username = data.get('username',None)
            if not username:
              return {'Error_msg': 'Inviald username'}, 400, None
            profile = Profile.objects.get(username=username)
            user_permission = UserPermission.objects.get(user_profile=profile)
            user_permission.is_super_user = True
            user_permission.save()
            return {'Success_msg': 'Profile is super user now'}, 200, None
        else:
            return {'Error_msg': 'fail to authenticate given user'}, 400, None

    def updating_profile(self, request):
        '''
    letting user to logout
    '''
        try:
            authtoken = request.COOKIES.get('authtoken')
        except:
            return {'Error_msg': 'No token persent'}, 400, None
        flag = False
        if authtoken is None:
            flag = self.getting_authentication(request)
        else:
            flag = UserPermission.objects.filter(
                token=authtoken).values('is_super_user').first()
        if flag:
            json_data = request.body.decode('utf-8')
            data = json.loads(json_data)
            username = data.get('username',None)
            email = data.get('email',None)
            if not (self.check_email_format(email) and username):
              return {'Error_msg': 'Inviald username or email'}, 400, None
            profile = Profile.objects.get(username=username, email=email)

            first_name = data.get('first_name', None)
            if first_name:
                profile.first_name = first_name

            last_name = data.get('last_name', None)
            if last_name:
                profile.last_name = last_name

            bio = data.get('bio', None)
            if bio:
                profile.bio = bio

            password = data.get('password', None)
            if password:
                profile.password = make_password(password)

            profile.save()
            return {'Success_msg': 'Profile Updated successfully'}, 200, None
        else:
            return {'Error_msg': 'fail to authenticate given user'}, 400, None

    @staticmethod
    def getting_authentication(request):
        '''
      Getting username and password with basic authentication
      '''
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Basic '):
            base64_decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
        username, password = base64_decoded.split(':')
        try:
            profile = Profile.objects.filter(username=username).first()
            if check_password(password, profile.password):
                user_permission = UserPermission.objects.filter(
                    user_profile=profile, is_super_user=True).exists()
                return user_permission
            return False
        except:
            return False

    @staticmethod
    def check_email_format(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            return False
