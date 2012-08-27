from django.shortcuts import render, render_to_response
from django.template import RequestContext
from blog.models import Article
from academics.models import Course
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect
from forms import ContactForm
from django.views.decorators.csrf import csrf_exempt

menu_items = [
        ('/about/', 'About'),
        ('/admission/', 'Admission'),
        ('/achievements/', 'Achievements'),
        ('/activities/', 'Activities'),
        ('/people/', 'People'),
        ('/courses/', 'Courses'),
        ('/contact-us/', 'Contact Us')
    ]


def index(request):
    global menu_items
    return render(request, "mainpage.html", 
        {"activepage": "index", "menu": menu_items})

def about(request):
    global menu_items
    return render(request, "about.html", 
        {"activepage": "About", "menu": menu_items})

def courses(request):
    global menu_items
    semesters = ['I','II','III','IV','V','VI','VII']
    courses = []
    for sem in semesters:
        courses.append(Course.objects.filter(semester=sem))
    return render(request, "courses.html", 
        {"activepage": "Courses", "menu": menu_items, "courses": courses})

def about_course(request):
    global menu_items
    return render(request, "about-course.html", 
        {"activepage": "About", "menu": menu_items})

def achievements(request):
    global menu_items
    articles = Article.objects.filter(category='ACH').order_by('-date')
    return render(request, "timeline.html", 
        {"activepage": "Achievements", "menu": menu_items, "articles": articles})

def activities(request):
    global menu_items
    articles = Article.objects.filter(category='ACT').order_by('-date')
    return render(request, "timeline.html", 
        {"activepage": "Activities", "menu": menu_items, "articles": articles})

def admission(request):
    global menu_items
    return render(request, "admission.html", 
        {"activepage": "Admission", "menu": menu_items})

def people(request):
    from academics.models import *
    global menu_items

    '''
    DEMO

    user = UserExtended(1)
    print user.type
    user.type = "student"
    print user.type
    user.save()

    #del user.age

    '''


    return render(request, "people.html", 
        {"activepage": "People", "menu": menu_items})

@csrf_exempt
def contact_us(request):
    global menu_items
    response = ''
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            email = cd['email']
            message = cd['message']
            messageBody = '\n\nFROM: ' + email + '\n\nName: ' + name + '\n\nMessage: ' + message
            try:
                send_mail('[FAF]Contact us', messageBody, email, ['ana.balica@gmail.com'], fail_silently=False)
                # response = '<span>*</span> Thank you. We will consider your message as soon as possible and contact you.'
            except:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact-us/thanks/')
    # else:
    #     form = ContactForm()
    return render(request, "contact-us.html", 
        {"activepage": "Contact Us", "menu": menu_items, "form": form})

def thanks(request):
    global menu_items
    form = ContactForm()
    response = '<span>*</span> Thank you. We will consider your message as soon as possible and contact you.'
    return render(request, "contact-us.html",
        {"activepage": "Contact Us", "menu": menu_items, "form": form,"response": response})