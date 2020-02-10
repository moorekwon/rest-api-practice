'''
웹 api를 만들기 위해
Snippet 클래스의 인스턴스를 json 형태로 직렬화 혹은 반직렬화 해야함
django rest framework에서는 django 폼과 비슷한 방식으로 serializer 작성
'''
from rest_framework import serializers
from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


# serializer 클래스
# django form 클래스와 매우 비슷
# 결국은 ModelSerializer 클래스 사용하면 일일이 아래처럼 구현하지 않아도 됨..
class SnippetSerializer(serializers.ModelSerializer):
    # serializer가 ModelSerializer 클래스를 사용하도록 refactoring
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

    # pk = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # # django form의 widget=widgets.Textarea와 같음
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    #
    # # create 메소드
    # # serializer.save()가 호출됐을 때 인스턴스 생성
    # def create(self, validated_data):
    #     # 검증한 데이터로 새 Snippet 인스턴스 생성하여 리턴
    #     return Snippet.objects.create(**validated_data)
    #
    # # update 메소드
    # # serializer.save()가 호출됐을 때 인스턴스 수정
    # def update(self, instance, validated_data):
    #     # 검증한 데이터로 기존 Snippet 인스턴스를 update한 후 리턴
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
