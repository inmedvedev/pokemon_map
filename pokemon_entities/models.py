from django.db import models


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Имя', max_length=200)
    photo = models.ImageField(verbose_name='Фото', upload_to='images', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    title_en = models.CharField(verbose_name='Имя на английском', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Имя на японском', max_length=200, blank=True)
    previous_evolution = models.ForeignKey('self',
                                           verbose_name='Предыдущая эволюция',
                                           on_delete=models.PROTECT,
                                           related_name='next_evolutions',
                                           null=True,
                                           blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                verbose_name='Покемон',
                                on_delete=models.CASCADE,
                                related_name='pokemon_entities',
                                blank=False)
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появление', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезновение', null=True, blank=True)
    level = models.IntegerField(verbose_name='Уровень', default=0)
    health = models.IntegerField(verbose_name='Здоровье', default=0)
    strength = models.IntegerField(verbose_name='Атака', default=0)
    defence = models.IntegerField(verbose_name='Защита', default=0)
    stamina = models.IntegerField(verbose_name='Выносливость', default=0)
