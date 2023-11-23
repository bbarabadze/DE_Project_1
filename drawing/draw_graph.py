import platform
from io import BytesIO
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

if platform.system() == 'Windows':
    matplotlib.use('TkAgg')

FRIENDS_FILE = "./social_network/friends_table.csv"

# Creates an empty graph
G = nx.Graph()

# Creates a dataframe from friends file
friendship_df = pd.read_csv(FRIENDS_FILE)

# Fills the graph with the friendship couples from the dataframe
for _, fr1, fr2 in friendship_df.itertuples():
    G.add_node(fr1)
    G.add_node(fr2)
    G.add_edge(fr1, fr2)


def create_graph(user_id: int) -> BytesIO | None:
    """
    This function draws a graph which contains friends of the 
    given user and friendships between them
    """

    if user_id not in G.nodes:
        return None

    # Creates a subgraph around the given user
    subgraph = nx.ego_graph(G, user_id, radius=1)

    # Plots the graph
    nx.draw(subgraph, with_labels=True, node_color='orange', font_weight='bold', node_size=500)

    # converts the plot into an image stream object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    return image_stream



