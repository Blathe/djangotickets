from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .forms import TicketForm

from .models import Ticket

def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            tickets = Ticket.objects.order_by('creation_date')
            return render(request, 'tickets/index.html', {'tickets':tickets})
        return render(request, 'tickets/index.html')

def details(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            return render(request, 'tickets/details.html', {'ticket':ticket})
        return render(request, 'tickets/index.html')

def close(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            ticket.status = "CLOSED"
            ticket.save()
            messages.add_message(request, messages.SUCCESS, 'Success! Ticket #{id} has been closed.'.format(id = ticket.id))
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'You are not authenticated')
            return redirect('/')

def create(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            ticket = Ticket()
            ticket.owner = request.user
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Success! Ticket #{id} has been created.'.format(id = ticket.id))
                return redirect('/')
            else:
                messages.add_message(request, messages.INFO, 'Error creating ticket.')
                return redirect('/')
        return redirect('/')

def delete(request, pk):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(pk=pk)
        if ticket.owner == request.user:
            messages.add_message(request, messages.SUCCESS, "Success! Ticket #{pk} has been deleted!".format(pk = ticket.id))
            ticket.delete()
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Error deleting ticket. You can only delete tickets you have created.')
            return redirect('/')
    return redirect('/')