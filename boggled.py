from typing import List, Tuple, Set

class TrieNode:
    def __init__(self, letter=None) -> None:
        self.letter = letter
        # add attributes for whether it is the end of a word and a collection of pointers to
        # next letters

class Trie:
    def __init__(self) -> None:
        pass

    def generate_tree_from_file(self)->None:
        words = self._load_words()
        #add code here to set up the TrieNode tree structure for the words
        

    # helper to load words. No modifications needed
    def _load_words(self):
        words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                words.append(word)
        return words

# Implement the Boggled Solver. This Boggle has the following special properties:
# 1) All words returned should end in a specified suffix (i.e. encode the trie in reverse)
# 2) Board tiles may have more than 1 letter (e.g. "qu" or "an")
# 3) The number of times you can use the same tile in a word is variable
# Your implementation should account for all these properties.
class Boggled:

    # setup test initializes the game with the game board and the max number of times we can use each 
    # tile per word
    def setup_board(self, max_uses_per_tile: int, board:List[List[str]])->None:
        pass

    
    # Returns a set of all words on the Boggle board that end in the suffix parameter string. Words can be found
    # in all 8 directions from a position on the board
    def get_all_words(self, suffix:str)->Set:
        pass


    # recursive helper for get_all_words. Customize parameters as needed; you will likely need params for 
    # at least a board position and tile
    def get_all_words_recursive(self):
        pass