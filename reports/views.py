from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

import csv
import datetime


# Create your views here.

@login_required
def index(request):
    return render(request, "reports/index.html")

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