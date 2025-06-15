from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from userprofile.forms import UserProfileForm
from userprofile.models import UserProfile



class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Returns the user profile for the currently logged-in user.
        """
        if not self.request.user:
            return None
        return UserProfile.objects.get(user=self.request.user)
