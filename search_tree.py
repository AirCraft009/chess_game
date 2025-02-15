class Node():
    def __init__(self, evaluation, move: tuple[int, int]):
        self.evaluation = evaluation
        self.move = move
        self.data = (move, evaluation)
        self.children = []
    
    def add_child(self, node):
        self.children.append(node)

class Tree():
    def __init__(self, height, start_node):
        self.height = height
        self.start_node = start_node
    
    def add_node(self, node, child):
        node.add_child(child)
    
    def add_to_root(self, node):
        self.start_node.add_child(node)
    
    def find_child(self, node, move):
        for child in node.children:
            if child.move == move:
                return child

    
    def find_move(self, node, move):
        if len(node.children) == 0:
            return None
        for child in node.children:
            if child.move == move:
                return child
            next_node = self.find_move(child, move)
            if next_node != None:
                return next_node
        return None
    


if __name__ == "__main__":
    ssd = Tree(4, Node(10, 10, 0))

    for x in range(4):
        ssd.add_node(ssd.start_node, Node(10*x, x*4, 0))
        for y in range(4):
            print(y + x*4)
            ssd.add_node(ssd.start_node.children[x], Node(10*y, x*4 + y, y))

            
    print(ssd.find_move(ssd.start_node, 13).evaluation)
            
    