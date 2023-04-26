from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.utils.timezone import now

import csv
import datetime

from tickets.models import Ticket

from .forms import ReportGenerationForm

# Create your views here.

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
            
            if group_by == "PRIORITY":
                all_tickets = all_tickets.order_by("priority")
            elif group_by == "USER":
                all_tickets = all_tickets.order_by("owner")
            elif group_by == "STATUS":
                all_tickets = all_tickets.order_by("status")
                
            paginator = Paginator(all_tickets, 100)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "reports/index.html", {"form": form, 'page_obj': page_obj})
    
    else:
        form = ReportGenerationForm()
        return render(request, "reports/index.html", {"form": form})
    
def csv_test(request):
    # Create the HttpResponse object with the appropriate CSV header.
    file_name = "report-" + datetime.now
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="{file}"'.format(file = file_name)},
    )

    writer = csv.writer(response)
    writer.writerow(["First row", "Foo", "Bar", "Baz"])
    writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])

    return response