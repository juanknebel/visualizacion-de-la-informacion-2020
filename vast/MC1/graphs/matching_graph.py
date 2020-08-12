from .profile import TravelProfile, FinancialProfile


class MatchingGraph:
  def __init__(self, graph, template_graph):
    self.graph = graph
    self.template_graph = template_graph
    self.only_travel = False

  @staticmethod
  def filter_used_nodes(df_links, used_nodes, side):
    if df_links.empty:
      print(f'Empty links')
      return []

    df_neighbors = df_links[~df_links[side].isin(used_nodes)]
    neighbors = df_neighbors[side].unique()

    return neighbors

  def calculate_similar_nodes(self, nodes, template_nodes):
    print(f'calculate_similar_nodes')
    if len(template_nodes) == 0:
      return {}

    matching_node = {}
    # This map has all the financial and travel profiles of the large graph
    profiles_by_node = {}
    used_nodes = []
    for a_node in nodes:
      financial = FinancialProfile(self.graph.all_financial_types(),
                                   self.graph.build_financial_dict(a_node),
                                   a_node)

      a_travel_profile = self.graph.build_travel_dict(a_node)
      travel = TravelProfile(self.graph.all_countries(),
                             a_travel_profile['from'],
                             a_travel_profile['to'], a_node)

      profiles_by_node[a_node] = (financial, travel)

    for a_node in template_nodes:
      financial_profile = FinancialProfile(
          self.template_graph.all_financial_types(),
          self.template_graph.build_financial_dict(a_node),
          a_node)

      a_travel_profile = self.template_graph.build_travel_dict(a_node)
      travel = TravelProfile(self.template_graph.all_countries(),
                             a_travel_profile['from'],
                             a_travel_profile['to'], a_node)
      sim = -1
      like = -1
      for other_node, profile in profiles_by_node.items():
        if other_node in used_nodes:
          continue
        actual_sim = financial_profile.cosine_simalarity(profile[0]) + \
                     travel.cosine_simalarity(profile[1])
        if actual_sim > sim:
          sim = actual_sim
          like = other_node
      matching_node[a_node] = (like, sim)
      used_nodes.append(like)

    return matching_node

  def find_similar(self, node, template_node, used_nodes, template_used_nodes):
    print(f'Calculando similares de (original) {node} y (template)'
          f' {template_node}')

    node_neighbors = self.filter_used_nodes(
        self.graph.find_by_params(
            source=node, e_types=[0, 1]), used_nodes, 'target')

    template_node_neighbors = self.filter_used_nodes(
        self.template_graph.find_by_params(
            source=template_node, e_types=[0, 1]), template_used_nodes,
        'target')

    source_matching = self.calculate_similar_nodes(
        node_neighbors, template_node_neighbors)
    print(f'Similares como source: {source_matching}')

    node_neighbors = self.filter_used_nodes(
        self.graph.find_by_params(target=node, e_types=[0, 1]), used_nodes,
        'source')

    template_node_neighbors = self.filter_used_nodes(
        self.template_graph.find_by_params(target=template_node, e_types=[0, 1]),
        template_used_nodes, 'source')

    target_matching = self.calculate_similar_nodes(node_neighbors,
                                                     template_node_neighbors)
    print(f'Similares como target: {target_matching}')

    # Common nodes between the neighbors
    common_nodes = set(source_matching.keys()) & set(target_matching.keys())

    similar = {}
    # Only keep the the node with the most cosine similarity
    for a_common in common_nodes:
      if source_matching[a_common][1] > target_matching[a_common][1]:
        similar[a_common] = source_matching[a_common][0]
      else:
        similar[a_common] = target_matching[a_common][0]

      # Remove the common node
      source_matching.pop(a_common)
      target_matching.pop(a_common)

    for k, v in source_matching.items():
      similar[k] = v[0]

    for k, v in target_matching.items():
      similar[k] = v[0]

    return similar

  def walk_graph(self, from_node, template_from_node, hub_nodes):
    to_visit = [template_from_node]
    match = {template_from_node: from_node}

    if not self.only_travel:
      print(f"Finding similarity in communications")
      while len(to_visit) > 0:
        template_node = to_visit.pop()
        node = match[template_node]
        matching = self.find_similar(node, template_node, match.values(),
                                     match.keys())
        for k, v in matching.items():
          match[k] = v
          to_visit.append(k)
    else:
      match[39] = 655491
      match[40] = 595737
      match[41] = 473963

    print(f"Finding similarity in travels")
    for template_hub_node in hub_nodes:
      match_hub_node = match[template_hub_node]
      print(f"Hub {{{template_hub_node}: {match_hub_node}}} ...")
      if match_hub_node == -1:
        continue
      template_visit_countries = \
        set(self.template_graph.find_countries_visit_by(template_hub_node))
      visit_countries = \
        set(self.graph.find_countries_visit_by(match_hub_node))

      common_countries = template_visit_countries & visit_countries

      for a_country in common_countries:
        translate_country = self.template_graph.translate_country(a_country)
        template_visitors = self.filter_used_nodes(
            self.template_graph.find_by_params(
                target=translate_country, e_types=[6]), match.keys(), 'source')

        translate_country = self.graph.translate_country(a_country)
        visitors = self.filter_used_nodes(self.graph.find_by_params(
            target=translate_country, e_types=[6]), match.values(), 'source')

        matching = self.calculate_similar_nodes(visitors, template_visitors)
        print(f'Similares: {matching}')

        for k, v in matching.items():
          match[k] = v[0]

    return match


if __name__ == '__main__':
  from time import time
  from .graph import GraphCsv, GraphMysql

  template_graph = GraphCsv('./template_nodes.csv', './template_links.csv')
  large_graph = GraphMysql({
    'hostname': 'localhost',
    'user': 'root',
    'password': 'root',
    'schema': 'vast',
    'port': 52000
    })

  matching_graph = MatchingGraph(large_graph, template_graph)

  t0 = time()
  mirror_nodes = matching_graph.walk_graph(600971, 0, [39, 40, 41])
  print(mirror_nodes)
  print(time() - t0)
