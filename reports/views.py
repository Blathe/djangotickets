from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.utils import timezone

import csv
import datetime

from tickets.models import Ticket

from .forms import ReportGenerationForm

# Create your views here.


### 
# This is the index view for the Reports page. 
# It handles displaying the reports page as well as taking in the form data to generate reports 
###
@login_required
def index(request):
    if request.method == "POST":
        form = ReportGenerationForm(request.POST)
        
        if form.is_valid():
            user = form.cleaned_data['user']
            status = form.cleaned_data['status']
            group_by = form.cleaned_data['group_by']
            time = form.cleaned_data['time']
            
            if user is None:
                all_tickets = Ticket.objects.all()
            else:
                all_tickets = Ticket.objects.filter(owner = user)
                
            if status != "ANY":
                all_tickets = all_tickets.filter(status = status)

            if time == "LAST 7 DAYS":
                all_tickets = all_tickets.filter(creation_date__range=[timezone.now() - timezone.timedelta(days=7), timezone.now()])
            elif time == "LAST 30 DAYS":
                all_tickets = all_tickets.filter(creation_date__range=[timezone.now() - timezone.timedelta(days=30), timezone.now()])
            
            if group_by == "PRIORITY":
                all_tickets = all_tickets.order_by("priority")
            elif group_by == "USER":
                all_tickets = all_tickets.order_by("owner")
            elif group_by == "STATUS":
                all_tickets = all_tickets.order_by("status")
                
            """ if the user clicks the download CSV button """
            if "download-csv" in request.POST:
                
                if request.POST.get('name') is not None and request.POST.get('name') != "":
                    print(request.POST.get('name'))
                    file_name = request.POST.get('name')
                else:
                    file_name = "TicketReport-{date}".format(date = timezone.now().strftime("%Y-%m-%d"))
                    
                response = HttpResponse(
                    content_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="{file}"'.format(file = file_name)},
                )
                
                writer = csv.writer(response)
                writer.writerow(["Ticket ID", "Ticket Name", "Owner", "Created On", "Priority", "Status", "Date Closed"])
                
                for ticket in all_tickets:
                    writer.writerow([ticket.id, ticket.title, ticket.owner, ticket.creation_date, ticket.priority, ticket.status, ticket.closed_date])
                    
                return response
            else: 
                paginator = Paginator(all_tickets, 100)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, "reports/index.html", {"form": form, 'page_obj': page_obj})
        else:
            print(form.errors)
    else:
        form = ReportGenerationForm()
        return render(request, "reports/index.html", {"form": form})
    
def csv_test(request):
    # Create the HttpResponse object with the appropriate CSV header.
    file_name = "report-{date}".format(date = timezone.now())
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="{file}"'.format(file = file_name)},
    )

    form = ReportGenerationForm(request.POST)
        
    if form.is_valid():
        
        user = form.cleaned_data['user']
        status = form.cleaned_data['status']
        group_by = form.cleaned_data['group_by']
        time = form.cleaned_data['time']
        
        if user is None:
            all_tickets = Ticket.objects.all()
        else:
            all_tickets = Ticket.objects.filter(owner = user)
            
        if status != "ANY":
            all_tickets = all_tickets.filter(status = status)

        if time == "LAST 7 DAYS":
            all_tickets = all_tickets.filter(creation_date__range=[timezone.now() - timezone.timedelta(days=7), timezone.now()])
        elif time == "LAST 30 DAYS":
            all_tickets = all_tickets.filter(creation_date__range=[timezone.now() - timezone.timedelta(days=30), timezone.now()])
        
        if group_by == "PRIORITY":
            all_tickets = all_tickets.order_by("priority")
        elif group_by == "USER":
            all_tickets = all_tickets.order_by("owner")
        elif group_by == "STATUS":
            all_tickets = all_tickets.order_by("status")

            
        paginator = Paginator(all_tickets, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        writer = csv.writer(response)
        writer.writerow(["Ticket ID", "Ticket Name", "Owner", "Created On", "Priority", "Status", "Date Closed"])
        for ticket in all_tickets:
            writer.writerow([ticket.id, ticket.title, ticket.owner, ticket.created_on, ticket.priority, ticket.status, ticket.closed_date])

        return response