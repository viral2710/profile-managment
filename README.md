Task: 
Implement a Django API endpoint to create and update user profiles 

Description: 
You are tasked with creating a Django API endpoint that allows users to create and update their profiles. The profile should include fields such as name, email, bio, and profile picture. Users should be able to send POST requests to create a new profile or PATCH requests to update their existing profile. 

Result:-
  1->'/api/user/login/' to login user with content type application/json
  2->'/api/user/logout/' to logout the user
  3->'/api/user/profile/' is has 3 action :-
      *post with multipart formdata to create user
      *get to see all user
      *patch update multiple field with content type application/json (except profile pic)      
  4->'/api/user/updating_profile_picture/' post call to update profile picture with multipart formdata
  5->'/api/user/updating_profile_to_super_user/' post call with content type application/json to give a porfile user power to add and update profile

  Note:- step 3 to 5 can only be done by super user