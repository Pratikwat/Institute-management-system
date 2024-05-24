from django.shortcuts import redirect, render
from app.models import Categories, Course, Author, Level, Video, UserCourse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.contrib import messages


def BASE(request):
    return render(request, 'base.html')

def HOME(request):
    categories = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')   # why we attched '-' before id coz it shows the last record first
    context = {"categories": categories, 'course' : course}
    return render(request, 'Main/home.html', context)

def single_course(request):
    category = Categories.get_all_categories(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    freecoursecount = Course.objects.filter(price = 0).count()
    paidcoursecount = Course.objects.filter(price__gte=1).count()
    context = { 'category': category, 'level': level, 'course': course, "freecoursecount": freecoursecount, "paidcoursecount": paidcoursecount}
    return render(request, 'Main/single_course.html', context)

def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in = category).order_by("-id")
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by("-id")
    else:
        course = Course.objects.all().order_by("-id")
    t = render_to_string('ajax/course.html', {'course': course})
    return JsonResponse({'data': t})

def contact_us(request):
    category = Categories.get_all_categories(Categories)
    context = {
        'category': category
    }
    return render(request, 'Main/contact_us.html', context)

def about_us(request):
    category = Categories.get_all_categories(Categories)
    context = {
        'category': category
    }
    return render(request, 'Main/about_us.html', context)

def search_course(request):
    category = Categories.get_all_categories(Categories)
   
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course': course,  'category': category
    }
    return render(request, 'search.html', context)

def course_details(request, slug):
    category = Categories.get_all_categories(Categories)
    time_duration = Video.objects.filter(course__slug = slug) .aaggregate(sum= Sum('time_duration'))
    course_id = Course.objects.get(slug = slug)
    try:

        check_enroll = UserCourse.objects.get(user = request.user, course = course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None
    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context = {
        'course': course, 'category': category, ' time_duration':  time_duration, 'check_enroll': check_enroll
    }
    return render(request, 'course/course_details.html', context)

def page_not_found(request):
    category = Categories.get_all_categories(Categories)
    context = {
        'category': category
    }
    return render(request, 'error/404.html', context)

def checkout(request, slug):
    course = Course.objects.get(slug = slug)
    
    if course.price == 0:
        course = UserCourse(user = request.user, course = course )
        course.save()
        messages.success(request, "courses are successfully enrolled")
        return redirect('my_course')
    return render(request, 'checkout/checkout.html')

def my_course(request):
    course = UserCourse.objects.filter(user = request.user)
    context = {
        'course': course
    }
    return render(request, 'course/my_course.html', context)