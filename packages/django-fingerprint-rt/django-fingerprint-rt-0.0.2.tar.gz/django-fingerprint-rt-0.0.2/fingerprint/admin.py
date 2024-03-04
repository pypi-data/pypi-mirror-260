from datetime import timedelta
from functools import wraps
from itertools import chain, islice
from typing import Callable, Iterator

from django.contrib import admin
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Count, Prefetch
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.timezone import now

from .models import BrowserFingerprint, RequestFingerprint, UserFingerprint, UserSession

try:
    from itertools import pairwise
except ImportError:
    def pairwise(items):
        return zip(items, items[1:])


class html_objects_list:
    def __init__(self, format_string: str, max_items: int = 10):
        self.format_string = format_string
        self.max_items = max_items

    def __call__(self, fn: Callable) -> Callable:

        @wraps(fn)
        def wrapped(*args, **kwargs):
            results = list(islice(fn(*args, **kwargs), self.max_items))
            return format_html(
                '<br>'.join(self.format_string for _ in results),
                *chain.from_iterable(results)
            )

        return wrapped


class LargePaginator(Paginator):

    @cached_property
    def count(self):
        query = self.object_list.query
        if not query.where:
            cursor = connection.cursor()
            table_name = query.model._meta.db_table
            if '"."' in table_name:
                table_name = table_name.split('"')[-1]
            cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s", [table_name])

            estimate = int(cursor.fetchone()[0])
            if estimate > 1000:  # do the count anyway if estimate is suspiciously small
                return estimate

        return 0  # super().count


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = 'session_key', 'user', 'browser_fingerprints', 'request_fingerprints', 'created',
    list_filter = 'created',
    search_fields = 'user__username', 'session_key',
    ordering = '-created',

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('user')
            .prefetch_related(
                Prefetch(
                    'browserfingerprints',
                    queryset=BrowserFingerprint.objects.order_by('visitor_id', '-created').distinct('visitor_id'),
                ),
                Prefetch(
                    'requestfingerprints',
                    queryset=RequestFingerprint.objects.order_by('user_session', 'user_agent', '-created').distinct('user_session', 'user_agent'),
                ),
            )
        )

    @html_objects_list('{} &nbsp;&nbsp; <a href="{}"><code>{}</code></a>')
    def browser_fingerprints(self, instance) -> Iterator[tuple]:
        for fingerprint in instance.browserfingerprints.all():
            yield (
                fingerprint.created.date(),
                reverse('admin:fingerprint_browserfingerprint_changelist') + f'?user_session={instance.id}',
                fingerprint.get_value_display(),
            )

    @html_objects_list('{} &nbsp;&nbsp; <a href="{}"><code>{}</code></a>')
    def request_fingerprints(self, instance) -> Iterator[tuple]:
        for fingerprint in instance.requestfingerprints.all():
            yield (
                fingerprint.created.date(),
                reverse('admin:fingerprint_requestfingerprint_changelist') + f'?user_session={instance.id}',
                fingerprint.get_value_display(),
            )


