def read_cities_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_handler:
        cities_list = file_handler.readlines()
    return cities_list


def create_cities_base(cities_list):
    cities_base = {}
    for city in cities_list:
        city = city.lower().strip()
        if cities_base.get(city[0]) is None:
            cities_base[city[0]] = [city]
        else:
            cities_base[city[0]].append(city)
    return cities_base
