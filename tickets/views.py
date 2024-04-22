from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from .models import maintickets
from .forms import ContactForm, TicketForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm,CommentForm
from django.contrib.auth.models import Group, User
from .models import maintickets
from notifylibrary.email_sender import EmailSender #my customised library
from django.core.mail import send_mail
def ticket_list(request):
    tickets = maintickets.objects.all()
    print(tickets)
    return render(request, 'ticket_list.html', {'tickets': tickets})

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
@login_required
def ticket_update(request, id):
    ticket = get_object_or_404(maintickets, id=id)
    comments = ticket.comments.all()
    comment_form = CommentForm()
    is_superuser = request.user.is_superuser

    if request.method == 'POST':
        if 'submit_comment' in request.POST:  # Check if the comment button was clicked
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.ticket = ticket
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, "Your comment has been added.")
                return redirect('tickets:ticket_update', id=ticket.id)
        else:  # This will be true for ticket updates
            form = TicketForm(request.POST, instance=ticket, super_user=is_superuser)
            if form.is_valid():
                form.save()
                messages.success(request, "The ticket has been updated.")
                return redirect('tickets:ticket_list')

    else:  # GET request
        form = TicketForm(instance=ticket, super_user=is_superuser)

    # Fetch all teams and members for the dropdowns if the user is a superuser
    teams = Group.objects.all() if is_superuser else None
    members = User.objects.filter(is_staff=True) if is_superuser else None

    return render(request, 'ticket_form.html', {
        'form': form,
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'teams': teams,
        'members': members,
        'is_superuser': is_superuser
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tickets:ticket_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        print('Working',request)
        username = request.POST.get('username')
        password = request.POST.get('password1')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print('Suceess login')
                login(request, user)
                return redirect('tickets:ticket_list') 
        
            else:
                print("errrorrrr")
                return redirect('tickets:signup')
        except:
                print("erorrrrrrrr")
                print('out of if')

    return render(request,'login.html') 
from django.http import HttpResponse
from .models import maintickets

def serve_ticket_file(request, ticket_id):
    # Fetch the ticket by ID
    ticket = maintickets.objects.get(id=ticket_id)

    # Check if there's a file content
    if not ticket.file_content:
        return HttpResponse("No file attached to this ticket.", status=404)

    # Create a response with the appropriate content type
    response = HttpResponse(ticket.file_content, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(ticket.title + '.png')

    return response

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import maintickets

@login_required
def my_tickets(request):
    if request.user.is_superuser:
        tickets = maintickets.objects.all()
    else:
     tickets = maintickets.objects.filter(user=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})
@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        print('message sent')
        if form.is_valid(): 
            ticket = form.save(commit=False)
            ticket.user = request.user
            print('message sent')
            form.save()
            print('message sent')
            
            email_sender = EmailSender(
                smtp_server=settings.NOTIFYLIB_EMAIL_HOST,
                port=settings.NOTIFYLIB_EMAIL_PORT,
                username=settings.NOTIFYLIB_EMAIL_HOST_USER,
                password=settings.NOTIFYLIB_EMAIL_HOST_PASSWORD
            )
            
            # Send the email
            subject = f'New Ticket Created: {ticket.title}'
            message = f'Dear {ticket.user.username},\nYour ticket "{ticket.title}" has been successfully created.'
            print('user mail is')
            print(ticket.user.email)
            recipient_list = [ticket.user.email]

            # Using  the library to send the email
            try:
              email_sender.send_mail(subject, message, settings.NOTIFYLIB_EMAIL_HOST_USER, recipient_list)
              print('message sent')
            except Exception as e:
    # Log the error for debugging
                print(f"Failed to send email: {e}")
        return redirect('tickets:ticket_list')
    else:
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})
@login_required


def logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']  
            send_mail(
                f'Message from {name}', 
                message, 
                email, 
                [settings.ADMIN_EMAIL], # An admin email defined in settings.py
                fail_silently=False,
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})