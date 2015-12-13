from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from users.models import UserProfile
from cubes.models import UserCube

# Create your views here.
@csrf_exempt
def get_or_create_cubes(request, user_id):
	resp = {}
	try:
		user_profile = UserProfile.objects.get(id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	if request.method == 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif request.method == 'GET':
		cubes = UserCube.objects.filter(user_id = user_profile.id)
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = [cube for cube in cubes]
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

def create_cube_content(request):
	pass

def delete_cube_content(request):
	pass

def delete_cube(request):
	pass

def share_cube(request):
	pass
