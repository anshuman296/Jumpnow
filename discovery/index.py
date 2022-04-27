from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import InstagramData





@register(InstagramData)
class YourModelIndex(AlgoliaIndex):
    fields = ('id', 'full_name', 'username', 'location', 'bio')
    index_name = 'Instagram'
