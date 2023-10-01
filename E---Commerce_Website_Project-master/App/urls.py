from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from App.forms import LoginForm, ChangePasswordForm, ResetPasswordForm, MySetPasswordForm


urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),

    # Paths Related Customer Profile , Address.
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),

    # Paths Related Purchasing of Products , Carts .
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('show_cart/', views.show_cart, name='show_cart'),

    path('pluscart/', views.plus_cart, name='plus_cart'),

    path('minuscart/', views.minus_cart, name='minus_cart'),

    path('removecart/', views.remove_cart, name='remove_cart'),

    # Paths Related Purchasing of Products , Checkout.
    path('buy/', views.buy_now, name='buy-now'),

    path('orders/', views.orders, name='orders'),

    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    # Paths Related to Product Pages , Details , Filters.
    path('mobile/', views.mobile, name='mobile'),

    path('mobile/<slug:data>', views.mobile, name='mobile'),

    path('laptop/<slug:data>', views.laptop, name='laptop'),

    path('laptop/', views.laptop, name='laptop'),

    path('topwear/', views.topwear, name='topwear'),

    path('topwear/<slug:data>', views.topwear, name='topwear'),

    path('bottemwear/', views.bottemwear, name='bottemwear'),

    path('bottemwear/<slug:data>', views.bottemwear, name='bottemwear'),

    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='product-detail'),

    # Paths Related to User Registration, Login , Authentication , Password Change , Reset, Forgot.

    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',
         authentication_form=LoginForm), name='login'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=ChangePasswordForm, success_url='/passwordchangedone/'),
         name='passwordchange'),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name='passwordchangedone.html'), name='passwordchangedone'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html', form_class=ResetPasswordForm), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
