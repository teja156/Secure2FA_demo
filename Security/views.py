from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
import requests
import ast
import json

# Create your views here.
def homepage(request):
	error = ""

	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
				data = {'s2fa_id':'f22402e3-2c16-11eb-8c26-00d861fc5607'}
				r = requests.post('http://127.0.0.1:5000/generate_otp',data=data)

				print("RAW OTP DATA : ",r.text)
				
				# otp = ast.literal_eval(r.text)[0]["otp"]
				otp = json.loads(r.text)[0]['otp']
				print("OTP received : ",otp)
				request.session['OTP'] = otp
			else:
				error = "yes"
		except Exception as e:
			print(e)
			error = "yes"
	d = {'error' : error}
	return render(request,'index.html',d)


def validate_otp(request):
	print("Checking otp")
	if(request.POST.get('otp_value')==request.session['OTP']):
		#Login success
		print("OTP valid")
		return render(request,'dashboard.html')
	else:
		print("OTP invalid")
		return render(request,'otp_page.html',{'error':'yes'})

def otp_page(request):
	return render(request,'otp_page.html')

def Logout(request):
	if not request.user.is_staff:
		return redirect('homepage')
	logout(request)
	return redirect('homepage')

def dashboard(request):
	return render(request,'dashboard.html')