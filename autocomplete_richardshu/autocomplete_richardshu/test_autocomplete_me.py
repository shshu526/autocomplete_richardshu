## Run the tests by running
## pytest -v test_autocomplete_me.py
## All test functions must start with test_.

import pytest

import autocomplete_me

from autocomplete_me import Trie




def test_slowComplete():
    assert autocomplete_me.slowComplete('Sc', 'Data/pokemon.txt', 3) == [('Scizor', 2194440), ('Scrafty', 174368), ('Sceptile', 67457)]


pokemon = autocomplete_me.build_trie('Data/pokemon.txt')
baby = autocomplete_me.build_trie('Data/baby-names.txt')
artists = autocomplete_me.build_trie('Data/artists.txt')
movies = autocomplete_me.build_trie('Data/movies.txt')
chinese = autocomplete_me.build_trie('Data/mandarin.txt')




def test_common():
	assert autocomplete_me.autoComplete('Porygon', pokemon, 2) == [('Porygon2', 156945), ('Porygon-Z', 83878)]
	assert autocomplete_me.autoComplete('Porygon', pokemon, 6) == [('Porygon2', 156945), ('Porygon-Z', 83878), ('Porygon', 533)]
	assert autocomplete_me.autoComplete('Chris', baby, 5) == [('Christopher', 11796), ('Christian', 9668), ('Christina', 1115), ('Chris', 654), ('Christine', 432)]
	assert autocomplete_me.autoComplete('Ch', movies, 3) == [('Charlie and the Chocolate Factory (2005)', 206459076), ('Chicago (2002)', 170687518), ('Cheaper by the Dozen (2003)', 138614544)]
	assert autocomplete_me.autoComplete('A', artists, 4) == [('Akon', 1000000), ('Argonout', 947328), ('Avril Lavigne', 941896), ('Alicia Keys', 933916)]


# def test_unicode():
# 	assert autocomplete_me.autoComplete('我'，chinese，2) == [('我的', 20865), ('我喜', 1495)]
# 	assert autocomplete_me.autoComplete('我'，chinese，6) == [('我的', 20865)， ('我喜', 1495), ('我自己', 811), ('我爸', 690), ('我家', 458), ('我等', 305)]



def test_same():
	assert autocomplete_me.autoComplete('Porygon', pokemon, 2) == autocomplete_me.slowComplete('Porygon', 'Data/pokemon.txt', 2)
	assert autocomplete_me.autoComplete('Sc', pokemon, 3) == autocomplete_me.slowComplete('Sc', 'Data/pokemon.txt', 3)
	assert autocomplete_me.autoComplete('Pika', pokemon, 1) == autocomplete_me.slowComplete('Pika', 'Data/pokemon.txt', 1)
	assert autocomplete_me.autoComplete('Abo', pokemon, 2) == autocomplete_me.slowComplete('Abo', 'Data/pokemon.txt', 2)
	
autocomplete_me.add(baby, 'Shiyu', 999)

def test_add():
	assert baby.search('Shiyu') != 0
	assert baby.search('Shiyu').weight == 999

autocomplete_me.delete(baby, 'Noah')#originally 17278
autocomplete_me.delete(baby, 'Malia')#originally 890

def test_delete():
	assert autocomplete_me.autoComplete('Noah', baby, 3) == [('Noahalexander', 6), ('Noahjames', 6), ('Noahgabriel', 5)]
	assert autocomplete_me.autoComplete('Malia', baby, 3) == [('Maliah', 273)]

def test_changeweight():
	autocomplete_me.change_weight(artists, 'Paramore', lambda x:x+1)#951488 originally
	assert artists.search('Paramore').weight == 951489


autocomplete_me.insert_or_update(pokemon, 'Skarmory', 999)
autocomplete_me.insert_or_update(pokemon, 'Richard', 999)

def test_insertupdate():
	assert pokemon.search('Skarmory').weight == 993019
	assert pokemon.search('Richard').weight == 999
	assert pokemon.search('Richard') != 0

pokemon2 = autocomplete_me.build_trie('Data/pokemon2.txt')

autocomplete_me.prune_trie(pokemon2, 153000)

def test_prune():
	assert pokemon2.search('Heracross') == 0
	assert pokemon2.search('Ditto') != 0
	assert pokemon2.search('Ditto').weight == 153550

pokemon3 = autocomplete_me.build_trie('Data/pokemon2.txt')

autocomplete_me.rescale_weights(pokemon3, lambda x:x/10)

def test_rescale_weights():
	assert pokemon3.search('Ditto').weight == 15355
	assert pokemon3.search('Scizor').weight == 219444

