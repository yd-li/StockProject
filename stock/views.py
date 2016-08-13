from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from MongoManager import MongoManager
import json

mongo_manager = MongoManager()

def index(request):
    return HttpResponse("Stock app page is working.")

def call_api(request):
    response = mongo_manager.get_from_API()
    return JsonResponse(response)

def get_all_data(request):
    response = mongo_manager.list_all_data()
    ret = {"result": response}
    return JsonResponse(ret)
