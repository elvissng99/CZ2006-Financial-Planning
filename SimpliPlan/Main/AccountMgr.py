from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password, check_password

class AccountMgr:
    '''
    Helper class to perform User account related operation
    static methods are for non-authenticated functions, i.e. user has not logged in
    instance method are for authenticated functions, i.e. user logged in
    
    for static methods, you can call the function by:
        AccountMgr.login(username,password) #calling login function

    for instance method, i.e. non-static method, you need to instantiate
    an AccountManager Object, then call the function:
        user = AccountMgr.login(username,password) #get a user object from login
        accMgr = AccountMgr(user) #instantiate a AccountManager object using the User
        accMgr.changePassword(yourNewPassword) # changePassword for the User
        
    '''
    def __init__(self,user):
        self.user = user
    
    @staticmethod
    def login(username,password):
        try:
            user = User.user.get(username=username)
            if user:
                check = check_password(password, user.password)
                print(check)
                if check:
                    result = User.user.validate(username,user.password)
                    if len(result) > 0:
                        return result[0]
                    return False
        except:
            user = None
    
    @staticmethod
    def register(username, password, email):
        if len(User.user.exist(username,email)) > 0:
            return False
        else:
            newUser = User(username=username, password=make_password(password),email=email)
            newUser.save()
            return True

    def changePassword(self, newPassword):
        '''
        change password for user
        TODO: do some basic validation here
        '''
        self.user.password = newPassword
        self.user.save(update_fields=['password'])
        return True

    def changeEmail(self, newEmail):
        '''
        change email for user
        TODO: do some basic validation, i.e. no duplicate email allowed
        '''
        self.user.email = newEmail
        self.user.save(update_fields=['email'])        
        return True
    
    @staticmethod
    def sendResetLink(username, request):
        '''
        Send a email reset link for a username
        generate email reset link, and send to the email address
        '''
        #Generate reset link and send to email 
        email = AccountMgr.getEmailAddress(username)
        if email:
            subject='Reset Password Link'
            current_site = get_current_site(request)
            html_message=render_to_string('accounts/password_reset_email.html', {'domain': current_site.domain, 'username': username})
            send_mail(
				subject,
				html_message,
				email,
				[email],
				fail_silently=False,
			)
            return True
        else:
            return False

    @staticmethod
    def verify(username):
        '''
        Verify if username exist in the database
        '''
        qs = User.user.verify(username)
        if len(qs) == 0:
            return False
        else:
            return qs[0]

    @staticmethod
    def getEmailAddress(username):
        u = AccountMgr.verify(username)
        if u == False:
            return False
        else:
            return u.email

    @staticmethod
    def resetPassword(newPassword, username):
        email = AccountMgr.getEmailAddress(username)
        password = newPassword
        newUser = User(username=username, password=make_password(password),email=email)
        newUser.save()
        return True

