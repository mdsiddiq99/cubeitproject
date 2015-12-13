# cubeitproject


Database credentials: in settings.py
Edit before running project

<!-- create user -->
POST 		/user
parameters : name and city

<!-- create cube -->
POST 		/user/:user_id:/cube
parameters : name

<!-- create content -->
POST 		/user/:user_id:/content
parameters : link

<!-- add content to cube -->
POST 		/user/:user_id:/cube/:cube_id:/content
parameters : content id

<!-- delete content from cube -->
DELETE 	/user/:user_id:/cube/:cube_id:/content/:content_id:

<!-- delete cube -->
DELETE 	/user/:user_id:/cube/:cube_id:

<!-- share cube -->
POST 		/user/:user_id:/cube/:cube_id:/share
parameters : user id

<!-- share content -->
POST 		/user/:user_id:/content/:content_id:/share
parameters : user id

<!-- list all cubes -->
GET 		/user/:user_id:/cube

<!-- list all contents -->
GET 		/user/:user_id:/content
