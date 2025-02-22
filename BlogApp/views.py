import razorpay
from django.views.generic.edit import CreateView,DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from .models import Post,Author
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from .forms import UserForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model,login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content','author']  
    template_name = 'create_form.html' 
    success_url = reverse_lazy('post_list')  



class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'



class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content','author']   
    template_name = 'create_form.html'
    success_url = reverse_lazy('post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
User = get_user_model()
    
def User_Register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # Create a new Author instance manually
            user = Author(
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email1']
            )
            user.set_password(user_form.cleaned_data['password1'])  # Secure password hashing
            user.save()  # Save the new Author instance
            
            login(request, user)  # Automatically log in the user after signup
            return redirect('post_list')  # Redirect to blog homepage
    
    else:
        user_form = UserForm()

    return render(request, 'user_create.html', {'user_form': user_form})


class SubscriptionPlans(ListView):
    model = Post
    template_name = 'subscription_plans.html'
    context_object_name = 'posts'
    
    

class AboutView(ListView):
    model = Post
    template_name = 'about.html'
    context_object_name = 'posts'
    

class ContactView(ListView):
    model = Post
    template_name = 'contact.html'
    context_object_name = 'posts'
    
    
def payment(request):
    """ Renders the payment page with Razorpay integration. """
    plan_name = request.GET.get("plan", "Basic")
    plan_price = int(request.GET.get("price", "99")) * 100  # Convert to paisa

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create an order
    order_data = {
        "amount": plan_price,
        "currency": "INR",
        "payment_capture": "1"  # Auto-capture
    }
    order = client.order.create(order_data)

    return render(request, "payment.html", {
        "plan_name": plan_name,
        "plan_price": plan_price // 100,
        "razorpay_order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })

@csrf_exempt
def process_payment(request):
    """ Handle the Razorpay payment response. """
    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Verify payment
        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            return render(request, "success.html", {"payment_id": razorpay_payment_id})
        except razorpay.errors.SignatureVerificationError:
            return render(request, "failure.html")

    return redirect("subscription_plans")

def payment_success(request, payment_id):
    # Dummy email details
    subject = "Payment Confirmation"
    message = f"Your payment with ID {payment_id} was successful!"
    recipient_email = "dummy@example.com"  # Change this to a real email if needed

    # Send email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

    return render(request, 'mail_success.html')