import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class TimeAndIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Types(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('ТВ шоу')


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('актер')
    DIRECTOR = 'director', _('директор')
    WRITER = 'writer', _('сценарист')

class Genre(TimeAndIDMixin, models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        managed = False

    def save(self, *args, **kwargs):
        super(Genre, self).save(*args, **kwargs)
        Filmwork.take_indexed([item.film for item in self.genremedia_set.all()])

    def __str__(self):
        return self.name

class Filmwork(TimeAndIDMixin, models.Model):
    title = models.CharField(_('title'),max_length= 50, blank=True)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'),auto_now=False, auto_now_add=False)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('Путь к файлу'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                                validators=[MinValueValidator(0), 
                                            MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=20, choices=Types.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    # флаг индексации фильма, например для elasticsearch
    indexed = models.BooleanField(_("индексирован"), default=False)


    class Meta:
        verbose_name = _('Фильм')
        verbose_name_plural = _('Фильмы')
        db_table = '"content"."film_work"'
        managed = False

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.indexed = False
        super(Filmwork, self).save(*args, **kwargs)

    @staticmethod
    def take_indexed(medias):
        """" Снимает флаг индексации переданных фильмов """
        for media in medias:
            media.indexed = False
            media.save()


class GenreFilmwork(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, to_field='id', db_column='genre_id')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['filmwork_id', 'genre_id'], name='film_work_genre'),
        ]
        db_table = "content\".\"genre_film_work" 
        verbose_name = 'Жанр фильма'
        verbose_name_plural = 'Жанры фильма'
        managed = False

    def __str__(self):
        return str(f'{self.filmwork} - {self.genre}')



class Person(TimeAndIDMixin, models.Model):
    full_name = models.CharField(_('Фио'),max_length=50, blank=True)
    birth_date = models.DateField(_('День рождения'), null=True, blank=True)

    class Meta:
        db_table = "content\".\"person"
        managed = False
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        Filmwork.take_indexed([item.film for item in self.personmedia_set.all()])


class PersonFilmwork(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    filmwork = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE, to_field='id', db_column='film_work_id'
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, to_field='id', db_column='person_id'
    )
    role = models.CharField(
        _('role'),
        max_length=30,
        choices=RoleType.choices
    )
    created_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _('Персона её роль')
        verbose_name_plural = _('Персоны и их роли')
        db_table = '"content"."person_film_work"'
        indexes = [
            models.Index(fields=['filmwork_id', 'person_id', 'role'], name='film_work_person_role'),
        ]
        managed = False

    def __str__(self):
        return str(f'{self.filmwork} - {self.person}')