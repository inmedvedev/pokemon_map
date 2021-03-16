import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # tooltip=name,  # disable tooltip because of folium encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        img_url = get_img_url(pokemon_entity.pokemon)
        img_absolute_uri = request.build_absolute_uri(location=img_url)
        add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon, img_absolute_uri)
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_img_url(pokemon),
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    img_url = get_img_url(pokemon)
    pokemon_data = {
        'title_ru': pokemon.title,
        'img_url': img_url,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
     }
    if pokemon.previous_evolution:
        pokemon_data['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': get_img_url(pokemon.previous_evolution)
        }
    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        pokemon_data['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': get_img_url(next_evolution)
        }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.pokemon_entities.all():
        img_absolute_uri = request.build_absolute_uri(location=img_url)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_absolute_uri
        )
    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_data})


def get_img_url(self):
    return self.photo.url if self.photo else DEFAULT_IMAGE_URL
