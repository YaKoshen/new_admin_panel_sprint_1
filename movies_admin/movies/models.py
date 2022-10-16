"""Описание моделей данных."""
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CharFieldMaxLength:
    """Стандартные размеры строк для полей."""

    BIG = 255
    MEDIUM = 124
    SMALL = 63
    MICRO = 7


class TimeStampedMixin(models.Model):
    """Mixin для создания полей created и modified."""

    created = models.DateTimeField(_('Сreated'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        """Абстакрный класс."""

        abstract = True


class UUIDMixin(models.Model):
    """Mixin для создания поля UUID."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Абстакрный класс."""

        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Модель Жанр кинопроизведений."""

    name = models.CharField(_('Name'), max_length=CharFieldMaxLength.BIG)
    description = models.TextField(_('Description'), null=True, blank=True)

    class Meta:
        """Описание настроек модели."""

        db_table = "content\".\"genre"
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Модель Кинопроизведение."""

    class AvalibleGenre(models.TextChoices):
        """Доступные жанры для Кинопроизведения."""

        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV show')

    title = models.CharField(_('Title'), max_length=CharFieldMaxLength.BIG)
    description = models.TextField(_('Description'), null=True, blank=True)
    creation_date = models.DateTimeField(
        _('Creation date'),
        null=True,
        blank=True,
    )
    rating = models.FloatField(
        _('Rating'),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.TextField(
        _('Type'),
        max_length=CharFieldMaxLength.SMALL,
        choices=AvalibleGenre.choices,
        null=True,
        blank=True,
    )
    file_path = models.FileField(
        _('File'),
        max_length=CharFieldMaxLength.MEDIUM,
        blank=True,
        null=True,
        upload_to='movies/',
    )

    class Meta:
        """Описание настроек модели."""

        db_table = "content\".\"filmwork"
        verbose_name = _('Кинопроизведение')
        verbose_name_plural = _('Кинопроизведения')


class GenreFilmwork(UUIDMixin):
    """Связь Жанр - Кинопроизведение."""

    filmwork = models.ForeignKey(
        Filmwork,
        verbose_name=_('Filmwork'),
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name=_('Genre'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(_('Сreated'), auto_now_add=True)

    class Meta:
        """Описание настроек модели."""

        db_table = "content\".\"genre_filmwork"
        verbose_name = _('Связь Жанр - Кинопроизведение')
        verbose_name_plural = _('Связи Жанр - Кинопроизведение')


class Person(UUIDMixin, TimeStampedMixin):
    """Модель Человек."""

    class Gender(models.TextChoices):
        """Гендр для модели Человек."""

        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')

    full_name = models.CharField(
        _('Full name'),
        max_length=CharFieldMaxLength.BIG,
    )
    gender = models.TextField(
        _('Gender'),
        max_length=CharFieldMaxLength.MICRO,
        choices=Gender.choices,
        blank=True,
        null=True,
    )

    class Meta:
        """Описание настроек модели."""

        db_table = "content\".\"person"
        verbose_name = _('Человек')
        verbose_name_plural = _('Люди')


class PersonFilmwork(UUIDMixin):
    """Связь Человек - Кинопроизведение."""

    filmwork = models.ForeignKey(
        Filmwork,
        verbose_name=_('Filmwork'),
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        Person,
        verbose_name=_('Person'),
        on_delete=models.CASCADE,
    )
    role = models.TextField(_('Role'), null=True, blank=True)
    created = models.DateTimeField(_('Сreated'), auto_now_add=True)

    class Meta:
        """Описание настроек модели."""

        db_table = "content\".\"person_filmwork"
        verbose_name = _('Связь Человек - Кинопроизведение')
        verbose_name_plural = _('Связи Человек - Кинопроизведение')
