import sqlalchemy as al
import datetime

# choose engine and location of the database
engine = al.create_engine('sqlite:///history.db', echo=True)
meta = al.MetaData()

connection = engine.connect()

# creates two tables
sorting = al.Table('sorting algs', meta,
                   al.Column('time', al.DateTime, primary_key=True,
                             default=datetime.datetime.now),
                   al.Column('algorithm', al.String),
                   al.Column('list size', al.Integer),
                   al.Column('swaps', al.String),
                   al.Column('comparisons', al.String))
path_finding = al.Table('path finding', meta,
                        al.Column('time', al.DateTime, primary_key=True,
                                  default=datetime.datetime.now),
                        al.Column('algorithm', al.String),
                        al.Column('maze size', al.Integer),
                        al.Column('cell scanned', al.Integer))
meta.create_all(engine)


# function to insert into the sorting table
def sort_entry(alg, list_size, swaps, comparison):
    connection.execute(sorting.insert(), [
        {'algorithm': alg, 'list size': list_size, 'swaps': swaps, 'comparisons': comparison},
    ])


# function to insert into the maze table
def maze_entry(alg, maze_size, cells):
    connection.execute(path_finding.insert(), [
        {'algorithm': alg, 'maze size': maze_size, 'cell scanned': cells},
    ])


# gets all entries from the sorting table
def get_sort():
    all_entries = sorting.select()
    result = connection.execute(all_entries)
    return result


# gets all entries from the maze table
def get_path():
    all_entries = path_finding.select()
    result = connection.execute(all_entries)
    return result


# deletes all entries in maze table
def clear_path():
    connection.execute(path_finding.delete())


# deletes all entries in sort table
def clear_sort():
    connection.execute(sorting.delete())


# select maze algorithm
def filter_maze(alg):
    result = connection.execute(path_finding.select(whereclause=(path_finding.c.algorithm == alg)))
    return result


# select sorting algorithm
def filter_sort(alg):
    result = connection.execute(sorting.select(whereclause=(sorting.c.algorithm == alg)))
    return result
