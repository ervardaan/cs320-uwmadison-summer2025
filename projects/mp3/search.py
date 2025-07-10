class Node():
    def __init__(self,key):
        self.key=key
        self.values=[]
        self.left=None
        self.right=None
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size +=len(self.left)
        if self.right!=None:
            size+=len(self.right)
        return size
    
    def lookup(self,key):
        if(key==self.key):
            return self.values
        elif(key<self.key):
            if(self.left!=None):
                return self.left.lookup(key)
            else:
                return []
        else:
            if(self.right!=None):
                return self.right.lookup(key)
            else:
                return []
                
class BST():
    def __init__(self):
        self.root=None
    def add(self,key,val):
        if self.root==None:
            self.root=Node(key)
        cur=self.root
        while True:
            if key<cur.key:
                if cur.left==None:
                    cur.left=Node(key)
                else:
                    cur=cur.left
            elif key>cur.key:
                if cur.right==None:
                    cur.right=Node(key)
                else:
                    cur=cur.right
            else:
                assert cur.key == key
                break
        cur.values.append(val)
    
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.right)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.left)             # 3

    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, key):
        if self.root is None:
            return []
        return self.root.lookup(key)
    
    def height(self,node):
        if node is None:
            return -1
        return 1+max(self.height(node.left),self.height(node.right))
    
    def countLeafNodes(self):
        """
        Count the number of leaf nodes in the entire tree.
        A leaf is a node with no left and no right child.
        """

        def _count(node):
            # 1) Empty subtree has 0 leaves
            if node is None:
                return 0
            # 2) If this node is a leaf, count 1
            if node.left is None and node.right is None:
                return 1
            # 3) Otherwise sum leaves in the two subtrees
            return _count(node.left) + _count(node.right)

        # Kick off recursion from the real root
        return _count(self.root)
    
    def top_n(self, n):
        result = []

        def _reverse_inorder(node):
            if node is None or len(result) >= n:
                return
            _reverse_inorder(node.right)
            if len(result) < n:
                result.append(node.key)
            _reverse_inorder(node.left)

        _reverse_inorder(self.root)
        return result
                
    



        
   


                
        
        