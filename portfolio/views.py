from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """
    Renders the main portfolio page.
    """
    return render(request, 'portfolio/index.html')

@csrf_exempt
def contact(request):
    """
    Handles the contact form submission.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not all([name, email, subject, message]):
            return JsonResponse({'success': False, 'message': 'Please fill in all fields.'}, status=400)
        
        # Email to the portfolio owner
        owner_subject = f"New Portfolio Message: {subject}"
        owner_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Email to the user who sent the message
        user_subject = f"Your Message Received: {subject}"
        user_message = f"Hello {name},\n\nYour message has been successfully received. I will contact you soon.\n\nThank you,\nYour Name"
        
        try:
            # Send email to the portfolio owner (your email)
            send_mail(
                owner_subject,
                owner_message,
                'your_email@gmail.com',  # Enter your sending email address here
                ['surya23051997@gmail.com'],  # Enter your receiving email address here
                fail_silently=False,
            )

            # Send confirmation email to the user
            send_mail(
                user_subject,
                user_message,
                'your_email@gmail.com',  # Enter your sending email address here
                [email],  # User's email address
                fail_silently=False,
            )
            
            return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
        except Exception as e:
            print(f"Error sending email: {e}")
            return JsonResponse({'success': False, 'message': 'There was an error sending the message.'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
