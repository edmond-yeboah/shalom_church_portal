from django.contrib import messages
from accounts.models import Customusers
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from AdminSide.models import sermon,announcement
from .models import comment,Payment, family
from django.db.models import Q
from django.http import HttpRequest,HttpResponse
import secrets
from django.conf import settings
import random
from accounts.models import quote
# Create your views here.
@login_required(login_url='login')
def userdash(request):
    context={}

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

    #getting all announcements
    allannounce = announcement.objects.all().order_by('-id') #getting all announcements
    context['allannounce'] = allannounce #putting in a context to be rendered on the frontend

    return render(request, 'home.html',context)




@login_required(login_url='login')
def announce(request):
    context= {}

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

    #getting all the announcements
    allannounce = announcement.objects.all().order_by('-id')
    context['allannounce'] = allannounce

    return render(request,'announce.html',context)




@login_required(login_url='login')
def sermons(request):
    context={}
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

    #getting all announcements
    allannounce = announcement.objects.all().order_by('-id') #getting all announcements
    context['allannounce'] = allannounce #putting in a context to be rendered on the frontend

    if request.method=="POST": #checking if a post request was received
        action = request.POST['action'] #getting the type of button that was clicked

        if action=="search": #if user clicked the search button
            searchquery = request.POST['searchquery'] #get the search query entered by the user
            if len(searchquery)>0: #if user enteres search query
                searchresults = sermon.objects.filter(Q(title__icontains=searchquery)) #searching sermons by title
                if len(searchresults)>0: #if search matched any sermon in the database
                    context["allsermons"] = searchresults #display sermon to the user
                else: #if search didn't match any sermon in the database
                    context["nosermonresult"] = "No sermon title matches search query "+"'"+searchquery+"'" #display this message to admin
            else:
                context["nothingentered"] = "No search query entered" #display message if user doesnt enter search query
        elif action=="comment": #if user clicked to comment on a sermon
            comments = request.POST['comment'] #get the comment entered by the user
            sermonid = request.POST['sid'] #get the sermon id of sermon user commented on
            user = Customusers.objects.get(id = request.user.id)#get the user who commented
            
            SermonCommentedOn = sermon.objects.get(id=sermonid) #getting the sermon commented on with the id
            newcomment = comment()
            newcomment.by=user #setting the user who commented
            newcomment.cfor = SermonCommentedOn #setting the sermon this comment belongs to
            newcomment.content = comments #setting the comment content
            newcomment.save() #saving the comment
            context['sdetails'] = SermonCommentedOn #putting the sermon fetched into the context list

            #fetching comments for sermon
            SermonComments = comment.objects.filter(cfor=SermonCommentedOn) #fetching comments for the sermon
            context['comments'] = SermonComments #putting comments in a context list
             
    elif "sid" in request.GET: #if user click to view details of a sermon
        sid = request.GET['sid'] #get the id of the sermon
        Sermon = sermon.objects.get(id=sid) #get the sermon with the id received
        context["sdetails"] = Sermon #putting the sermon fetched into a list to pass it to the user

        #fetching comments for sermon
        SermonComments = comment.objects.filter(cfor=Sermon) #fetching comments for the sermon
        context['comments'] = SermonComments #putting comments in a context list

    else:
        #fetching all sermons
        allsermons = sermon.objects.all().filter(deleted=False) #fetching all sermons that have not been deleted
        if len(allsermons)>0: # if there are sermons in the database
            context["allsermons"] = allsermons #putting the sermons fetched into the context list
        else:
            context["nosermons"] = "There are no sermons..." #if there are no sermons show this message     
    return render(request,'sermons.html',context)




