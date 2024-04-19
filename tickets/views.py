from django.shortcuts import render, redirect
from .models import maintickets
from .forms import TicketForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import maintickets
from django.core.mail import send_mail
def ticket_list(request):
    tickets = maintickets.objects.all()
    print(tickets)
    return render(request, 'ticket_list.html', {'tickets': tickets})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user

            # Handle the file upload
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                ticket.file_content = uploaded_file.read()  # Read and save the file content as binary

            ticket.save()
            return redirect('tickets:ticket_list')
    else:
        print("hhhhh")
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})


def ticket_update(request, id):
    ticket = maintickets.objects.get(id=id)  
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets:ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'ticket_form.html', {'form': form})
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
    tickets = maintickets.objects.filter(user=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})
@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user

            # Handle the file upload
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                ticket.file_content = uploaded_file.read()  # Read the file content as binary

            ticket.save()
            return redirect('tickets:ticket_list')
    else:
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})