from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


def index(request):
    return render(request, 'index.html')


# serializer 사용하는 (일반적인) django view
# HttpResponse의 하위 클래스를 만들고, 받은 데이터를 json 형태로 반환
class JSONResponse(HttpResponse):
    # content를 json으로 변환 후 httpresponse 형태로 반환
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# 만들 api의 최상단에서 저장된 코드 조각을 모두 보여주거나, 새 코드 조각을 만들 수 있음
# csrf_exempt 데코레이터: 인증되지 않은 사용자도 이 뷰에 post하도록 함
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


# 코드 조각 하나를 보여줄 뷰
# 코드 조각을 업데이트 혹은 삭제
@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
