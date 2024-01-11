from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
import datetime

def call_api_ep(request):
    listed_data = []
    start = int(request.GET.get("start_month",10))
    end = int(request.GET.get("end_month",11))
    if (start <= 0 or end >= 13 or start > end):
        return {"error":"Please enter valid month range!!"}
    url = "http://canteen.benzyinfotech.com/api/v3/customer/report?"
    if request.method=="GET":
        for month in range(start,end+1):
            payload = json.dumps({
                        "month": int(month)
                        })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZWRhNWExODU0OTFhYWE0MmY5YzMyZjRhMTU5MDM1ODk4ZjZiMzMxNWUzZjJjNGRiZDA1N2IyNGE3NTAzMDc3NDBlMjFlYjZmNGE4Mjk0MGUiLCJpYXQiOjE3MDQ4MDA4OTAuODc5OTI1OTY2MjYyODE3MzgyODEyNSwibmJmIjoxNzA0ODAwODkwLjg3OTkyOTA2NTcwNDM0NTcwMzEyNSwiZXhwIjoxNzM2NDIzMjkwLjgzNDkxMjA2MTY5MTI4NDE3OTY4NzUsInN1YiI6IjI2NSIsInNjb3BlcyI6W119.CwDEjlHoRtOXdFcaO6KGGxV202AOA7MMtJVPtKzgLqzTFzUUnDLGBd7PNAtHO2--3YOathM9HOG8hYjY8wjktXZIoCGUR9GWIaEVUxLwFq927CrSf05NuqTBTrJcDeBOjXDvKcSBiJ2A994FC2IunPcdkaZ4jpoaWBIaWueYUbHviYSQuLec3tFcAMg4njrImAlaN9k-QKkHetpdrdbUEX1Wzq4X-1QwuOx7W3W2nbbxaoNgFX1gaabxi00ZO7h5MokGvtqy_gCkS9TYoM74VfxmTyAAczjttLcPqDNiAL_ZJdutDMezw32CZj8G8l8PUL46F_BuaxatZDBUZxeClZh4_0Wvo9GX4zqF2XvHdzZHnwdB414vNCl8itaGW9w7QWbdchPOglhnek32ZmkH0MIqeOBhnAyHo5_WbP0uLd_3qmz3w04nvTbTGV25-QebaxPAsVD0-7Za1sVpqB_FD6yEeliaEzdxl_8gA5IH59uowpfPYgUIjom8NVEASuYsAwb0q3f0jhNRfwg2zmXNenoDunh_dN9l2NRjI2gdZueSMwu6IJLQK46jpn01uG2iQ1xx-pFJAGe_bzSceLsho3dbtabym3tMqi0Ac02xUP9Mn50LdkFJGNVU9jiuHQfyjQirDtGUfya3aIvpJlCGx9Cx99s_4P89uDnOiXy3A1Q'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            listed_data.extend(response.json()['reports'])
        return {"reports":listed_data,"user":response.json()['user']}
    
def user_details(request):
    response = call_api_ep(request)
    if 'error' in response:
        return render(request, 'user_details.html', {"error":response})
    return render(request, 'user_details.html', {'user': response['user']})

def monthly_status(request):
    response = call_api_ep(request)
    if 'error' in response:
        return render(request, 'monthly_status.html', {"error":response})
    result, monthly_fine = generate_report(response['reports'])
    return render(request, 'monthly_status.html', {'monthly_statuses': result, "monthly_fine": monthly_fine})

def calculate_fine(opt_ins):
    fine = 0
    if isinstance(opt_ins, dict):
        for meal, status in opt_ins.items():
            if status == "Pending":
                fine += 100
    return fine

def generate_report(api_response):
    monthly_fine_total = 0
    result = []
    for report in api_response:
        date = datetime.datetime.strptime(report["date"], "%Y-%m-%d").strftime("%d-%b-%Y")
        opt_ins = report["opt_ins"]
        fine = calculate_fine(opt_ins)
        report['fine'] = fine
        result.append(report)
        monthly_fine_total += fine
    return result, monthly_fine_total