@login_required(login_url='login')
def profile(request):
    context={}

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

    #getting all announcements
    allannounce = announcement.objects.all().order_by('-id') #getting all announcements
    context['allannounce'] = allannounce #putting in a context to be rendered on the frontend

    global famexits 
    famexits = False
    #get the user's username
    user = Customusers.objects.get(username=request.user.username)
    try:
        fam = family.objects.get(who=request.user.id)
        context["fam"] = fam
        famexits = True
    except Exception as e:
        print(e)

    #fetching all users excluding admin and super users
    allusers = Customusers.objects.all().exclude(is_superuser=True).exclude(admin=True).filter(is_active=True)
    context["allusers"] = allusers

    if request.method == "POST": #checking if a post request was sent
        action = request.POST['action'] #getting the value for the aciton
        if action=="profile": #if the value for the action is profile

            try:
                fname = request.POST['fname'] #getting the first name entered by the user
                lname = request.POST['lname'] #getting the last name entered by the user
                tel = request.POST['phone'] #getting the phone number entered by the user
                bio = request.POST['bio'] #getting the bio entered by the user
                age = request.POST['age'] #getting the age entered by the user
                email = request.POST['email'] #getting the email entered by the user
                password = request.POST['password'] #getting the password entered by the user

                #checking if the user made a change of auth credentials change
                if len(password)>0: #if user submitted password

                    #updating user's profile info
                    user.first_name = fname #aetting user's first name to new name
                    user.last_name = lname #setting user's last name to new name
                    user.tel = tel #setting user's telephone to new telephone
                    user.bio = bio #setting user's bio to new bio
                    user.age = age #setting user's age to new age

                    #for authentication side
                    user.username = email #setting user's username to new email
                    user.email = email #setting user's email to new email
                    user.set_password(password) #setting user's new password
                    user.save() #saving changes to the database
                    messages.info(request,"Profile update successful, Remember to login next time with your new credentials!") #show this message
                    return redirect("/UserSide/profile/") #redirect to the profile page
                
                else: #if user doesn't make change of auth credential request
                    user.first_name = fname #setting user's first name to new name 
                    user.last_name = lname #setting user's last name to new name
                    user.tel = tel # setting user's telephone to new telephone
                    user.bio = bio #setting user's bio to new bio
                    user.age = age #setting user's age to new age
                    user.save() #saving changes to the database
                    messages.info(request,"Profile update successful") #show this message
                    return redirect("/UserSide/profile/") #redirect to the profile page
                    
            except Exception as e: #if an error occur while getting the information
                print(e) #print error message to terminal

        elif action =="family": #if user select to update family hierarchy

            newfam = family() #the family object
            count = 0 #int variable

            gfather = request.POST['gfather'] #get grand father selected
            gmother = request.POST['gmother'] #get grand mother selected
            father = request.POST['father'] #get father selected
            mother = request.POST['mother'] #get mother selected
            spouse = request.POST['spouse'] #get spouse selected
            child = request.POST.get('child') #get child or children selected

            # print(father)

            #getting the instance of the users selected
            if gfather == "none":
                pass
            else:
                thegfather = Customusers.objects.get(username=gfather)

                if famexits:
                    fam.gfather = thegfather
                    fam.save()
                else:
                    newfam.who = Customusers.objects.get(id=request.user.id)
                    newfam.gfather = thegfather #setting the user's grandfather
                    newfam.save()
                count +=1


            if gmother == "none":
                pass
            else:
                thegmother = Customusers.objects.get(username=gmother)

                if famexits:
                    fam.gmother = thegmother
                    fam.save()
                else:
                    newfam.who = Customusers.objects.get(id=request.user.id)
                    newfam.gmother = thegmother #setting the user's grandmother
                    newfam.save()
                count +=1


            if father == "none":
                pass
            else:
                thefather = Customusers.objects.get(username=father)

                if famexits:
                    fam.father = thefather
                    fam.save()
                else:
                    newfam.who = Customusers.objects.get(id=request.user.id)
                    newfam.father = thefather #setting the user's father
                    newfam.save()
                count +=1
                

            if mother == "none":
                pass
            else:
                themother = Customusers.objects.get(username=mother)

                if famexits:
                    fam.mother = themother
                    fam.save()
                else:
                    newfam.who = Customusers.objects.get(id=request.user.id)
                    newfam.mother = themother #setting the user's mother
                    newfam.save()
                count +=1


            if spouse == "none":
                pass
            else:
                thespouse = Customusers.objects.get(username=spouse)

                if famexits:
                    fam.spouse = thespouse
                    fam.save()
                else:
                    newfam.who = Customusers.objects.get(id=request.user.id)
                    newfam.spouse = thespouse #setting the user's spouse
                    newfam.save()
                count +=1


            if child == "None" or "none":
                pass
            else:
                print(child)
                thechild = Customusers.objects.get(username=child)

                if famexits:
                    fam.child = thechild
                    fam.save()
                else:
                    newfam.who = Customusers.objects.get(id=request.user.id)
                    newfam.child = thechild #setting the user's child
                    newfam.save()
                count +=1


            if count>=1:
                messages.info(request,"Family hierarchy update successful") #show this message
            return redirect("/UserSide/profile/") #redirect to the profile page

    return render(request,'profile.html',context)





@login_required(login_url='login')
def tithe(request: HttpRequest) -> HttpResponse:
    context={}

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

    #getting all announcements
    allannounce = announcement.objects.all().order_by('-id') #getting all announcements
    context['allannounce'] = allannounce #putting in a context to be rendered on the frontend
    
    #fetching user tithes
    userpayments = Payment.objects.filter(email=request.user.email).filter(verified=True) #fetch user payments with email since its unique for every user
    print(userpayments)
    if len(userpayments)>0:
        context["userpayments"] = userpayments #if results found, put in context list
    else: #if no results found
        context["nouserpayments"] = "You have not made any payments" #show message to user 

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        amount = request.POST['amount']
        try:
            newPayment = Payment()

            #generating a reference
            while not newPayment.ref:
                ref = secrets.token_urlsafe(10)
                similar_ref = Payment.objects.filter(ref=ref)
                if not similar_ref:
                    newPayment.ref = ref

            #multiplying amount by 100
            newamount = int(amount) * 100
            print(newamount)

            newPayment.fname = fname
            newPayment.lname = lname
            newPayment.email = email
            newPayment.amount = amount

            newPayment.save()

            context["amount"] = amount
            context["ref"] = ref
            context["publicKey"] = settings.PAYSTACK_PK
            context["email"] = email
            context["amount"] =newamount
            context["disamount"] = amount

            return render(request,'makepayment.html',context)
        except Exception as e:
            print(e)

    return render(request,'tithe.html',context)



def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment,ref=ref)
    verified = payment.verify_payment()
    print(verified)
    return redirect('tithe')