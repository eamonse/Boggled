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
        self.root = TrieNode(None)
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



# Implement the Boggled Solver. This Boggle has the following special properties:
# 1) All words returned should end in a specified suffix (i.e. encode the trie in reverse)
# 2) Board tiles may have more than 1 letter (e.g. "qu" or "an")
# 3) The number of times you can use the same tile in a word is variable
# Your implementation should account for all these properties.
class Boggled:

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
        self.use_board = []
        r = 0
        for row in self.board:
            c = 0
            tile_list = []
            use_list = []
            for col in row:
                tile = Tiles(r, c, self.board[r][c], self.max_uses)
                tile_list.append(tile)
                use_list.append(max_uses_per_tile)
                c+=1
            r=r+1
            self.tile_board.append(tile_list)
            self.use_board.append(use_list)
    
    # Returns a set of all words on the Boggle board that end in the suffix parameter string. Words can be found
    # in all 8 directions from a position on the board
    def get_all_words(self, suffix:str)->Set:
        self.suffix = suffix
        r = 0
        for row in self.board:
            c = 0
            for col in self.board[0]:
                all_words = self.get_all_words_recursive(self.trie.root, self.tile_board[r][c], self.board[r][c], self.suffix)
                self.word_set.update(all_words)
                c+=1
            r+=1
        return self.word_set


    # recursive helper for get_all_words. Customize parameters as needed; you will likely need params for 
    # at least a board position and tile
    def get_all_words_recursive(self, node:TrieNode, current_tile:Tiles, built_str:str, suffix):
        #cases to check - board usage, then if it can find the suffix, then build any possible words from there
        
        #it should not be taking me too much in order to complete the recursive method
        #focus on getting the suffix and then looking at the rest of the possible word.
        cur_node = node
        word = built_str
        #base case if there are no more uses left in the tile
        if current_tile.uses == 0:
            return set()


        for letter in current_tile.str_val[::-1]:           
            if letter not in cur_node.letter_dict:
                #if you can't traverse any further into the str
                return 
            #suffix implementation
            suf_length = len(suffix) - len(word)
            if suf_length > 0 and suffix[suf_length-1] != letter:
                return set()
            word = letter + word
            #otherwise, keep going deeper into the tree
            cur_node = cur_node.letter_dict[letter]
        
        word_set = set()
        if cur_node.start_of_word and len(word) > len(suffix):
            #if you reach the start of the word (meaning reached the end of the word) then add it
            word_set.add(word)
        
    
        sur_tiles = self.surrounding_tiles_list(current_tile)
        current_tile.use()
        for tile in sur_tiles:
            if tile.uses > 0:
                self.get_all_words_recursive(cur_node, tile, word, suffix)
        current_tile.unuse()
        return word_set

    def surrounding_tiles_list(self, tile:Tiles) -> List[Tiles]:
        avail_tiles = []
        #r = y, c = x
        if tile.r != 0 and tile.r != len(self.tile_board)-1 and tile.c != 0 and tile.c != len(self.tile_board)-1:
            #if its not amy of the tiles along the border, add 8 tiles around.
            avail_tiles.append(self.tile_board[tile.r][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
        elif tile.r == 0 and tile.c == 0:
            #top left corner
            avail_tiles.append(self.tile_board[tile.r][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
        elif tile.r == len(self.tile_board)-1 and tile.c == 0:
            #bottom left corner
            avail_tiles.append(self.tile_board[tile.r][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
        elif tile.r == 0 and tile.c == len(self.tile_board)-1:
            #top right corner
            avail_tiles.append(self.tile_board[tile.r][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
        elif tile.r == len(self.tile_board)-1 and tile.c == len(self.tile_board)-1:
            #bottom right corner
            avail_tiles.append(self.tile_board[tile.r][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
        elif tile.r == 0:
            #for the top row not including corners
            avail_tiles.append(self.tile_board[tile.r][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r][tile.c-1])
        elif tile.r == len(self.tile_board)-1:
            #for the bottom row not including corners
            avail_tiles.append(self.tile_board[tile.r][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r][tile.c-1])
        elif tile.c == 0:
            #for the left col not including corners
            avail_tiles.append(self.tile_board[tile.r][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c+1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c+1])
        elif tile.c == len(self.tile_board)-1:
            #for the right col not including corners
            avail_tiles.append(self.tile_board[tile.r][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c-1])
            avail_tiles.append(self.tile_board[tile.r-1][tile.c])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c])
            avail_tiles.append(self.tile_board[tile.r+1][tile.c-1])       
        return avail_tiles


