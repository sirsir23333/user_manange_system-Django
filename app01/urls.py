from django.urls import path
from . import views

'''user/ handles the register and login, that is, the Sub task A
   user/1 allows individual user to see their info(Get), change their info(Put) and delete their account(Delete),
          that is, for Sub task B and C.
   AdminUser/ is an endpoint that only ADMIN can access. The admin can look for others info, update others info and delete
    others account. Admin can also downgrade himself/herself to non ADMIN and will be deny from accessing this endpoint.
    That is to said, the AdminUser/ is for the bonus sub task D'''

'''Since we are using restful api, we do not want our urls to have any verb. So I used user and AdminUser.'''

urlpatterns = [
    path("user/", views.UserView.as_view(), name="user-page"),
    path("user/1/", views.SingleUserView.as_view(), name="single-user-page"),
    path("AdminUser/", views.AdminUserView.as_view(), name="Admin-user-page"),
]
