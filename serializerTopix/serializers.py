from rest_framework import serializers
from .models import Comments, TempUser, Account, News, Category, Book, UserProfile, Novel, DataPointColor, Album, Track, TechArticle, BillingRecord
from rest_framework.validators import UniqueTogetherValidator
import re
from rest_framework import serializers
import time
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator, UniqueForDateValidator, UniqueForMonthValidator, UniqueForYearValidator


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
    # url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Comments
        # fields = '__all__'
        fields =  ['user', 'content', 'created', 'int_a', 'int_b']
        # fields =  ['user', 'content', 'created', 'int_a', 'int_b', 'url']
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


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'id', 'account_name', 'user_type', 'created']

        # extra_kwargs = {
        #     'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
        #     'users': {'lookup_field': 'username'}
        # }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
    
class NewsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='news-detail',
        lookup_field='pk'  # default; could use slug if needed
    )
    # category = CategorySerializer()

    class Meta:
        model = News
        fields = ['url', 'title', 'content','created']
        # fields = ['url', 'title', 'content', 'category', 'created']
        # extra_kwargs = {
        #     'url': {'view_name': 'news-detail', 'lookup_field': 'pk'}
        # }




# Custom ListSerializer
class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # Bulk create books
        books = [Book(**item) for item in validated_data]
        return Book.objects.bulk_create(books)

    def update(self, instance, validated_data):
        # Map id -> instance and id -> data
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                # Create new if not found
                ret.append(self.child.create(data))
            else:
                # Update existing
                ret.append(self.child.update(book, data))

        # Optionally handle deletions (this example skips deletion)
        return ret

# BookSerializer
class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Make id writable for update

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published']
        list_serializer_class = BookListSerializer  # Point to our custom ListSerializer




class BaseProfileSerializer(serializers.Serializer):
    bio = serializers.CharField()
    
    def validate_bio(self, value):
        if 'forbidden' in value:
            raise serializers.ValidationError("Bio cannot contain 'forbidden'.")
        return value

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)  
    
# Diamond inheritance" problem, where multiple parent classes inherit from the same grandparent.
# class UserProfileSerializer( BaseProfileSerializer, DynamicFieldsModelSerializer, serializers.ModelSerializer):
class UserProfileSerializer( BaseProfileSerializer, DynamicFieldsModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = rep['username'].lower()  # Force lowercase
        return rep

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        validated_data['email'] = validated_data['email'].lower()
        return validated_data
        # return super().to_internal_value(data)



class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = ['id', 'title', 'author']
        # include nested data for related models

        # depth is only for reading/output 
        depth = 1

        # Extra customization for individual fields
        # extra_kwargs = {
            # 'title': {'required': False},           # Make title optional
            # 'title': {'write_only': True}          # Only accept author in input, don't show in output
        # }


class Color:
    def __init__(self, red, green, blue):
        assert 0 <= red <= 255
        assert 0 <= red <= 255
        assert 0 <= red <= 255
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f"rgb({self.red}, {self.green}, {self.blue})"


class ColorField(serializers.Field):
    default_error_messages = {
        'incorrect_type': 'Expected a string but got {input_type}.',
        'incorrect_format': 'Expected `rgb(#,#,#)` format.',
        'out_of_range': 'Values must be between 0 and 255.',
    }

    def to_representation(self, value):
        # Convert Color instance → string
        return f"rgb({value.red}, {value.green}, {value.blue})"

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)

        if not re.match(r'^rgb\(\d{1,3},\s?\d{1,3},\s?\d{1,3}\)$', data):
            self.fail('incorrect_format')

        stripped = data.strip('rgb()')
        red, green, blue = [int(x.strip()) for x in stripped.split(',')]

        if any(c < 0 or c > 255 for c in (red, green, blue)):
            self.fail('out_of_range')

        return Color(red, green, blue)


class CoordinateField(serializers.Field):
    def to_representation(self, value):
        # obj is the full Product instance (because source='*'
        return {
            "x": value.x_coordinate,
            "y": value.y_coordinate
        }

    def to_internal_value(self, data):
        return {
            "x_coordinate": data["x"],
            "y_coordinate": data["y"]
        }

class NestedCoordinateSerializer(serializers.Serializer):
    x = serializers.IntegerField(source='x_coordinate')
    y = serializers.IntegerField(source='y_coordinate')


