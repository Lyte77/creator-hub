from django.shortcuts import render
from allauth.account.views import SignupView
from django.shortcuts import render

# Create your views here.

class HTMXSignupView(SignupView):
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValueError as e:
            if self.request.htmx:
                return render(
                    self.request,
                    "partials/signup_errors.html",
                    {"error_message": str(e)},
                    status=400
                )
            else:
                form.add_error(None, str(e))
                return self.form_invalid(form)
