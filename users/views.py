from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from users.models import UserProfile

# Create your views here.
@csrf_exempt
def create_user(request):
	resp = {}
	if request.method != 'POST':
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Only POST allowed'
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	_post_data = json.loads(request.body)
	name = _post_data.get('name', '')
	city = _post_data.get('city', '')
	errors = []
	if not name:
		errors.append('name required')
	if not city:
		errors.append('city required')
	if errors:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = errors
		return HttpResponse(json.dumps(resp), content_type = 'application/json')
	try:
		user_profile = UserProfile.objects.create(name = name, city = city)
		resp['status'] = 'success'
		resp['status_code'] = 200
		resp['city'] = user_profile.city
		resp['name'] = user_profile.name
		resp['id'] = user_profile.id
		resp['message'] = 'Successfully created user %s' % user_profile.id
	except Exception, e:
		resp['status'] = 'failed'
		resp['status_code'] = 400
		resp['message'] = 'Error in creating user %s' % e
	return HttpResponse(json.dumps(resp), content_type = 'application/json')