class DataPointColorSerializer(serializers.ModelSerializer):
    color = ColorField()
    # coordinates = CoordinateField(source='*')
    coordinates = NestedCoordinateSerializer(source='*')

    class Meta:
        model = DataPointColor
        fields = ['id', 'name', 'color', 'label', 'coordinates']

    def to_representation(self, instance):
        # Convert DB dict → Color instance for ColorField
        instance.color = Color(**instance.color)
        return super().to_representation(instance)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        # Convert Color instance → dict for DB
        color_obj = ret['color']
        ret['color'] = {'red': color_obj.red, 'green': color_obj.green, 'blue': color_obj.blue}
        return ret
    

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

# Custom relational fields
# class TrackListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         duration = time.strftime('%M:%S', time.gmtime(value.duration))
#         return 'Track List %d: %s (%s)' % (value.order, value.title, duration)


class TrackPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        # return 'Track List: %d' % (instance.title)
        return f"Tracks List: {instance.title}"
    
# serializer relation 
class AlbumSerializer(serializers.ModelSerializer):
# class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    # tracks = serializers.StringRelatedField(many=True)

    # tracks = serializers.PrimaryKeyRelatedField(
    #     many=True, 
    #     # read_only=True,
    #     queryset=Track.objects.all()
    # )

    # tracks = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     # read_only=True,
    #     queryset=Track.objects.all(),
    #     view_name='track-detail'
    # )

    # tracks = serializers.SlugRelatedField(
    #     many=True,
    #     # read_only=False,
    #     queryset=Track.objects.all(),
    #     slug_field='title'
    #  )
    
    # track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    # tracks = TrackSerializer(many=True)

    # tracks = TrackListingField(many=True, read_only=True)

    tracks = TrackPrimaryKeyRelatedField(
        many=True, 
        read_only=True,
        # queryset=Track.objects.all()
    )


    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
        # fields = ['album_name', 'artist', 'track_listing']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album

    def update(self, instance, validated_data):
        tracks_data = validated_data.pop('tracks')
        print('validated_data', validated_data)
        # Update album fields
        instance.album_name = validated_data.get('album_name', instance.album_name)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.save()
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()

        # Delete old tracks and create new ones (simplest way)
        instance.tracks.all().delete()
        for track_data in tracks_data:
            print("track_data", track_data) 
            Track.objects.create(album=instance, **track_data)

        return instance
    



class TrackHyperLinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='track-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Track
        fields = ['url', 'album', 'order', 'title', 'duration']


class AlbumHyperLinkSerializer(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Track.objects.all(),
        view_name='track-detail'
    )

    class Meta:
        model = Album
        fields = ['url', 'album_name', 'artist', 'tracks']



# vaildators
class TechArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[UniqueValidator(queryset=TechArticle.objects.all())]
    )
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TechArticle
        fields = ['title', 'slug', 'category', 'position', 'published', 'author']

        validators = [
            UniqueTogetherValidator(
                queryset=TechArticle.objects.all(),
                fields=['category', 'position'],
                message="This position is already taken in this category."
            ),
            UniqueForDateValidator(
                queryset=TechArticle.objects.all(),
                field='slug',
                date_field='published',
                message="Slug must be unique per day."
            ),
            UniqueForMonthValidator(
                queryset=TechArticle.objects.all(),
                field='slug',
                date_field='published',
                message="Slug must be unique per month."
            ),
            UniqueForYearValidator(
                queryset=TechArticle.objects.all(),
                field='slug',
                date_field='published',
                message="Slug must be unique per year."
            ),
        ]

# custom validators
def positive_amount(value):
    print("positive_amt validator")
    if value <= 0:
        raise serializers.ValidationError('Amount must be positive.')

class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        print("class validator")
        if value % self.base != 0:
            raise serializers.ValidationError(f'Must be a multiple of {self.base}')

class BillingRecordSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[positive_amount, MultipleOf(10)]
    )

    def validate(self, attrs):
        print("custom validation")
        client = attrs.get('client')
        date = attrs.get('date')
        if client and date:
            if BillingRecord.objects.filter(client=client, date=date).exists():
                raise serializers.ValidationError('This client already has a record for this date.')
        return attrs

    class Meta:
        model = BillingRecord
        fields = ['client', 'date', 'amount']
        extra_kwargs = {'client': {'required': False}}
        validators = []
