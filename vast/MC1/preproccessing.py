import csv
import json


directory = './data/'
extension_in = '.csv'
extension_out = '.json'

def numerify_rows(a_row):
    """Try to parse the float and integer items in the row. If any value in the row cannot be parse then assigns the same vale. Cannot be None.

    Args:
        a_row (dict): A row to parse.

    Returns:
        (dict): the row with all the items parse when it is possible.
    """
    for k, v in list(a_row.items()):
        try:
            a_row[k] = float(v)
            a_row[k] = int(v)
        except ValueError:
            pass
    return a_row



def convert_to_json(list_of_file_names):
    """Convert all the csv files in the list to json file and save them in a file with the same name but with json extension. Assumes the that the files sent to the method are a csv with comma separator.
    
    Args:
        list_of_files_names [string]: the list of the files to convert to strings. Cannot be None.
    """
    for file_name in list_of_file_names:
        file_in = open(directory + file_name + extension_in, newline='\n')
        
        reader = csv.DictReader(file_in, delimiter=',')
        
        rows = []
        for a_row in reader:
            rows.append(numerify_rows(a_row))

        file_out = open(directory + file_name + extension_out, 'w')
        json.dump(list(rows), file_out, ensure_ascii=False, indent=2)


def create_graph(node_file, links_file, nodes_type_description, edges_type_description, file_name_out):
    """Creates a json file to use it as a graph for D3.

    Args:
        node_file (string): This file contains the values of the nodes. Cannot be None.
        
        links_file (string): This file contains the links between the nodes. Cannot be None.
        
        nodes_type_description (string): This file contains the node's type description. Cannot be None.
        
        edges_types_description (string): This file contains the edge's type description. Cannt be None.
        
        file_name_out (string): This the name of the file to write the new graph. Cannot be None.
    """
    nodes = json.load(open(directory + node_file))
    links = json.load(open(directory + links_file))
    nodes_type = json.load(open(directory + nodes_type_description))
    edges_type = json.load(open(directory + edges_type_description))

    set_of_nodes = set()
    for a_link in links:
        set_of_nodes.add(a_link['Source'])
        set_of_nodes.add(a_link['Target'])

    new_nodes = []
    nodes_in_links = set()
    for a_node in nodes:
        if a_node['NodeID'] in set_of_nodes:
            new_nodes.append(a_node)
            nodes_in_links.add(a_node['NodeID'])

    missing_nodes_ids = set_of_nodes.difference(nodes_in_links)
    for a_missing_node_id in missing_nodes_ids:
        new_missing_node = {'NodeID': a_missing_node_id, 'NodeType': 99}
        new_nodes.append(new_missing_node)

    for a_node in new_nodes:
        for a_type in nodes_type:
            if a_type['NodeType'] == a_node['NodeType']:
                description = a_type['Description']
        a_node['NodeTypeDescription'] = description
        a_node['id'] = a_node['NodeID']

    for a_link in links:
        for a_type in edges_type:
            if a_type['EdgeType'] == a_link['eType']:
                description = a_type['Description']
        a_link['eType'] = description
        a_link['source'] = a_link['Source']
        a_link['target'] = a_link['Target']

    graph = {}
    graph['nodes'] = new_nodes
    graph['links'] = links

    file_out = open(directory + file_name_out, 'w')
    json.dump(graph, file_out, ensure_ascii=False, indent=2)


file_names = ['CGCS-GraphData-NodeTypes', 'CGCS-Template-NodeTypes', 'DemographicCategories', 'NodeTypeDescriptions', 'CGCS-Template', 'Q1-Graph1', 'Q1-Graph2', 'Q1-Graph3', 'Q1-Graph4', 'Q1-Graph5', 'Q2-Seed1', 'Q2-Seed2', 'Q2-Seed3']

#convert_to_json(file_names)

# For Template graph
create_graph('CGCS-Template-NodeTypes.json', 'CGCS-Template.json', 'NodeTypeDescriptions.json', 'EdgeTypesDescription.json', 'graph-template.json')

create_graph('CGCS-GraphData-NodeTypes.json', 'Q1-Graph1.json', 'NodeTypeDescriptions.json', 'EdgeTypesDescription.json', 'graph-q1.json')

create_graph('CGCS-GraphData-NodeTypes.json', 'Q1-Graph2.json', 'NodeTypeDescriptions.json', 'EdgeTypesDescription.json', 'graph-q2.json')

create_graph('CGCS-GraphData-NodeTypes.json', 'Q1-Graph3.json', 'NodeTypeDescriptions.json', 'EdgeTypesDescription.json', 'graph-q3.json')

create_graph('CGCS-GraphData-NodeTypes.json', 'Q1-Graph4.json', 'NodeTypeDescriptions.json', 'EdgeTypesDescription.json', 'graph-q4.json')

create_graph('CGCS-GraphData-NodeTypes.json', 'Q1-Graph5.json', 'NodeTypeDescriptions.json', 'EdgeTypesDescription.json', 'graph-q5.json')