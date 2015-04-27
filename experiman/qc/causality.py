def pca(g):
    """Implements the PCA algorithm.
    :param g: The graph whose causal subset we wish to deduce.
    :return: A causal graph, conditioned on the data.
    """
    # Remove links between independent variables.
    for x in g.nodes:
        for y in g.nodes:
            if not x == y:
                independence_test(x, y)

def independence_test(x, y):
    pass