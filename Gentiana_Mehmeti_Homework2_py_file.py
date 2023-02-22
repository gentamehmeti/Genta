from urllib.request import urlopen
from urllib.parse import quote

found_cities = []
found_cities_name = []
cities_by_steps = []

#turn values to key value pair
def add_colum_names(city_params):
    result = {}
    column_names = ["Name", "Country", "Province", "Longitude", "Latitude", "River", "Sea", "Lake"]
    if len(city_params) < len(column_names):
        empty_spaces_to_add = len(column_names) - len(city_params)
        for i in range(1, empty_spaces_to_add + 1):
            city_params.append("")

    for i in range(len(column_names)):
        result[column_names[i]] = city_params[i]

    return result

#create a variable, and write your queries
def get_params(city):
    q = "SELECT c.Name, c.Country, c.Province, c.Longitude, c.Latitude, l.River, l.Sea, l.Lake FROM City AS c LEFT JOIN located AS l ON c.Name = l.City WHERE c.Name = '%s' LIMIT 1 " % (city)
    eq = quote(q)
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql="+eq
    query_results = urlopen(url)

    # iterate over the result rows
    for line in query_results:
        string_line = line.decode('utf-8').rstrip()
        # if the query had a syntax error or if the result is empty
        # there is nevertheless one empty line, ignore it
        if len(string_line) > 0:
            # put the column values in columns
            columns = string_line.split("\t")
            with_column_names = add_colum_names(columns)

    return with_column_names

    query_results.close()

def getAllNeighbourCities(cities, d):

    to_return = []

    # Loop through all cities that are part of the array passed to find the neighbours of
    for city in cities:

        longitude = 0
        latitude = 0
        if len(city['Longitude']):
            longitude = float(city['Longitude'])
        if len(city['Latitude']):
            latitude = float(city['Latitude'])

        # Here, all the cities that are closer than the maxium distance <= 2 will be filtered (also, the current city being itarated will not be added to the return)
        q = "SELECT c.Name, c.Country, c.Province, c.Longitude, c.Latitude, l.River, l.Sea, l.Lake, (ABS(%s - c.Longitude) + ABS(%s - c.Latitude)) as Distance FROM City AS c LEFT JOIN located AS l ON c.Name = l.city WHERE c.Longitude IS NOT NULL AND c.Latitude IS NOT NULL AND c.Name <> '%s' HAVING Distance <= %s" % (longitude, latitude, city['Name'], d)
        eq = quote(q)
        url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq
        query_results = urlopen(url)

        # iterate over the result rows
        for line in query_results:
            string_line = line.decode('utf-8').rstrip()
            # if the query had a syntax error or if the result is empty
            # there is nevertheless one empty line, ignore it
            if len(string_line) > 0:
                # put the column values in columns
                columns = string_line.split("\t")
                if columns[0] not in found_cities_name:
                    found_cities_name.append(columns[0])
                    with_column_names = add_colum_names(columns)
                    to_return.append(with_column_names)
                    found_cities.append(with_column_names)

        query_results.close()

        q1 = "SELECT c.Name, c.Country, c.Province, c.Longitude, c.Latitude, l.River, l.Sea, l.Lake FROM City AS c LEFT JOIN located AS l ON c.Name = l.city WHERE ((l.River IS NOT NULL AND l.River = '%s') OR (l.Lake IS NOT NULL AND l.Lake='%s') OR (l.Province IS NOT NULL AND l.Province='%s')) AND c.Longitude IS NULL AND c.Latitude IS NULL AND c.Name <> '%s'" % (city['River'], city['Lake'], city['Province'], city['Name'])
        eq1 = quote(q1)
        url1 = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq1
        query_results1 = urlopen(url1)

        # iterate over the result rows
        for line in query_results1:
            string_line = line.decode('utf-8').rstrip()
            # if the query had a syntax error or if the result is empty
            # there is nevertheless one empty line, ignore it
            if len(string_line) > 0:
                # put the column values in columns
                columns = string_line.split("\t")
                if columns[0] not in found_cities_name:
                    found_cities_name.append(columns[0])
                    with_column_names = add_colum_names(columns)
                    to_return.append(with_column_names)
                    found_cities.append(with_column_names)

        query_results1.close()

    return to_return

def search(city, country, k, s, d):
    found_cities.append(get_params(city))
    found_cities_name.append(city)

    cities_to_loop = [get_params(city)]

    if len(cities_to_loop):
        current_step_cities = []

        # Iterating through a for loop with a maximum of steps given as part of the task
        for i in range(1, k + 1):

            if i == 1:
                current_step_cities = getAllNeighbourCities(cities_to_loop, d)
                cities_by_steps.append({
                    "Step": i,
                    "Cities": [city['Name'] for city in current_step_cities]
                })

            else:
                current_step_cities = getAllNeighbourCities(current_step_cities, d)
                cities_by_steps.append({
                    "Step": i,
                    "Cities": [city['Name'] for city in current_step_cities]
                })

    print(cities_by_steps)

search('Geneva', 'CH', 5, 4, 2)