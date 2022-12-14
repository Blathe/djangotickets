from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import TicketForm, CommentForm

from .models import Ticket, Comment
#index page
#/
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            tickets = Ticket.objects.all()
            
            if request.GET.get('filters') is not None or request.GET.get('sort') is not None:
                filters = request.GET.get('filters')
                sort = request.GET.get('sort')
                
                if (filters is not None):
                        tickets = tickets.filter(status = 'OPEN')
                if (sort is not None):
                    if sort == 'pHighToLow':
                        tickets = tickets.order_by('-priority')
                    elif sort == 'pLowToHigh':
                        tickets = tickets.order_by('priority')
                    elif sort == 'sOpenClosed':
                        tickets = tickets.order_by('-status')
                    elif sort == 'sClosedOpen':
                        tickets = tickets.order_by('status')
                    elif sort == 'NewestFirst':
                        tickets = tickets.order_by('-creation_date')
                    elif sort == 'OldestFirst':
                        tickets = tickets.order_by('creation_date')
               
                return render(request, 'tickets/index.html', {'tickets':tickets})
            else:    
                tickets = Ticket.objects.order_by('creation_date')
                return render(request, 'tickets/index.html', {'tickets':tickets})
    return render(request, 'tickets/index.html')
    
#ticket details page
#/tickets/details/{id}
def details(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            comments = Comment.objects.all().filter(ticket = ticket).order_by('-creation_date')
            return render(request, 'tickets/details.html', {'ticket':ticket, 'comments':comments})
        return render(request, 'tickets/index.html')

#/tickets/create/
@login_required
def create(request):
    if request.method == "POST":
        ticket = Ticket()
        ticket.owner = request.user
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Success! Ticket #{id} has been created.'.format(id = ticket.id))
            return render(request, 'tickets/details.html', {'ticket':ticket})
        else:
            messages.add_message(request, messages.INFO, 'Error creating ticket.')
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

@login_required
def open(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            ticket.status = 'OPEN'
            ticket.save(update_fields=['status'])
            comment = Comment()
            comment.owner = request.user
            comment.ticket = ticket
            comment.tag = 'REOPENED' #set tag to reopened to display a badge next to the comment
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'You have successfully reopened ticket #{id}'.format(id = ticket.id))
                return redirect('/tickets/details/{id}'.format(id = pk))
            else:
                messages.add_message(request, messages.WARNING, 'Error reopening ticket #{id}'.format(id = ticket.id))
                return redirect('/tickets/details/{id}'.format(id = pk))
        else:
            return redirect('/tickets/details/{id}'.format(id = pk))

#/tickets/close/{id}
@login_required
def close(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            ticket.status = 'CLOSED'
            ticket.save(update_fields=['status'])
            comment = Comment()
            comment.owner = request.user
            comment.ticket = ticket
            comment.tag = 'CLOSED' #set tag to closed to display a badge next to the comment.
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

@login_required
def comment(request, pk):
    if request.method == "POST":
        ticket = Ticket.objects.get(pk=pk)
        if ticket.status == "CLOSED":
            messages.add_message(request, messages.WARNING, 'You tried commenting on a closed ticket.')
            return redirect('/tickets/details/{id}'.format(id = pk))
        else:
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

@login_required
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