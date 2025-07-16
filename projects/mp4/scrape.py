'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: vardaan kapoor, vkapoor5
'''
class GraphSearcher:
    def __init__(self):
        # tracks which nodes have been visited
        self.visited = set()
        # records the order in which nodes are first seen
        self.order = []

    def visit_and_get_children(self, node):
        """
        MUST be overridden in subclasses.
        Should append `node` to self.order and return an iterable
        of its children.
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, start_node):
        """
        Public entry point: clears state, kicks off the recursion,
        and returns the final visitation order.
        """
        # reset visited & order
        self.visited.clear()
        self.order.clear()

        # start the recursive DFS
        self.dfs_visit(start_node)

        # return the recorded order
        return self.order

    def dfs_visit(self, node):
        """
        Recursive DFS:
          1. If already seen, return immediately.
          2. Mark as seen.
          3. Ask subclass for children (and record node in order).
          4. Recurse on each child.
        """

        # 1) base case
        if node in self.visited:
            return

        # 2) mark visited
        self.visited.add(node)

        # 3) get children (subclass must record node in self.order here)
        children = self.visit_and_get_children(node)

        # 4) recurse
        for child in children:
            self.dfs_visit(child)

class MatrixSearcher(GraphSearcher):
    def __init__(self, df: pd.DataFrame):
        """
        df should be a square DataFrame whose index and columns
        are the same set of node labels, and entries are 0/1.
        """
        super().__init__()
        self.df = df

    def visit_and_get_children(self, node):
        """
        1) append the node to the visitation order
        2) look across df.loc[node] for entries == 1
           and return those column‐labels as children
        """
        # record the visitation
        self.order.append(node)

        # df.loc[node] is a Series of 0/1; .items() yields (col_label, value)
        children = [
            col
            for col, val in self.df.loc[node].items()
            if val == 1
        ]
        return children