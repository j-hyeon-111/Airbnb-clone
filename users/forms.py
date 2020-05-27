from django import forms
from . import models


class LoginForm(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


def clean(self):
    name = self.cleaned_data.get("name")
    password = self.clean_data.get("password")
    try:
        user = models.User.objects.get(username=name)
        if user.check_password(password):
            return self.cleaned_data
        else:
            self.add_error("password", forms.ValidationError("Password is Wrong"))
    except models.User.DoesNotExists:
        self.add_error("name", forms.ValidationError("Usere Does Not Exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        name = forms.CharField(max_length=80)
        password = forms.CharField(widget=forms.PasswordInput)
        password1 = forms.CharField(
            widget=forms.PasswordInput, label="Confirm Password"
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That user is already exists", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.name = name
        user.save()
