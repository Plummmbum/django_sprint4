from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.utils import timezone

from blog.constants import QUANTITY_PUB
from blog.models import Post


def get_published_posts(
        queryset: QuerySet = None,
        author=None,
        user=None,
        filter_flag=False,
        count_comment_flag=False,
        pub_posts=False,
        order_by='-pub_date'
     ):

    """Возвращает опубликованные посты."""
    if queryset is None:
        queryset = Post.objects.filter(
            pub_date__lte=timezone.now()
        )
    if filter_flag:
        queryset = queryset.filter(
            is_published=True,
            category__is_published=True
        )
    if count_comment_flag:
        queryset = queryset.annotate(comment_count=Count('comments'))
    queryset = queryset.select_related('author', 'location', 'category')
    if author and user == author:
        queryset = queryset.filter(author=author)
    return queryset.order_by(order_by)


def paginate(queryset, request, quantity_pub):
    paginator = Paginator(queryset, QUANTITY_PUB)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
