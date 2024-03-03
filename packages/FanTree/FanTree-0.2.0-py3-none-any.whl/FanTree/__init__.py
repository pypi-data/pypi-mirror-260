__version__ = "0.2.0"
__author__ = 'ShiYuan Fan'

import random

def random_with_probability(probability):
    """Input a probability(0~1) and output random result(True or False) with probability. We are accurate to 4 decimal places."""
    # Probability is at the range of 0 to 1
    probability = round(probability*10000) # 0.90335 --> 9034
    whole = 10000 # 100 * 100
    random_number = random.randint(1,whole)
    if random_number < probability:
        return True
    else:
        return False

class Tree: # This the 'trunk'(base) of all Branches
    """Create a decision tree"""
    def __init__(self, name:str):
        self.name = name # A Tree MUST has a name
        self.father = None  # Tree(Trunk) has no father
        '''
        Explanation for Tree.children:
        Tree.children is a list that contains objects(branches) that have Tree as DIRECT father.
        Please notice "DIRECT", not the grandfather or grandgrandfather...
        '''
        self.open = True  # Tree(Trunk) is always open
        self.branches = []
        self.children = self.find_children()
        print(self.children)

    def add_branch(self, father, condition:tuple, name:str=''):
        """Create a decision branch"""
        new_branch = Branch(father=father, condition=condition, name=name)
        self.branches.append(new_branch)
        return new_branch # Return a object
    
    def add_random_branch(self, father, probability=1, name:str=""):
        """Create a random branch(decision branch without certain condition)"""
        new_branch = Random_Branch(father=father, probability=probability, name=name)
        self.branches.append(new_branch)
        return new_branch

    def find_children(self):
        """Find direct children of a father."""
        children = []
        for branch in self.branches:
            if branch.father == self:
                children.append(branch)
        return children

    def simulate(self, show_branches=False):
        """Simulate the decision tree"""
        def simulate_layer(fathers:list):
            activated_children = []
            for father in fathers:
                for child in father.find_children():
                    child.run()
                    if child.open == True:
                        activated_children.append(child)
            return activated_children

        def check_if_end(father):
            if len(father.find_children()) == 0:
                return True # Branch has no children means the fork ends here
            else:
                return False

        activated = [self]
        while True:
            activated = simulate_layer(activated)
            for child in activated:
                if child == None or check_if_end(child) == True:
                    activated.remove(child)
            if len(activated) == 0: 
                break

        print()
        print(f"Simulation for {self.name}:\n")
        
        if show_branches == True:
            for branch in self.branches:
                if branch.open == False:
                    print(f"{branch.name} : X")
                if branch.open == True:
                    print(f"{branch.name} : √")

        print("\nSimulation complete")

        # All set to default
        for branch in self.branches:
            branch.open = False

class Child_Of_Tree(): # Both Branches are the children of the tree
    def __init__(self):
        pass
    
    def find_trunk(self): 
        father = self.father
        while True: # Father's father's father.... is always the Trunk(Tree)
            if father.father == None:
                return father
            father = father.father

    def find_children(self):
        trunk = self.find_trunk()
        children = []
        for branch in trunk.branches:
            if branch.father == self:
                children.append(branch)
        return children

class Branch(Child_Of_Tree): # !: User should not be allowed to use this class, only create branch by Tree.add_branch
    def __init__(self, father, condition:tuple, command=None, name:str=''):
        if father.__class__ != Branch and father.__class__ != Tree and father.__class__ != Random_Branch:
            raise TypeError("Incorrect 'father' augument for Branch. It should be Tree or Branch.")
        self.father = father  # Branch or Tree
        self.trunk = self.find_trunk()
        self.open = False  # Branch is open or close. False for close, True for open.
        self.probability = 1  # An ordinary branch has probability 1

        if not callable(command) and command != None:
            raise TypeError("Argument 'command' for Branch must be a callable function.")
        self.command = command
        
        # Give default name to the branch if user doesn't set
        if name == '':
            self.name = f"Branch {len(self.trunk.branches)}"
        else:
            self.name = name

        self.condition = condition

        self.detect_target = self.condition[0]
        self.operator = self.condition[1]
        self.expected_value = self.condition[2]
        number_types = [int, float, complex, list, tuple, bool]
        
        # Because of different inputs types, so we need different ways to process them.
        # Divide inputs to two types: number(bool) or string
        # Seems a little bit ugly
        if type(self.detect_target) in number_types:
            if type(self.expected_value) in number_types:
                self.condition_statement = f"{self.detect_target} {self.operator} {self.expected_value}"
            else:
                self.condition_statement = f"{self.detect_target} {self.operator} '{self.expected_value}'"
        else:
            if type(self.expected_value) in number_types:
                self.condition_statement = f"'{self.detect_target}' {self.operator} {self.expected_value}"
            else:
                self.condition_statement = f"'{self.detect_target}' {self.operator} '{self.expected_value}'"
    
        try:
            eval(self.condition_statement)
        except SyntaxError:
            raise ValueError("Incorrect condition statement for Branch.")

    def run(self): # User should not to be able to use this function
        if eval(self.condition_statement):
            #if self.father.open == True:
            self.open = True
            self.command()

# Random Branch means a branch that has a uncertain condition. For example, the random branch has 50% probability to open.
class Random_Branch(Child_Of_Tree):
    def __init__(self, father, name:str="", command=None, probability=1):
        if father.__class__ != Branch and father.__class__ != Tree and father.__class__ != Random_Branch:
            raise TypeError("Incorrect 'father' augument for Branch. It should be Tree or Branch.")
        if type(probability) != int and type(probability) != float:
            raise TypeError("Wrong argument type for probability of Random Branch, must be float or int")
        if probability < 0 or probability > 1:
            raise ValueError("Random Branch must have a probability in range of 0 to 1")
        if not callable(command) and command != None:
            raise TypeError("Argument 'command' for Random Branch must be a callable function.")
        self.command = command
        self.father = father
        self.trunk = self.find_trunk()
        self.probability = probability
        self.open = False
        if name == "":
            self.name = f"Random Branch {len(self.trunk.branches)}"
        else:
            self.name = name

    def run(self):
        if random_with_probability(self.probability) == True and self.father.open == True:
            self.open = True
            if self.command != None:
                self.command()