from scipy import spatial
import numpy as np

class Profile:
  def __init__(self, node_id):
    self.node_id = node_id
    self.values = []

  def cosine_simalarity(self, another_profile):
    if np.any(self.values) and np.any(another_profile.values):
      return (1 - spatial.distance.cosine(self.values, another_profile.values))
    else:
      return 0


class FinancialProfile(Profile):
  def __init__(self, financial_categories, financial_values, node_id):
    super().__init__(node_id)
      
    # Each position in the vector represents a financial category, if the value is not present then fill with 0.
    # The values in every position represents the same financial attribute for every FinancialProfile. 
    for key in sorted(financial_categories.keys()):
      if key in financial_values.keys():
        self.values.append(float(financial_values[key]))
      else:
        self.values.append(0.0)


class TravelProfile(Profile):
  def __init__(self, countries_all, countries_from, countries_to, node_id):
    super().__init__(node_id)
    self.values = [0] * (len(countries_all) * 2)
    
    for idx, a_country in enumerate(sorted(countries_all)):
      if a_country in countries_from.keys():
        self.values[idx] = countries_from[a_country]

      if a_country in countries_to.keys():
        self.values[(idx*2)+1] = countries_to[a_country]


if __name__ == '__main__':
  from .graph import GraphCsv
  template_graph = GraphCsv('../template_nodes.csv', '../template_links.csv')
  
  financial_profile = FinancialProfile(template_graph.all_financial_types(), template_graph.build_financial_dict(0), 0)
  financial_profile2 = FinancialProfile(template_graph.all_financial_types(), template_graph.build_financial_dict(65), 65)
  print(financial_profile.cosine_simalarity(financial_profile2))
  
  countries = template_graph.build_travel_dict(0)
  travel_profile = TravelProfile(template_graph.all_countries(), countries[
    'from'], countries['to'], 0)
  countries = template_graph.build_travel_dict(78)
  travel_profile2 = TravelProfile(template_graph.all_countries(), countries['from'], countries['to'], 78)
  print(travel_profile.cosine_simalarity(travel_profile2))
