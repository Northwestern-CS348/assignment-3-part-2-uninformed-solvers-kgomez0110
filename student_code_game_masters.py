from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def convertDiskorPeg(self, disk):
        return int(disk[-1])

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1)'))
        peg2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2)'))
        peg3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3)'))

        peg1_list = []
        peg2_list = []
        peg3_list = []

        if peg1:
            for binding in peg1:
                peg1_list.append(self.convertDiskorPeg(binding["?disk"]))
            peg1_list.sort()
        if peg2:
            for binding in peg2:
                peg2_list.append(self.convertDiskorPeg(binding["?disk"]))
            peg2_list.sort()
        if peg3:
            for binding in peg3:
                peg3_list.append(self.convertDiskorPeg(binding["?disk"]))
            peg3_list.sort()

        return (tuple(peg1_list), tuple(peg2_list), tuple(peg3_list))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        disk = movable_statement.terms[0].term.element
        initial_peg = movable_statement.terms[1].term.element
        dest_peg = movable_statement.terms[2].term.element

        disk_num = int(disk[-1]) - 1
        initial_peg_num = int(initial_peg[-1]) - 1
        dest_peg_num = int(dest_peg[-1]) - 1

        peg_tuple = self.getGameState()

        ## on 
        old_on = parse_input('fact: (on ' + disk + ' ' + initial_peg + ')')
        self.kb.kb_retract(old_on)
        new_on = parse_input('fact: (on ' + disk + ' ' + dest_peg + ')')
        self.kb.kb_assert(new_on)

        ## destination peg
        old_empty = parse_input('fact: (empty ' + dest_peg + ')')
        self.kb.kb_retract(old_empty)
        old_top_bindings = self.kb.kb_ask(parse_input('fact: (top ?disk ' + dest_peg + ')'))
        if old_top_bindings:
            old_top = old_top_bindings[0]['?disk']
            old_top_fact = parse_input('fact: (top ' + old_top + ' ' + dest_peg + ')')
            self.kb.kb_retract(old_top_fact)
        
        new_top = parse_input('fact: (top ' + disk + ' ' + dest_peg + ')')
        self.kb.kb_assert(new_top)

        ## initial peg
        old_top = parse_input('fact: (top ' + disk + ' ' + initial_peg + ')')
        self.kb.kb_retract(old_top)
        if (len(peg_tuple[initial_peg_num]) == 1):
            init_empty = parse_input('fact: (empty ' + initial_peg + ')')
            self.kb.kb_assert(init_empty)
        else:
            new_top_disk = "disk" + str(peg_tuple[initial_peg_num][1])
            new_top_disk_fact = parse_input('fact: (top ' + new_top_disk + ' ' + initial_peg + ')')
            self.kb.kb_assert(new_top_disk_fact)
    

        return 

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = self.kb.kb_ask(parse_input('fact: (position ?tile ?x pos1'))
        row2 = self.kb.kb_ask(parse_input('fact: (position ?tile ?x pos2'))
        row3 = self.kb.kb_ask(parse_input('fact: (position ?tile ?x pos3'))

        row1_dict = {}
        row2_dict = {}
        row3_dict = {}

        for binding in row1:
            if binding['?tile'] == 'empty':
                row1_dict[binding['?x']] = -1
            else :
                row1_dict[binding['?x']] = int(binding['?tile'][-1])
        
        for binding in row2:
            if binding['?tile'] == 'empty':
                row2_dict[binding['?x']] = -1
            else :
                row2_dict[binding['?x']] = int(binding['?tile'][-1])

        for binding in row3:
            if binding['?tile'] == 'empty':
                row3_dict[binding['?x']] = -1
            else :
                row3_dict[binding['?x']] = int(binding['?tile'][-1])
        
        row1_list = [row1_dict['pos1'], row1_dict['pos2'], row1_dict['pos3']]
        row2_list = [row2_dict['pos1'], row2_dict['pos2'], row2_dict['pos3']]
        row3_list = [row3_dict['pos1'], row3_dict['pos2'], row3_dict['pos3']]
        return (tuple(row1_list), tuple(row2_list), tuple(row3_list))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        # (movable ?tile ?x1 ?y1 ?x2 ?y2)
        tile = movable_statement.terms[0].term.element
        x1 = movable_statement.terms[1].term.element
        y1 = movable_statement.terms[2].term.element
        x2 = movable_statement.terms[3].term.element
        y2 = movable_statement.terms[4].term.element
        
        old_pos = parse_input('fact: (position ' + tile + ' ' + x1 + ' ' + y1 + ')')
        old_empty = parse_input('fact: (position empty ' + x2 + ' ' + y2 + ')')
        new_pos = parse_input('fact: (position ' + tile + ' ' + x2 + ' ' + y2 + ')')
        new_empty = parse_input('fact: (position empty ' + x1 + ' ' + y1 + ')')
        self.kb.kb_retract(old_pos)
        self.kb.kb_retract(old_empty)
        self.kb.kb_assert(new_pos)
        self.kb.kb_assert(new_empty)
        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
