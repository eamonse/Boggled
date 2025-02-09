from typing import List, Tuple, Set

class TrieNode:
    def __init__(self, letter=None) -> None:
        self.letter = letter
        # add attributes for whether it is the end of a word and a collection of pointers to
        # next letters
        self.letter_dict = {}
        self.end_of_word = True
        self.start_of_word = False

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        #initialze the start of the Trie with an empty node like the BSTs

    def generate_tree_from_file(self)->None:
        words = self._load_words()
        #add code here to set up the TrieNode tree structure for the words

        #go through the words, and for each word break it apart into separate letters for each node
        for word in words:
            node = self.root
            for letter in word[::-1]:
                #traversing this thing backwards, assign the nodes to the letter in the reverse order
                if letter not in node.letter_dict:
                    node.letter_dict[letter] = TrieNode(letter)
                node = node.letter_dict[letter]
                
            node.start_of_word = True



    # helper to load words. No modifications needed
    def _load_words(self):
        words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                words.append(word)
        return words


#storing the x and y values and the uses in a separate class in order to figure out
#      a)simplicity when dealing with the surrounding tiles
#      b)keeping track of the amount of times i can use a tile without causing too much trouble
#        (trying to keep track of the times i can use each letter on the board on the exact same board became problematic)
#           - need to backtrack with the uses per word**
#keeps the code a bit clean 
class Tiles:
    def __init__(self, r:int, c:int, str_val:str, uses:int) -> None:
        self.r = r
        self.c = c
        self.str_val = str_val
        self.uses = uses

    def use(self) -> None:
        self.uses = self.uses-1

    def unuse(self) -> None:
        self.uses = self.uses + 1

    def is_available(self) -> bool:
        return self.uses > 0


# Implement the Boggled Solver. This Boggle has the following special properties:
# 1) All words returned should end in a specified suffix (i.e. encode the trie in reverse)
# 2) Board tiles may have more than 1 letter (e.g. "qu" or "an")
# 3) The number of times you can use the same tile in a word is variable
# Your implementation should account for all these properties.
class Boggled:

    def __init__(self):
        self.board = []
        self.max_uses = 0
        self.trie = Trie()
        self.visited = set()
        self.tile_dict = {}


    # setup test initializes the game with the game board and the max number of times we can use each 
    # tile per word
    def setup_board(self, max_uses_per_tile: int, board:List[List[str]])->None:
        self.max_uses = max_uses_per_tile 
        self.board = board
        self.word_set = set()
        self.trie = Trie()
        self.trie.generate_tree_from_file()
        #basic setup for the trie tree and the initial variables
        self.tile_dict = {}
        
        #make a second board with tile form to save x, y, str, uses
        self.tile_board = []
        r = 0
        for row in self.board:
            c = 0
            tile_list = []
            for col in row:
                tile = Tiles(r, c, self.board[r][c], self.max_uses)
                tile_list.append(tile)
                c+=1
            r=r+1
            self.tile_board.append(tile_list)
    
    # Returns a set of all words on the Boggle board that end in the suffix parameter string. Words can be found
    # in all 8 directions from a position on the board
    def get_all_words(self, suffix:str)->Set:
        #self.suffix = suffix
        r = 0
        found_words = set()
        for row in self.board:
            c = 0
            for col in self.board[0]:
                #all_words = self.get_all_words_recursive(self.trie.root, self.tile_board[r][c], self.board[r][c], self.suffix)
                #self.word_set.update(all_words)
                c+=1
                self.visited.clear()
                self.get_all_words_recursive(r, c, "", suffix, found_words)
            r+=1
        return found_words


    # recursive helper for get_all_words. Customize parameters as needed; you will likely need params for 
    # at least a board position and tile
    def get_all_words_recursive(self, r:int, c:int, current_word:str, suffix:str, found_words: Set[str]) -> None:
        #base case if tile is out of bounds or has already been visited
        if not (0 <= r < len(self.tile_board)) or not (0 <= c < len(self.tile_board[r])):
            return
        tile = self.tile_board[r][c]
        #if tile has been been used in path
        if ((r,c) in self.visited):
            return
        #if there are no more uses for the tile
        if not (tile.is_available()):
            return

        current_word += tile.str_val
        tile.use()

        if (current_word.endswith(suffix) and self.is_valid_word(current_word)):
            found_words.add(current_word)
        
        self.visited.add((r,c))

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in directions:
            row = r + x
            col = c + y
            self.get_all_words_recursive(row, col, current_word, suffix, found_words)

        tile.unuse()
        self.visited.remove((r,c))


    def is_valid_word(self, word:str) -> bool:
        node = self.trie.root
        for letter in word[::-1]:
            if letter not in node.letter_dict:
                return False
            node = node.letter_dict[letter]
        return node.start_of_word



game = Boggled()
board = [
['b', 'o', 'g', 'l'],
['e', 'r', 'a', 'e'],
['d', 'y', 'p', 'i'],
['t', 'r', 'e', 's']
]

game.setup_board(1, board)
result = game.get_all_words("er")
print(result)

