from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    """
        To alter user model we created a function for user(normal user) and superuser
        (admin).

        create_user: this will get the username, email, user_type and password as well,
            and create a normal user
        create_superuser: this will also get the same info as normal user but this will create a 
            Admin user
    """

    def create_user(self, username , email, password, user_type):
        user = self.model(username=username, email=email, user_type=user_type)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, email, password, user_type):
        user = self.create_user(username=username, email=email, password=password, user_type=user_type)
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self.db)
        return user