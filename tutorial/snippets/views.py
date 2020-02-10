from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


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

# upgrade! json뿐만 아니라 다른 콘텐츠 형태에 대한 요청이나 응답도 할 수 있도록 함
# 함수 기반 뷰에서 @api_view 데코레이터 사용
@api_view(['GET', 'POST'])
# format 키워드 추가
def snippet_list(request, format=None):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 코드 조각 하나를 보여줄 뷰
# 코드 조각을 업데이트 혹은 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
