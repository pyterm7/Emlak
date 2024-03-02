import re
from django.shortcuts import render, redirect
from Contact.models import ContactMessage
from django.contrib import messages


def ContactPage(request):
    #  Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
    else: ip = request.META.get('REMOTE_ADDR')
    # Email Regex
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    data = {}
    if request.POST:
        email = request.POST.get("contact_email", "")
        subject = request.POST.get("contact_subject", "")
        message = request.POST.get("contact_message", "")
        data['email'] = email 
        data['subject'] = subject
        data['message'] = message 
        if (re.fullmatch(email_regex, email)) and len(subject) < 100 and len(subject) > 10 and len(message) < 1000 and len(message) > 10: 
            try: 
                ContactMessage.objects.create(ip_address=ip, message=message, email=email, subject=subject)
                messages.success(request, "Mesajınız qeydə alındı.")
            except: messages.info(request, "Xəta oldu. Mesaj göndərilmədi.")
        else: messages.info(request, "Məlumatlar doğru şəkildə doldurulmadı. E-poçt doğru şəkildə yazılmalı, mövzu [11-99], mesaj [11-999] simvoldan ibarət olmalıdır.")
        return render(request, 'contact.html', context=data)
    return render(request, 'contact.html', context=data)