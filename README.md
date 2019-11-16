# mongodb-project

# Busqueda {"offices.country_code": {$nin : ["USA"]}}
# {$and: [{"offices.country_code": {$nin : ["USA"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}
# LONDRES {$and: [{"offices.country_code": {$in : ["GBR"]}}, {"offices.city": {$in : ["London"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}
# AMSTERDAM {$and: [{"offices.country_code": {$in : ["NLD"]}}, {"offices.city": {$in : ["Amsterdam"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}]}
# {$and: [{"offices.country_code": {$in : ["NLD"]}}, {"offices.city": {$in : ["Amsterdam"]}}, {"funding_rounds.raised_amount": {$gte: 1000000}}, {founded_year: {$gte : 2009}}]}


# {$and: [{"offices.city": {$in : ["Amsterdam"]}}, {deadpooled_year: null}]}
# {'$and': [{"offices.latitude": { '$nin': [null] }}, {"offices.longitude":{ '$nin': [null] }}, {"offices.city": "Amsterdam"}, {'deadpooled_year': null}]}

# Buscar escuelas o guarderias