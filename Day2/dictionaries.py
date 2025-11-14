
# Dictionaries
dictionary = {"cat":"chat", "dog":"chien"}
print(dictionary['cat'])

for english, french in dictionary.items():
    print(english, "->", french)

dictionary['cat'] = 'chatte'
dictionary['swan'] = 'cygne'
dictionary.update({'swan' :'cygne'})