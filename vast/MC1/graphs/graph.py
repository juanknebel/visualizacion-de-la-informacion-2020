import pymysql.cursors
import pandas as pd


class Graph:
  def __init__(self):
    self.financial_type = {
      459381: 'Water and other public services',
      466907: 'Electricity',
      473173: 'Household furnishings',
      503218: 'Natural gas',
      503701: 'Miscellaneous',
      510031: 'Gifts',
      520660: 'Healthcare',
      523927: 'Restaurants',
      527449: 'Alcohol',
      536346: 'Home maintenance',
      537281: 'Housekeeping supplies',
      552988: 'Money income before taxes',
      567195: 'Personal insurance and pensions',
      571970: 'Reading',
      575030: 'Transportation',
      577992: 'Education',
      580426: 'Telephone services',
      589943: 'Lodging away from home',
      595298: 'Groceries',
      595581: 'Donations',
      606730: 'Entertainment',
      616315: 'Apparel and services',
      620120: 'Personal taxes',
      621924: 'Mortgage payments',
      630626: 'Rented dwellings',
      632961: 'Personal care products and services',
      640784: 'Tobacco',
      642329: 'Household operations',
      644226: 'Property taxes'
    }
    self.edge_type = {
      0: 'Email', 
      1: 'Phone', 
      2: 'Sell', 
      3: 'Buy', 
      4: 'Authro-of', 
      5: 'Financial', 
      6: 'Travels-to'
      }
    self.node_type = {
      1: 'Person', 
      2: 'Product category', 
      3: 'Document', 
      4: 'Financial category', 
      5: 'Country'
      }
    self.countries_id = [0, 1, 2, 3, 4, 5]
    self.translate_countries = {}

  def translate_country(self, country):
    for k, v in self.translate_countries.items():
      if v == country:
        return k
    raise Exception('Country not found')

  def find_node_type(self, node_id):
    raise Exception('Not implemented')

  def find_by_params(
    self,
    source=None, 
    e_types=None, 
    target=None, 
    time=None, 
    weight=None, 
    source_location=None, 
    target_location=None):
    raise Exception('Not implemented')

  def node_type_description(self, type_id):
    return self.node_type[type_id]

  def edge_type_description(self, type_id):
    return self.edge_type[type_id]

  def financial_description(self, type_id):
    return self.financial_type[type_id]

  def all_financial_types(self):
    return self.financial_type

  def all_countries(self):
    return self.countries_id

  def find_countries_visit_by(self, a_node):
    countries = self.find_by_params(source=a_node, e_types=[6])\
      ['target'].unique()

    countries_translate = map(lambda x: self.translate_countries[x], countries)
    return list(countries_translate)

  def build_financial_dict(self, node_id):
    '''
    Take the relations between a node and their financial links, the noda could be source or target.
    Translate the union in a dictionaty with the id of the financial category like key and the weight as value.
    '''
    filter_data_source = self.find_by_params(source=node_id, e_types=[5])[['target', 'weight']].rename(columns={"target": "financial", "weight": "value"})
    filter_data_target = self.find_by_params(target=node_id, e_types=[5])[['source', 'weight']].rename(columns={"source": "financial", "weight": "value"})
    filter_data = pd.concat([filter_data_source, filter_data_target], axis=0)

    return dict(zip(filter_data.financial, filter_data.value))

  def build_travel_dict(self, node_id):
    filter_data_source = self.find_by_params(source=node_id, e_types=[6])
    if filter_data_source.empty:
      return {'from': {}, 'to': {}}

    filter_data_source = filter_data_source[
      ['target', 'source_location', 'target_location']].rename(
        columns={"source_location": "from", "target_location": "to"})

    from_location = filter_data_source.groupby('from')['to'].nunique().to_dict()
    to_location = filter_data_source.groupby('to')['from'].nunique().to_dict()

    return {'from': from_location, 'to': to_location}

  def list_nodes(self, types=None):
    raise Exception('Not implemented')


