from django.shortcuts import redirect, render

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Perform authentication logic here
        print("request.POST",request.POST)
        # For example, check against a database or use Django's authentication system
        if username == 'admin' and password == 'password':
            print("This is true")
            return redirect('user')  # Redirect to the home page after successful login
        else:
            return render(request, 'valid/login.html', {'error': 'Invalid credentials'})
    return render(request, 'valid/login.html')

def logout_user(request):
    if request.method == 'POST':
        # Perform logout logic here
        print(request.POST)
        print(10/0)
        
        
