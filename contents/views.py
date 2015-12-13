from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from users.models import UserProfile
from cubes.models import UserCube, Cube, CubeContent
from contents.models import UserContent, Content

# Create your views here.
@csrf_exempt
def get_or_create_contents(request, user_id):
	resp = {}
	try:
		user_profile = UserProfile.objects.get(id = user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'User does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	if request.method == 'POST':
		link = request.POST.get('link')
		if not link:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'link required'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		try:
			content = Content.objects.create(link = link)
			user_content = UserContent.objects.create(user = user_profile, content = content)
		except Exception, e:
			resp['status'] = 'failed'
			resp['status_code'] = 400
			resp['message'] = 'Error creating content'
			return HttpResponse(json.dumps(resp), content_type = 'application/json')
		resp['status'] = 'success'
		resp['status_code'] = 200
		resp['link'] = content.link
		resp['user_id'] = user_profile.id
		resp['id'] = content.id
		resp['message'] = 'Successfully created content'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

	elif request.method == 'GET':
		user_content_ids = UserContent.objects.select_related('content').filter(user_id = user_profile.id).values_list('content_id', flat = True)
		user_cube_ids = UserCube.objects.select_related('content').filter(user_id = user_profile.id).values_list('cube_id', flat = True)
		cube_content_ids = CubeContent.objects.select_related('content').filter(cube_id__in = user_cube_ids).values_list('content_id', flat = True)
		user_content_ids = [c_id for c_id in user_content_ids]
		cube_content_ids = [c_id for c_id in cube_content_ids]
		content_ids = user_content_ids +  list(set(cube_content_ids) - set(user_content_ids))
		contents = Content.objects.filter(id__in = content_ids)
		content_list = []
		for content in contents:
			content_list.append({
					'id' : content.id,
					'link' : content.link,
					'user_id' : user_id
				})
		resp['status'] = 'success'
		resp['status_code'] = 200
		resp['results'] = content_list
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	else:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error in request type'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def share_content(request, user_id, content_id):
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
		content = UserContent.objects.get(content_id = content_id, user = user_profile)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Content does not exist'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	share_with_user_id = request.POST.get('user_id')
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
		UserContent.objects.get_or_create(content = content.content, user_id = share_with_user_id)
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error in sharing content with %s' % share_with_user_id
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	resp['status'] = 'success'
	resp['status_code'] = 200
	resp['message'] = 'Successfully shared content with %s' % share_with_user_id
	return HttpResponse(json.dumps(resp), content_type = 'application/json')
