from django.urls import path
from .views import PostCreateView,PostUpdateView,PostDeleteView,SubscriptionPlans,AboutView,ContactView
from .views import PostListView,User_Register,payment,process_payment
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('', PostListView.as_view(), name='post_list'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_create/',User_Register,name='user_create'),
    path('subscription_plans/',SubscriptionPlans.as_view(),name='subscription_plans'),
    path('about/',AboutView.as_view(),name='about'),
    path('contact/',ContactView.as_view(),name='contact'),
    path("payment/", payment, name="payment"),
    path("process_payment/", process_payment, name="process_payment"),
]
