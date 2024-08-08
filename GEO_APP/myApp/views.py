import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os

def welcome(request):
    return render(request, 'index.html')

def index(request):
    return render(request, 'coordinate.html')

def generate_excel(request):
    if request.method == 'POST':
        data = request.POST.get('data', '')
        coordinates = data.split()
        longitude_list = []
        latitude_list = []
        for coord in coordinates:
            parts = coord.split(',')
            if len(parts) == 2:
                longitude, latitude = parts
                longitude_list.append(longitude)
                latitude_list.append(latitude)
            else:
                return HttpResponse("Invalid input format.", status=400)
        
        # Create a DataFrame
        df = pd.DataFrame({
            'Longitude': longitude_list,
            'Latitude': latitude_list
        })
        
         
        # Save the DataFrame to an Excel file on the server
        file_path = 'coordinates.xlsx'
        df.to_excel(file_path, index=False)

        # Redirect to the add_info view for further input
        return redirect('add_info')  # Start with the first row
    else:
        return HttpResponse("Only POST requests are allowed.", status=405)


import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os

def add_info(request):
    file_path = 'coordinates.xlsx'

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        # Load existing Excel file
        df = pd.read_excel(file_path)

        # Add Name and Description columns if not already present
        if 'Name' not in df.columns:
            df['Name'] = ''
        if 'Description' not in df.columns:
            df['Description'] = ''

        # Update all rows with the same Name and Description
        df['Name'] = name
        df['Description'] = description

        # Save the updated DataFrame back to the Excel file
        df.to_excel(file_path, index=False)

        # Redirect to the download page after saving
        return redirect('download_excel')  # Redirect to the final download page

    return render(request, 'add_info.html')


def download_excel(request):
    file_path = 'coordinates.xlsx'
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="coordinates.xlsx"'
            return response

    return HttpResponse('File not found')
