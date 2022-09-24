from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import TicketForm, CommentForm

from .models import Ticket, Comment
#index page
#/
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            tickets = Ticket.objects.order_by('creation_date')
            return render(request, 'tickets/index.html', {'tickets':tickets})
        return render(request, 'tickets/index.html')
#ticket details page
#/tickets/details/{id}
def details(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            comments = Comment.objects.all().filter(ticket = ticket)
            return render(request, 'tickets/details.html', {'ticket':ticket, 'comments':comments})
        return render(request, 'tickets/index.html')

#/tickets/create/
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
    return redirect('/')

#/tickets/close/{id}
def close(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            ticket.status = 'CLOSED'
            ticket.save(update_fields=['status'])
            comment = Comment()
            comment.owner = request.user
            comment.ticket = ticket
            comment.closed = 1 #set closed to 1 so we can determine this comment is associated with the ticket being closed
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'You have successfully closed ticket {id}'.format(id = ticket.id))
                return redirect('/tickets/details/{id}'.format(id = pk))
            else:
                return redirect('/tickets/details/{id}'.format(id = pk))
        else:
            messages.add_message(request, messages.INFO, 'Error closing ticket - You cannot close a ticket owned by someone else.')
            return redirect('/tickets/details/{id}'.format(id = pk))
    return redirect('/')


def comment(request, pk):
    if request.method == "POST":
        if ticket.status == "CLOSED":
            messages.add_message(request, messages.WARNING, 'You tried commenting on a closed ticket.')
            return redirect('/tickets/details/{id}'.format(id = pk))
        else:
            ticket = Ticket.objects.get(pk=pk)
            comment = Comment()
            comment.owner = request.user
            comment.ticket = ticket
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Success! Your comment has been added.')
                return redirect('/tickets/details/{id}'.format(id = pk))
            else:
                messages.add_message(request, messages.WARNING, 'There was an error posting your comment.')
                return redirect('/tickets/details/{id}'.format(id = pk))
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