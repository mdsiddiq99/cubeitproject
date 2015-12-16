from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from users.models import UserProfile
from cubes.models import UserCube, Cube, CubeContent
from contents.models import UserContent, Content

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
		name = json.loads(request.body).get('name')
		if not name:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'name required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			cube = Cube.objects.create(name = name)
			print cube
			user_cube = UserCube.objects.create(user = user_profile, cube = cube)
		except Exception, e:
			print e
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error creating cube'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		resp['status'] = 'success'
		resp['status_code'] = 200
		resp['name'] = cube.name
		resp['user_id'] = user_profile.id
		resp['id'] = cube.id
		resp['message'] = 'Successfully created cube'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif request.method == 'GET':
		user_cubes = UserCube.objects.select_related('cube').filter(user_id = user_profile.id)
		cube_list = []
		for cube in user_cubes:
			cube_list.append({
					'id' : cube.cube_id,
					'name' : cube.cube.name,
					'user_id' : cube.user_id
				})
		resp['status'] = 'success'
		resp['status_code'] = 200
		resp['results'] = cube_list
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	else:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error in request type'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
@csrf_exempt
def create_cube_content(request, user_id, cube_id):
	resp = {}
	print request.method
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'POST method allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		user_profile = UserProfile.objects.get(id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		cube = UserCube.objects.get(cube_id = cube_id, user = user_profile)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Cube does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	content_id = json.loads(request.body).get('content_id')
	if not content_id:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'content_id required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	try:
		content = UserContent.objects.get(content_id = content_id, user_id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Content does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	try:
		cube_content = CubeContent.objects.create(cube = cube.cube, content = content.content)
	except Exception, e:
		print e
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error adding content to cube'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	resp['status'] = 'success'
	resp['status_code'] = 200
	resp['cube_id'] = cube.cube_id
	resp['content_id'] = content.content_id
	resp['user_id'] = user_profile.id
	resp['id'] = cube_content.id
	resp['message'] = 'successfully added content to cube'
	return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def delete_cube_content(request, user_id, cube_id, content_id):
	resp = {}
	try:
		user_profile = UserProfile.objects.get(id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		cube = UserCube.objects.get(cube_id = cube_id, user = user_profile)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Cube does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		content = UserContent.objects.get(content_id = content_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Content does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		cube_content = CubeContent.objects.get(cube = cube.cube, content = content.content).delete()
	except Exception, e:
		print e
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error deleting content from cube'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	resp['status'] = 'success'
	resp['status_code'] = 200
	resp['message'] = 'successfully deleted content from cube'
	return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def delete_cube(request, user_id, cube_id):
	resp = {}
	try:
		user_profile = UserProfile.objects.get(id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		cube = UserCube.objects.get(cube_id = cube_id, user = user_profile)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Cube does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')	
	try:
		CubeContent.objects.filter(cube = cube.cube).delete()
		Cube.objects.filter(id = cube.cube_id).delete()
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error deleting cube'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')	
	resp['status'] = 'success'
	resp['status_code'] = 200
	resp['message'] = 'Successfully deleted cube'
	return HttpResponse(json.dumps(resp), content_type = 'application/json')	

@csrf_exempt
def share_cube(request, user_id, cube_id):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'POST method allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		user_profile = UserProfile.objects.get(id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		cube = UserCube.objects.get(cube_id = cube_id, user = user_profile)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Cube does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	share_with_user_id = json.loads(request.body).get('user_id')
	if not share_with_user_id:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'user_id required'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	try:
		share_with_user = UserProfile.objects.get(id = share_with_user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist with id %s' % share_with_user_id
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	try:
		UserCube.objects.get_or_create(cube = cube.cube, user_id = share_with_user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error in sharing cube with %s' % share_with_user_id
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	resp['status'] = 'success'
	resp['status_code'] = 200
	resp['message'] = 'Successfully shared cube with %s' % share_with_user_id
	return HttpResponse(json.dumps(resp), content_type = 'application/json')

