from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

from django.db.models import Q

from .forms import TicketForm, CommentForm

from .models import Ticket, Comment


'''
This function handles all functionality for the ticket dashboard including Searches and Pagination.
'''
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            # This would probably be done differently on a larger product with more data but it will work for now.
            all_tickets = Ticket.objects.all()
            open_tickets = all_tickets.filter(status = "OPEN")
            closed_tickets = all_tickets.filter(status = "CLOSED")
            your_tickets = all_tickets.filter(owner = request.user)
            total_ticket_count = all_tickets.count()
            
            if request.GET.get('search') is not None:
                query = request.GET.get('search')
                                
                #double check to make sure the query exists
                if (query is not None):
                    
                    #Q tags define what fields we are searching in the Ticket model
                    search = Ticket.objects.filter(
                       Q(id__contains=query) | Q(title__icontains=query) | Q(description__icontains=query) | Q(owner__first_name__icontains=query) | Q(owner__username__icontains=query)
                    )

                    #grab all tickets and filter to grab any with a ticket number that matches the query
                    filtered_tickets = search
                    
                    if (request.GET.get('per_page')):
                        paginator = Paginator(filtered_tickets, request.GET.get('per_page'))
                    else:
                        paginator = Paginator(filtered_tickets, 10)

                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    #if the filtered ticket count is 0, send a warning message that no results were found.
                    if (filtered_tickets.count() == 0):
                        messages.add_message(request, messages.WARNING, 'No results found.')                    

                    return render(request, 'tickets/index.html', {'page_obj': page_obj, 'search_results': page_obj.paginator.count, 'open_tickets': open_tickets, 'closed_tickets' : closed_tickets, 'your_tickets' : your_tickets, 'total_tickets' : total_ticket_count})
                
            else:
                if request.GET.get('filters') is not None or request.GET.get('sort') is not None:
                    filters = request.GET.get('filters')
                    sort = request.GET.get('sort')
                    
                    if (filters is not None):
                            all_tickets = all_tickets.filter(status = request.GET.get('filters'))
                    if (sort is not None):
                        if (sort == "default"):
                            all_tickets = all_tickets.order_by("creation_date")
                        else:
                            all_tickets = all_tickets.order_by(sort)

                    if (request.GET.get('per_page')):
                        paginator = Paginator(all_tickets, request.GET.get('per_page'))
                    else:
                        paginator = Paginator(all_tickets, 10)

                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                        
                    return render(request, 'tickets/index.html', {'page_obj': page_obj, 'search_results': page_obj.paginator.count, 'open_tickets': open_tickets, 'closed_tickets' : closed_tickets, 'your_tickets' : your_tickets, 'total_tickets' : total_ticket_count})
                    
                if request.GET.get('my_tickets') is not None:
                    if request.GET.get('my_tickets') == "true":
                        all_tickets = your_tickets
                        
                all_tickets.order_by('creation_date')

                if (request.GET.get('per_page')):
                    paginator = Paginator(all_tickets, request.GET.get('per_page'))
                else:
                    paginator = Paginator(all_tickets, 10)

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                return render(request, 'tickets/index.html', {'page_obj': page_obj, 'search_results': page_obj.paginator.count, 'open_tickets': open_tickets, 'closed_tickets' : closed_tickets, 'your_tickets' : your_tickets, 'total_tickets' : total_ticket_count})
        else:
            return HttpResponseRedirect('/login')
    return render(request, 'tickets/index.html')       

'''
This function handles our custom login logic.
'''
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Error authenticating user. Check login credentials and try again.')
            return HttpResponseRedirect('/')
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return render(request, 'tickets/login.html')
        
'''
This function fetches a single ticket and returns ticket details and the details.html page.

/tickets/details/{id}
'''
@login_required
def details(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(pk=pk)
            comment = Comment()
            comment.owner = request.user
            comment.ticket = ticket
            comment.tag = 'CLOSED' #set tag to closed to display a badge next to the comment.
            form = CommentForm(request.POST)
            comments = Comment.objects.all().filter(ticket = ticket).order_by('-creation_date')
            return render(request, 'tickets/details.html', {'ticket':ticket, 'comments':comments, 'form': form})
        return render(request, 'tickets/index.html')

'''
This function handles creating a new ticket.

/tickets/create/
'''
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

'''
This function handles reopening a closed ticket.

/tickets/open/{id}
'''
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
            comment.tag = 'REOPENED' #set the tag to REOPENED so a badge is displayed next to the comment on the frontend.
            form = CommentForm(request.POST)
            if form.is_valid():
                comment.body = form.cleaned_data['body']
                comment.save()
                messages.add_message(request, messages.SUCCESS, 'You have successfully reopened ticket #{id}'.format(id = ticket.id))
                return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
            else:
                messages.add_message(request, messages.WARNING, 'Error reopening ticket #{id}'.format(id = ticket.id))
                return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
        else:
            return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))

'''
This function handles setting a ticket's status to Closed.

/tickets/close/{id}
'''
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
            comment.tag = 'CLOSED' #set the tag to CLOSED so a badge is displayed next to the comment on the frontend.
            form = CommentForm(request.POST)
            if form.is_valid():
                comment.body = form.cleaned_data['body']
                comment.save()
                messages.add_message(request, messages.SUCCESS, 'You have successfully closed ticket {id}'.format(id = ticket.id))
                return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
            else:
                return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
        else:
            messages.add_message(request, messages.INFO, 'Error closing ticket - you are not authorized to close a ticket.')
            return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
    return HttpResponseRedirect('/')

'''
This function handles creating a new comment on a ticket.

/tickets/comment/{id}
'''
@login_required
def comment(request, pk):
    if request.method == "POST":
        ticket = Ticket.objects.get(pk=pk)
        if ticket.status == "CLOSED":
            messages.add_message(request, messages.WARNING, 'You tried commenting on a closed ticket.')
            return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
        else:
            comment = Comment()
            comment.owner = request.user
            comment.ticket = ticket
            form = CommentForm(request.POST)
            if form.is_valid():
                comment.body = form.cleaned_data['body']
                comment.save()
                messages.add_message(request, messages.SUCCESS, 'Success! Your comment has been added.')
                return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
            else:
                messages.add_message(request, messages.WARNING, 'There was an error posting your comment.')
                return HttpResponseRedirect('/tickets/details/{id}'.format(id = pk))
    return HttpResponseRedirect('/')

'''
This function handles deleting a ticket.

/tickets/delete/{id}
'''
@login_required
def delete(request, pk):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(pk=pk)
        if ticket.owner == request.user:
            messages.add_message(request, messages.SUCCESS, "Success! Ticket #{pk} has been deleted!".format(pk = ticket.id))
            ticket.delete()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Error deleting ticket. You can only delete tickets you have created.')
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')