"""Описание моделей админ-панели."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from movies.models import (Filmwork, Genre, GenreFilmwork, Person,
                           PersonFilmwork)


class StartRatingListFilter(admin.SimpleListFilter):
    """Фильтр по рейтингу количества звёзд из 5."""

    title = _('Рейтинг')
    parameter_name = 'Star rating'

    def lookups(self, request, model_admin):
        """Кнопки для фильтра на админ-панеле.

        Args:
            request: Стандратное поле для lookups.
            model_admin: Стандратное поле для lookups.

        Returns:
            Набор кнопок.
        """
        return (
            ('1', '⭐'),
            ('2', '⭐⭐'),
            ('3', '⭐⭐⭐'),
            ('4', '⭐⭐⭐⭐'),
            ('5', '⭐⭐⭐⭐⭐'),
        )

    def queryset(self, request, queryset):
        """Условия фильтрации по количеству ⭐.

        Рейтинг в звёздах зависимост от числового рейтинга,
        где case - количество звёзд, а в queryset.filter
        указываются границы числового рейтинга.

        Args:
            request: Стандратное поле для queryset.
            queryset: Стандратное поле для queryset.

        Returns:
            queryset в зависимости от числового рейтига.
        """
        ranges = {
            '1': (0,  20),
            '2': (20, 40),
            '3': (40, 60),
            '4': (60, 80),
            '5': (80, 100),
        }

        stars = self.value()
        if stars == '1':
            return queryset.filter(
                rating__gte=ranges[stars][0],
                rating__lte=ranges[stars][1],
            )
        elif stars in ('2', '3', '4', '5'):
            return queryset.filter(
                rating__gt=ranges[stars][0],
                rating__lte=ranges[stars][1],
            )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс для отображения Genre в меню админ-панели."""

    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class GenreFilmworkInline(admin.TabularInline):
    """Класс для отображения GenreFilmwork в формате TabularInline."""

    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    """Класс для отображения PersonFilmwork в формате TabularInline."""

    model = PersonFilmwork
    raw_id_fields = ('filmwork', 'person')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Класс для отображения Filmwork в меню админ-панели."""

    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'created',
        'modified',
    )

    list_filter = ('type', StartRatingListFilter, 'creation_date')
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Класс для отображения Person в меню админ-панели."""

    list_display = ('full_name', 'gender')
    search_fields = ('full_name', 'gender')
