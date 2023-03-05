# app01_wavescan
Used Django and Django Restful API framework to built a project.
All the requirement in the task for back end have been done. I used class base view instead of function base view as it is more suitable for DRF.

1. In the url user/ corresponding to the view UserView. I have implemented an API that allows users to register,login and manage their accounts. I use post request for both login and register, while adding a param to seperate them. The param is action=login and action=register. I also define the get method for user/, it will simply return the two params in a JSON format, so that the front-end can help to direct.

2. Users can register by providing their email, password, user role, designation, company, first name, and last name. I do this by customizing the User Model in Django. Django's built-in User model provides several methods that can be used for authentication and managing user accounts, but the data User Model create for database is fixed. Hence, I customize it for adding and deleting field that eventually suite the task requirements.

3. To ensure security, passwords are securely hashed before being stored in the database. I do this by overriding the save method in the User Model.

4. Once registered, users can log in using their email address and password, and receive a JSON Web Token (JWT) for subsequent authentication. I do this by adding the module simple jwt that supports django 4.1.

5. In the url user/1/ corresponding to the view SingleUserView. I have provided users with the ability to view and update their personal information, including first and last names, email address, role, designation, and company, which is the get method. Additionally, users can delete their own account if needed, which is the delete method.

6. To ensure a smooth user experience, I have included error handling and input validation to ensure that appropriate responses are returned.

7. In the url AdminUser/ corresponding to the view AdminUserView. I have also implemented a bonus feature that allows admin users to manage other user accounts. Admin users can delete or update the roles of other user accounts. Admin can also downgrage themselve, and once such action is done, admin cannot access AdminUser/.

To summarize, the subtask A is done by 1,2,3,4. Subtask B, C is done by 5. Subtask D is done by 7.

More explanation about the code have been written as comments in the code.

Thank you so much.

Contact Info :
  Email: a269570234@gmail.com
  Telegram: sirsir233
