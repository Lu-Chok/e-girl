from vedis import Vedis
# db = Vedis(':mem:')  # Create an in-memory database. Alternatively you could supply a filename for an on-disk database.
db = Vedis('db')
# db['k1'] = 'v1'

def add_data(reference, data):
    cell = db.Set({'test' : 1})
    print(set(cell))
    # cell.update(reference, data)

add_data('test', {"test" : 1})