from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

class CreditCardForm(forms.Form):
    age = forms.IntegerField(label= 'Age')
    income = forms.IntegerField(label = 'Income Per Year')
    costofliving = forms.IntegerField(label='Cost of Living per Year')
    numberdependents = forms.IntegerField(label='Number of Dependents')
    spending = forms.IntegerField(label='Spending Per Month')
    creditscore = forms.IntegerField(label='Credit Score')
    delinquency = forms.IntegerField(label='Delinquency Status', help_text = 'Put 1 if you have committed crime and put 0 if you have never been convicted of any crime.')
    maritalstatus = forms.IntegerField(label='Marital Status', help_text = 'Put 1 if married, put 0 if not married')

class UserCreateForm(UserCreationForm):
	firstname = forms.CharField(required=True)
	lastname = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	phone = forms.IntegerField(required=True)
	cardnumber = forms.IntegerField(required=True, label='Enter your credit card number')

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "email", "phone", "cardnumber")

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.firstname = self.cleaned_data["firstname"]
		user.email = self.cleaned_data["email"]
		user.phone = self.cleaned_data["phone"]
		user.cardnumber = self.cleaned_data["cardnumber"]
		if commit:
			user.save()
		return user
