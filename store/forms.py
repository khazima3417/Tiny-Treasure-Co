from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Order, ContactMessage, Customer


class CustomerRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Your Full Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Email Address'
        })
    )
    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': '03XX XXXXXXX'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Create a password (min 6 characters)'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Username (or choose letters/numbers)'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match. Please re-enter them carefully.")
        if password and len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        return cleaned_data


class CustomerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Password'
        })
    )


class CheckoutOrderForm(forms.ModelForm):
    """Checkout form collecting sender, recipient, and order details."""
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'is_surprise_gift', 'recipient_name', 'recipient_address',
            'recipient_city', 'recipient_postal', 'card_message',
            'wax_seal_preference', 'delivery_instructions', 'payment_method'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'id': 'sender_name', 'required': 'required'}),
            'customer_email': forms.EmailInput(attrs={'id': 'sender_email', 'required': 'required'}),
            'customer_phone': forms.TextInput(attrs={'id': 'sender_phone', 'required': 'required'}),
            'is_surprise_gift': forms.CheckboxInput(attrs={'id': 'surprise-checkbox'}),
            'recipient_name': forms.TextInput(attrs={'id': 'recipient_name', 'required': 'required'}),
            'recipient_address': forms.TextInput(attrs={'id': 'recipient_address', 'required': 'required'}),
            'recipient_city': forms.Select(attrs={'id': 'recipient_city'}),
            'recipient_postal': forms.TextInput(attrs={'id': 'recipient_postal'}),
            'card_message': forms.Textarea(attrs={'id': 'card_message', 'rows': '4'}),
            'wax_seal_preference': forms.TextInput(attrs={'id': 'wax_seal_preference'}),
            'delivery_instructions': forms.TextInput(attrs={'id': 'delivery_notes'}),
            'payment_method': forms.RadioSelect(attrs={'name': 'payment_method'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Your Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'WhatsApp / Phone (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-space-md py-3 rounded-full bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Subject / Inquiry topic'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full p-space-md rounded-2xl bg-surface-container-low text-on-surface font-body-md focus:outline-none focus:ring-2 focus:ring-primary resize-none',
                'rows': 4,
                'placeholder': 'How can our concierge assist your bespoke gifting requirements?'
            }),
        }
