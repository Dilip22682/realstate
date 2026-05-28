from django.contrib.auth.decorators import login_required
from .models import Property, Booking
from .forms import RegisterForm, PropertyForm,BookingForm
from django.contrib import messages 
from django.core.paginator import Paginator
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




#property list and search box


def property_list(request):
    qs = Property.objects.all().order_by('-id')

    search    = request.GET.get('search', '').strip()
    prop_type = request.GET.get('type', '').strip()
    price     = request.GET.get('price', '').strip()

    if search:
        qs = qs.filter(location__icontains=search)

    if prop_type:
        qs = qs.filter(property_type=prop_type)

    if price:
        price_ranges = {
            'low':  (1_000_000,  5_000_000),
            'mid':  (5_000_000,  10_000_000),
            'high': (10_000_000, None),
        }
        if price in price_ranges:
            low_val, high_val = price_ranges[price]
            qs = qs.filter(price__gte=low_val)
            if high_val:
                qs = qs.filter(price__lte=high_val)

    paginator  = Paginator(qs, 9)
    page_num   = request.GET.get('page', 1)
    properties = paginator.get_page(page_num)

    return render(request, 'property_list.html', {
        'properties': properties,
    })


# PROPERTY DETAIL + BOOKING
def property_detail(request, id):
    property_obj = get_object_or_404(Property, id=id)
    form         = BookingForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to book a property.')
            return redirect('login')

        form = BookingForm(request.POST)
        if form.is_valid():
            booking          = form.save(commit=False)
            booking.property = property_obj
            booking.user     = request.user
            booking.save()
            messages.success(request, '✅ Booking submitted! We will contact you shortly.')
            return redirect('property_detail', id=id)

    return render(request, 'property_detail.html', {
        'property': property_obj,
        'form':     form,
    })

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


# #Search box
# def properties(request):
#     queryset = Property.objects.all()

#     search = request.GET.get('search')
#     prop_type = request.GET.get('type')
#     price = request.GET.get('price')
#     print(search,prop_type,price)

#     if search:
#         queryset = queryset.filter(location__icontains=search)

#     if prop_type:
#         queryset = queryset.filter(type=prop_type)

#     if price == '10-50':
#         queryset = queryset.filter(price__gte=1000000, price__lte=5000000)
#     elif price == '50-100':
#         queryset = queryset.filter(price__gte=5000000, price__lte=10000000)
#     elif price == '100+':
#         queryset = queryset.filter(price__gte=10000000)

#     return render(request, 'properties.html', {'properties': queryset})



# ── My Bookings ──────────────────────────────────────────
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {
        'bookings': bookings,
    })