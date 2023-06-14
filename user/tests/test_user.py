from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Profile, UserPermission
from django.contrib.auth.hashers import check_password, make_password
import json


class UsersAPITestCase(TestCase):
    def setUp(self):
        # Create some sample users or set up your database with test data
        record = Profile.objects.create(username='testadmin',
                                        email='testadmin@admin.com',
                                        password=make_password('admin12'))
        profile_permission = UserPermission.objects.create(is_super_user=True,
                                                           user_profile=record)

        # Set up the API client
        self.client = APIClient()

    def test_create_users(self):
        # tying to add user without authentication
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'testuser1'
        }
        response = self.client.post('/api/user/profile/',
                                    data,
                                    format='multipart')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'fail to authenticate given user'}
        self.assertEqual(response_data, expected_data)
        # login authenticate user
        data = {"username": "testadmin", "password": "admin12"}
        json_data = json.dumps(data)
        response = self.client.post("/api/user/login/",
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = {'Success_msg': 'Logged in successfully'}
        self.assertEqual(response_data, expected_data)
        # adding porfile requeired field
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'testuser1'
        }
        response = self.client.post('/api/user/profile/',
                                    data,
                                    format='multipart')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = {'Success_msg': 'Profile created successfully'}
        self.assertEqual(response_data, expected_data)
        # Invalid email or user or password
        data = {
            'username': 'testuser1',
            'email': 'testuser.email.com',
            'password': 'testuser1'
        }
        response = self.client.post('/api/user/profile/',
                                    data,
                                    format='multipart')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'Inviald username or email or password'}
        self.assertEqual(response_data, expected_data)
        # Invalid email or user or password
        data = {
            # 'username': 'testuser1',
            'email': 'testuser@email.com',
            'password': 'testuser1'
        }
        response = self.client.post('/api/user/profile/',
                                    data,
                                    format='multipart')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'Inviald username or email or password'}
        self.assertEqual(response_data, expected_data)
        # Invalid email or user or password
        data = {
            'username': 'testuser1',
            'email': 'testuser@email.com',
            # 'password': 'testuser1'
        }
        response = self.client.post('/api/user/profile/',
                                    data,
                                    format='multipart')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'Inviald username or email or password'}
        self.assertEqual(response_data, expected_data)
        # creating already exiting Profile
        data = {
            'username': 'testuser1',
            'email': 'testuser@email.com',
            'password': 'testuser1'
        }
        response = self.client.post('/api/user/profile/',
                                    data,
                                    format='multipart')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'profile already persent'}
        self.assertEqual(response_data, expected_data)
    
    def test_updating_users(self):
        # updating profile without authentication
        data = {"username": "testadmin", "email": "testadmin@admin.com", "first_name":"admin1","last_name":"last","bio":"this bio"}
        json_data = json.dumps(data)
        response = self.client.patch('/api/user/profile/',
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'fail to authenticate given user'}
        self.assertEqual(response_data, expected_data)
        # login authenticate user
        data = {"username": "testadmin", "password": "admin12"}
        json_data = json.dumps(data)
        response = self.client.post("/api/user/login/",
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = {'Success_msg': 'Logged in successfully'}
        self.assertEqual(response_data, expected_data)
        # updating profile
        data = {"username": "testadmin", "email": "testadmin@admin.com", "first_name":"admin1","last_name":"last","bio":"this bio"}
        json_data = json.dumps(data)
        response = self.client.patch('/api/user/profile/',
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = {'Success_msg': 'Profile Updated successfully'}
        self.assertEqual(response_data, expected_data)
        # updating profile with invalid email
        data = {"username": "testadmin", "email": "testadmin.admin.com", "first_name":"admin1","last_name":"last","bio":"this bio"}
        json_data = json.dumps(data)
        response = self.client.patch('/api/user/profile/',
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'Inviald username or email'}
        self.assertEqual(response_data, expected_data)
        # updating profile with invalid username
        data = {"email": "testadmin@admin.com", "first_name":"admin1","last_name":"last","bio":"this bio"}
        json_data = json.dumps(data)
        response = self.client.patch('/api/user/profile/',
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'Inviald username or email'}
        self.assertEqual(response_data, expected_data)
        # updating profile with non existing profile
        data = {"username": "testadmin12", "email": "testadmin@admin.com", "first_name":"admin1","last_name":"last","bio":"this bio"}
        json_data = json.dumps(data)
        response = self.client.patch('/api/user/profile/',
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        expected_data = {'Error_msg': 'No Profile with this username or email exists'}
        self.assertEqual(response_data, expected_data)
        # get all profile
        response = self.client.get('/api/user/profile/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = [{'username': 'testadmin', 'email': 'testadmin@admin.com', 'first_name': 'admin1', 'last_name': 'last', 'bio': 'this bio', 'profile_picture': 'None'}]
        self.assertEqual(response_data, expected_data)
        # logout
        response = self.client.post('/api/user/logout/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = {'Success_msg': 'Logged out successfully'}
        self.assertEqual(response_data, expected_data)