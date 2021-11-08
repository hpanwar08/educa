from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View

from courses.models import Course


# Create your views here.
class CourseChatRoom(LoginRequiredMixin, View):
    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):

        try:
            course = self.request.user.courses_joined.get(id=kwargs['course_id'])
        except Course.DoesNotExist:
            return HttpResponseForbidden()

        return render(self.request, self.template_name, {'course': course})
