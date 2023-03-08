from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as Login, logout as Logout
from django.contrib.auth.decorators import login_required
from .models import Customusers,quote
from AdminSide.models import sermon
import random

# Create your views here.
def home(request):
    context={} #list to hold data
    #fetching all sermons
    Sermons = sermon.objects.all()
    if len(Sermons)>=3: #if the number of sermons is greater than or equal to three
        onlythreesermons = sermon.objects.all()[:3] #fetch only three sermons for the homepage
        context["sermon"] = onlythreesermons #put only three sermons in the list
    else:
        allsermons = sermon.objects.all() #fetch all sermons
        context["sermon"] = allsermons #put all sermons in the list
    
    return render(request,'index.html',context)



def sermondetails(request):
    context={}
    if "sid" in request.GET:
        sid = request.GET['sid'] #get the id of the sermon
        Sermon = sermon.objects.get(id=sid) #get the sermon using the id
        context["sdetails"] = Sermon 
    return render(request,'single.html',context)


def login(request):
    context={}
    #getting the quote to display on the login page
    #getting the number of quotes in the database
    allqoutes = quote.objects.all()
    #getting the number of quotes
    quotetotal = len(allqoutes)
    #checking if there are quotes
    if quotetotal>0:
        #generating random number to get a quote at random from the database
        randomnuber = random.randint(1,quotetotal)
        #getting the quote with this random id
        thequote = quote.objects.get(id=randomnuber)
        context["thequote"] = thequote
    else:
        pass
    
    if request.user.is_authenticated: #checking if user is already logged in
        if request.user.admin: #checking if user is an admin
            return redirect('/AdminSide/adminhome') #if user is an admin, redirect to admin dashboard
        else:
            return redirect('/UserSide/userhome') #if user is not admin, redirect to user dashboard
    else: #if user is not logged in
        if request.method == "POST": #checking if a post request was received
            email = request.POST['email'] #getting the email entered by the user
            password = request.POST['password'] #getting the password entered by the user

            auth = authenticate(request, username=email, password=password) #authenticating user
            if auth is not None: #if authentication is successful
                Login(request,auth) #login user
                if request.user.admin: #if user is an admin
                    return redirect('/AdminSide/adminhome') #redirect user to admin dashboard
                else: #if user is not an admin
                    return redirect('/UserSide/userhome') #redirect user to user dashboard
            else: #if authentication is not successful
                messages.error(request,"Incorrect Email or Password. Register if you are a new user!") #message to the user

    return render(request,'login.html',context)




def register(request):

    context={}
    #getting the quote to display on the login page
    #getting the number of quotes in the database
    allqoutes = quote.objects.all()
    #getting the number of quotes
    quotetotal = len(allqoutes)
    #checking if there are quotes
    if quotetotal>0:
        #generating random number to get a quote at random from the database
        randomnuber = random.randint(1,quotetotal)
        #getting the quote with this random id
        thequote = quote.objects.get(id=randomnuber)
        context["thequote"] = thequote
    else:
        pass
    #checking if there was a post request 
    if request.method=="POST":
        email = request.POST['email'] #getting the email
        password1 = request.POST['password1'] #getting first password
        password2 = request.POST['password2'] #getting second password

        #checking if passwords match
        if password2==password1:
        
            #checking if email is already registered with an existing account
            if Customusers.objects.filter(email=email).exists():
                #telling the user this email is associated with an existing account
                messages.info(request,"This email is already registered with an existing account")
            else:
                #registering the user if email doesn't exist
                user=Customusers()
                user.username = email #setting the username to the email entered
                user.email = email #setting the email to the email entered
                user.set_password(password2) #setting the user password to the password entered
                user.save() #saving user credentials to database

                #loggin user in and redirecting to dashboard
                try:
                    auth = authenticate(request, username=email, password=password2) #authenticate user
                    if auth is not None: #if user login credentials are correct
                        Login(request,auth) #log user in
                        return redirect("/UserSide/userhome/") #redirect user to user dashboard
                    else: #if user login credentials are incorrect
                        return redirect("/accounts/login/") #redirect user to login page
                except Exception as e: #if an unkown error occur
                    print(e) #output error to terminal
        else:
            #telling the user the passwords entered do not match
            messages.error(request,"Passwords do not match")
    return render(request,'register.html',context)




@login_required(login_url='login') #login decorator
def logout(request):
    Logout(request) #logging user out
    return redirect("../../") #redirecting to the homepage
