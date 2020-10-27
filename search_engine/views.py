from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from search_engine.search_queries import Search


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def search_movies(request):
    try:
        results = []
        universe = request.GET.get('universe')
        query_param = request.GET.get('q')
        user_id = request.user.id

        # page_number = request.GET.get('page')
        # filter_name = request.GET.get('filter_name')
        # filter_value = request.GET.get('filter_value')        

        # if query_param is None or len(query_param.strip()) == 0:
        #     return JsonResponse({'result': 'Nothing to search!'}, status=status.HTTP_400_BAD_REQUEST)

        query_param = query_param.strip() if query_param else ''
        if universe is None or universe == '':
            universe = 'all'

        search_engine = Search(query_string=query_param, universe=universe, user_id=user_id)

        if query_param is None or len(query_param.strip()) == 0:
            results = search_engine.default_movies()
        else:
            results = search_engine.get_query_result()
    except Exception as e:
        print("eeee",e)
        results = []
    return JsonResponse(results,status=status.HTTP_200_OK,safe=False)