class FingerprintBaseAdmin(admin.ModelAdmin):
    list_display = 'id', 'user_session', 'get_user',
    list_filter = 'created',
    ordering = '-created',
    search_fields = (
        'user_session__session_key',
        'user_session__user__email',
        'user_session__user__username',
        'url__value',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_session__user', 'url')

    @admin.display(description='user')
    def get_user(self, instance):
        return instance.user_session.user


@admin.register(BrowserFingerprint)
class BrowserFingerprintAdmin(FingerprintBaseAdmin):
    list_display = *FingerprintBaseAdmin.list_display, 'visitor_id', 'created',
    search_fields = (
        'visitor_id',
        *FingerprintBaseAdmin.search_fields,
    )


@admin.register(RequestFingerprint)
class RequestFingerprintAdmin(FingerprintBaseAdmin):
    list_display = *FingerprintBaseAdmin.list_display, 'ip', 'user_agent', 'created',

    search_fields = (
        'ip', 'user_agent', 'accept', 'content_encoding', 'content_language',
        *FingerprintBaseAdmin.search_fields,
    )


class NumFingerprintsFilter(admin.SimpleListFilter):
    groups = list(pairwise((1, 4, 6, 11, 21, 10_001)))
    query_parameter = None

    def lookups(self, request, model_admin):
        return [
            (f'{min_}-{max_-1}',)*2
            for (min_, max_) in self.groups
        ]

    def queryset(self, request, queryset):
        if not (raw_value := self.value()):
            return

        try:
            values = [int(value) for value in raw_value.split('-')]
            min_, max_ = values*2 if len(values) == 1 else values
        except ValueError:
            return

        return queryset.filter(**{
            f'{self.query_parameter}__gte': min_,
            f'{self.query_parameter}__lte': max_,
        })


class NumBrowserFingerprintsFilter(NumFingerprintsFilter):
    title = 'unique browser fingerprints'
    parameter_name = 'num_browser_fingerprints'
    query_parameter = 'num_browser_fingerprints'


class NumRequestFingerprintsFilter(NumFingerprintsFilter):
    title = 'unique request fingerprints'
    parameter_name = 'num_request_fingerprints'
    query_parameter = 'num_request_fingerprints'


class LastActivityListFilter(admin.SimpleListFilter):
    title = 'last activity'
    parameter_name = 'fingerprint_captured_within'

    def lookups(self, request, model_admin):
        return [
            (1, '1 day'),
            (7, '1 week'),
            (30, '1 month'),
            (90, '3 months'),
            (365, '12 months'),
        ]

    def queryset(self, request, queryset):
        if not (value := self.value()):
            return

        try:
            days = timedelta(days=int(value))
        except ValueError:
            return

        since = now() - days
        return queryset.filter(
            id__in=RequestFingerprint.objects.filter(created__gte=since).select_related('user_session').values_list('user_session__user_id', flat=True)
        )


@admin.register(UserFingerprint)
class UserFingerprintAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email',
        'sessions',
        'num_browser_fingerprints', 'browser_fingerprints',
        'num_request_fingerprints', 'request_fingerprints',
    )
    list_filter = (
        LastActivityListFilter,
        NumRequestFingerprintsFilter,
        NumBrowserFingerprintsFilter,
    )
    search_fields = 'username', 'email',
    paginator = LargePaginator
    show_full_result_count = False

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .prefetch_related(
                Prefetch('sessions', queryset=UserSession.objects.all().order_by('-created')),
                Prefetch('sessions__browserfingerprints', queryset=BrowserFingerprint.objects.order_by('visitor_id', '-created').distinct('visitor_id')),
                Prefetch('sessions__requestfingerprints', queryset=RequestFingerprint.objects.order_by('user_session', 'user_agent', '-created').distinct('user_session', 'user_agent')),
            )
            .annotate(
                num_browser_fingerprints=Count('sessions__browserfingerprints__visitor_id', distinct=True),
                num_request_fingerprints=Count('sessions__requestfingerprints__user_agent', distinct=True),
            )
        )

    @admin.display(description='#')
    def num_browser_fingerprints(self, instance):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:fingerprint_browserfingerprint_changelist') + f'?q={instance.email}',
            instance.num_browser_fingerprints
        )

    @admin.display(description='#')
    def num_request_fingerprints(self, instance):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:fingerprint_requestfingerprint_changelist') + f'?q={instance.email}',
            instance.num_request_fingerprints
        )

    @admin.display(description='last sessions')
    @html_objects_list('{} &nbsp;&nbsp; <a href="{}"><code>{}</code></a>')
    def sessions(self, instance) -> Iterator[tuple]:
        for session in instance.sessions.all():
            yield (
                session.created.date(),
                reverse('admin:fingerprint_usersession_changelist') + f'?id={instance.id}',
                session.get_value_display(),
            )

    @admin.display(description='last browsers')
    @html_objects_list('{} &nbsp;&nbsp; <a href="{}"><code>{}</code></a>')
    def browser_fingerprints(self, instance) -> Iterator[tuple]:
        for session in instance.sessions.all():
            for fingerprint in session.browserfingerprints.all():
                yield (
                    fingerprint.created.date(),
                    reverse('admin:fingerprint_browserfingerprint_changelist') + f'?id={fingerprint.id}',
                    fingerprint.get_value_display(),
                )

    @admin.display(description='last requests')
    @html_objects_list('{} &nbsp;&nbsp; <a href="{}"><code>{}</code></a>')
    def request_fingerprints(self, instance) -> Iterator[tuple]:
        for session in instance.sessions.all():
            for fingerprint in session.requestfingerprints.all():
                yield (
                    fingerprint.created.date(),
                    reverse('admin:fingerprint_requestfingerprint_changelist') + f'?id={fingerprint.id}',
                    fingerprint.get_value_display(),
                )
