from rest_framework import serializers
from .models import Comments, TempUser
from rest_framework.validators import UniqueTogetherValidator


def multiple_of_five(value):
    if value % 5 != 0:
        raise serializers.ValidationError('Must be a multiple of 5')

def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Must be a multiple of 10')
    
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField(read_only=True) 
    int_a = serializers.IntegerField(validators=[multiple_of_five], required=False)
    int_b = serializers.IntegerField(validators=[multiple_of_ten], required=False)

    # Field-level
    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must be from @example.com domain")
        return value

    # Object-level
    def validate(self, data):
        if data['int_a'] < data['int_b']:
            raise serializers.ValidationError("int_a gretare than int_b")
        return data

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.int_a = validated_data.get('int_a', instance.int_a)
        instance.int_b = validated_data.get('int_b', instance.int_b)
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempUser
        fields = ['email', 'username']


class CommentModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    int_a = serializers.IntegerField(validators=[multiple_of_five], required=False)
    int_b = serializers.IntegerField(validators=[multiple_of_ten], required=False)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Comments
        # fields = '__all__'
        fields =  ['user', 'content', 'created', 'int_a', 'int_b', 'url']
        validators = [
            UniqueTogetherValidator(
                queryset=Comments.objects.all(),
                fields=['email', 'content'],
                message="This user already posted this comment."
            )
        ]

    # Field-level
    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must be from @example.com domain")
        return value

    # Object-level
    def validate(self, data):
        if data['int_a'] < data['int_b']:
            raise serializers.ValidationError("int_a should be greater than int_b")
        return data
        


# serializers.py

from rest_framework import serializers
from .models import Post, Reaction

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['content']

class PostSerializer(serializers.ModelSerializer):
    comment = ReactionSerializer()

    class Meta:
        model = Post
        fields = ['title', 'body', 'comment']

    def create(self, validated_data):
        comment_data = validated_data.pop('comment')
        post = Post.objects.create(**validated_data)
        Reaction.objects.create(post=post, **comment_data)
        return post

    def update(self, instance, validated_data):
        comment_data = validated_data.pop('comment', None)

        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()

        if comment_data:
            comment = instance.comment
            print("comment.content", comment.content)
            comment.content = comment_data.get('content', comment.content)
            comment.save()

        return instance
