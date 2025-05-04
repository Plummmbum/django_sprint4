from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.utils import timezone

from blog.constants import QUANTITY_PUB
from blog.models import Post


def get_published_posts(
        queryset: QuerySet = Post.objects.all(),
        filter_flag=True,
        count_comment_flag=True,
        order_by='-pub_date'
):
    """Возвращает опубликованные посты."""
    if filter_flag:
        queryset = queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
    if count_comment_flag:
        queryset = queryset.annotate(comment_count=Count('comments'))
    queryset = queryset.select_related('author', 'location', 'category')
    return queryset.order_by(order_by)


def paginate(queryset, request):
    paginator = Paginator(queryset, QUANTITY_PUB)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