class GraphMysql(Graph):
  def __init__(self, connection_config):
    super().__init__()
    self.hostname = connection_config['hostname']
    self.db_user = connection_config['user']
    self.db_password = connection_config['password']
    self.db_schema = connection_config['schema']
    self.db_port = connection_config['port']
    self.connection = pymysql.connect(host=self.hostname, user=self.db_user, password=self.db_password, db=self.db_schema, charset='utf8mb4', port=self.db_port, cursorclass=pymysql.cursors.DictCursor)
    self.links = 'links'
    self.nodes = 'nodes'
    self.translate_countries = {
      616453: 5,
      499467: 2,
      509607: 4,
      561157: 0,
      625756: 3,
      657173: 1
      }
    structure = self.execute_sql_query(f"DESC {self.links}")
    self.empty_structure = [x['Field'] for x in structure]

  def execute_sql_query(self, sql):
    self.connection.ping(reconnect=True)
    try:
      with self.connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
      self.connection.close()
    return result

  def execute_sql_query_unique(self, sql):
    self.connection.ping(reconnect=True)
    try:
      with self.connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        if cursor.fetchone() != None:
          raise Exception('Error, must be a unique result')

    finally:
      self.connection.close()
    return result

  def find_node_type(self, node_id):
    sql = f'SELECT * FROM {self.nodes} where id = {node_id}'
    return self.execute_sql_query_unique(sql)['node_type']

  def find_by_params(
    self,
    source=None, 
    e_types=None, 
    target=None, 
    time=None, 
    weight=None, 
    source_location=None, 
    target_location=None):
    sql = f'SELECT * FROM {self.links}'
    conditions = []

    if source != None:
      conditions.append(f'source = {source}')
    if e_types != None and len(e_types) > 0:
      conditions.append(f'e_type in ({",".join(map(str, e_types))})')
    if target != None:
      conditions.append(f'target = {target}')
    if time != None:
      conditions.append(f'time = {time}')
    if weight != None:
      conditions.append(f'weight = {weight}')
    if source_location != None:
      conditions.append(f'source_location = {source_location}')
    if target_location != None:
      conditions.append(f'target_location = {target_location}')

    if len(conditions) > 0:
      sql += f' WHERE {" AND ".join(conditions)}'

    result = pd.DataFrame(self.execute_sql_query(f"{sql}"))
    if result.empty:
      result = pd.DataFrame(columns=self.empty_structure)

    return result


class GraphCsv(Graph):
  def __init__(self, nodes_file_name, links_file_name):
    super().__init__()
    self.nodes = pd.read_csv(nodes_file_name, sep=',')
    self.links = pd.read_csv(links_file_name, sep=',')
    self.translate_countries = {
      81: 1,
      70: 3,
      69: 4,
      76: 2,
      71: 0,
      72: 5
      }

  def find_node_type(self, node_id):
    return self.nodes[(self.nodes.id == node_id)].iloc[0]['node_type']

  def find_by_params(
    self,
    source=None, 
    e_types=None, 
    target=None, 
    time=None, 
    weight=None, 
    source_location=None, 
    target_location=None):
    partial_filter = pd.DataFrame(self.links)
    if source != None:
      partial_filter = partial_filter[(partial_filter.source == source)]
    if e_types != None:
      partial_filter = partial_filter[(partial_filter.e_type.isin(e_types))]
    if target != None:
      partial_filter = partial_filter[(partial_filter.target == target)]
    if time != None:
      partial_filter = partial_filter[(partial_filter.time == time)]
    if weight != None:
      partial_filter = partial_filter[(partial_filter.weight == weight)]
    if source_location != None:
      partial_filter = partial_filter[(partial_filter.source_location == source_location)]
    if target_location != None:
      partial_filter = partial_filter[(partial_filter.target_location == target_location)]

    return partial_filter

  def list_nodes(self, types=None):
    if type is None:
      return self.nodes['id'].values
    else:
      return self.nodes[self.nodes['node_type'].isin(types)]['id'].values


if __name__ == '__main__':
  template_graph = GraphCsv('../template_nodes.csv', '../template_links.csv')
  large_graph = GraphMysql({'hostname': 'localhost',
  'user': 'root',
  'password': 'root',
  'schema': 'vast',
  'port': 52000})

  print(template_graph.find_by_params(source=0, e_types=[4]))
  print(large_graph.find_by_params(source=600971, e_types=[4]))
  print(large_graph.build_financial_dict(1))
