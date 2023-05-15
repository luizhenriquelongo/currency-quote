from django.http import JsonResponse

from currencies.vat_comply_api import VATComplyAPI


def rates(request):
    api = VATComplyAPI()
    return JsonResponse(api.get_rates().dict())
