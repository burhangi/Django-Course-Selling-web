from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course, Video, UserCourse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='login'), name='dispatch')
class MyCoursesList(ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'

    def get_queryset(self):
        return UserCourse.objects.filter(user=self.request.user)

def coursePage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")

    if serial_number is None:
        serial_number = 1

    try:
        video = Video.objects.get(serial_number=serial_number, course=course)
    except Video.DoesNotExist:
        video = None
    except Video.MultipleObjectsReturned:
        video = Video.objects.filter(serial_number=serial_number, course=course).first()

    if video and not video.is_preview:
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            user = request.user
            if not UserCourse.objects.filter(user=user, course=course).exists():
                return redirect("check-out", slug=course.slug)

    context = {
        "course": course,
        "video": video,
        "videos": videos
    }
    return render(request, template_name="courses/course_page.html", context=context)
