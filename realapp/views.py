from django.contrib.auth.decorators import login_required
from .models import Property, Booking
from .forms import RegisterForm, PropertyForm
from django.contrib import messages 

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404)

from django.contrib.auth import (
    authenticate,
    login,
    logout)



# HOME PAGE

def home(request):

    properties = Property.objects.all()

    return render(
        request,
        'home.html',
        {'properties': properties}
    )


# REGISTER PAGE

def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/login/')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


# LOGIN PAGE

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

    return render(
        request,
        'login.html'
    )


# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('/login/')


# DASHBOARD

@login_required(login_url='/login/')
def dashboard(request):
    my_properties = Property.objects.filter(owner=request.user)
    my_bookings = Booking.objects.filter(user=request.user)

    context = {
        'my_properties': my_properties,
        'my_bookings': my_bookings,
        'total_properties': my_properties.count(),
        'total_bookings': my_bookings.count(),
    }
    return render(request, 'dashboard.html', context)


# PROPERTY LIST PAGE

def property_list(request):

    properties = Property.objects.all()

    return render(
        request,
        'property_list.html',
        {'properties': properties}
    )


# PROPERTY DETAIL PAGE

def property_detail(request, id):

    property_obj = get_object_or_404(
        Property,
        id=id
    )

    return render(
        request,
        'property_detail.html',
        {'property': property_obj}
    )


#Property create
@login_required(login_url='/login/')
def create_property(request):

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            property_obj = form.save(commit=False)

            property_obj.owner = request.user

            property_obj.save()

            return redirect('/dashboard/')

    else:

        form = PropertyForm()

    return render(request,'create_property.html',{'form': form})

# UPDATE PROPERTY

 
@login_required(login_url='/login/')
def update_property(request, pk):
    
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=property_obj
        )

        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user  # ✅ was created_by, now owner
            property_obj.save()
            return redirect('/dashboard/')
        
        else:
            print(f"❌ Form errors: {form.errors}")

    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'update_property.html', {
        'form': form,
        'property': property_obj
    })


# DELETE PROPERTY

@login_required(login_url='/login/')
def delete_property(request, pk):

    property_obj = get_object_or_404(
        Property,
        id=pk
    )

    property_obj.delete()

    return redirect('/dashboard/')

# CONTACT DETAILS
def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name')
        email   = request.POST.get('email')
        phone   = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(name,email,phone,subject,message)

        # Save to database or send email here

        messages.success(request, f"Thanks {name}! We'll get back to you soon.")
        return redirect('/contact/')

    return render(request, 'contact.html')


# views.py
def about(request):
    return render(request, 'about.html')