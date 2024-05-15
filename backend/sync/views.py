import json

from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from news.models import get_sync_content, sync_from_content


@method_decorator(csrf_exempt, name='dispatch')
class SyncResource(View):
    def get(self, request):
        sync_key = request.GET.get("key")
        if sync_key != settings.SYNC_KEY:
            print(f"Invalid key: {sync_key}")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid key."}))
        return JsonResponse(get_sync_content())

    def post(self, request):        
        # Check that the sync key is correct.
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            print("Invalid JSON.")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid JSON."}))

        sync_key = body.get("key")
        if sync_key != settings.SYNC_KEY:
            print(f"Invalid key: {sync_key}")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid key."}))
        
        if not isinstance(body.get("categories"), list) or not isinstance(body.get("articles"), list):
            print(f"Invalid data format: {body}")
            return HttpResponseBadRequest(json.dumps({"error": "Invalid data format."}))

        try:
            sync_from_content(body)
        except Exception as err:
            print(f"Error during sync: {err}")
            return HttpResponseBadRequest(json.dumps({"error": "Error during sync."}))        
        return JsonResponse({"status": "ok"})