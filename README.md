# mongodb-project

# BUSQUEDAS INICIALES
# Busqueda {"offices.country_code": {$nin : ["USA"]}}
# {$and: [{"offices.country_code": {$nin : ["USA"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}
# LONDRES {$and: [{"offices.country_code": {$in : ["GBR"]}}, {"offices.city": {$in : ["London"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}
# AMSTERDAM {$and: [{"offices.country_code": {$in : ["NLD"]}}, {"offices.city": {$in : ["Amsterdam"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}
# {$and: [{"offices.country_code": {$in : ["NLD"]}}, {"offices.city": {$in : ["Amsterdam"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}, {founded_year: {$gte : 2009}}]}


# Me decido por Amsterdam
# {$and: [{"offices.city": {$in : ["Amsterdam"]}}, {deadpooled_year: null}]}

# {'$and': [{"offices.latitude": { '$nin': [null] }}, {"offices.longitude":{ '$nin': [null] }}, {"offices.city": "Amsterdam"}, {'deadpooled_year': null}]}

# Con el filtro de arriba consigo empresas con un raised_amount que pasa de 500.000 a 1.000.000 por lo que sea un millon de euros(1,11) o de libras(1,29), siempre va a ser más que un millón de dolares por el cambio de moneda, el problema lo tendría si hubiese cantidades entre 750.000 y 950.000

# {'$and': [{"offices.latitude": { '$nin': [null] }}, {"offices.longitude":{ '$nin': [null] }}, {"offices.city": "Amsterdam"}, {'deadpooled_year': null}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}





# Buscar escuelas o guarderias