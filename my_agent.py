__author__ = "<Max van der Sluis>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<vanma236@student.otago.ac.nz>"

import numpy as np

import helper


class WordleAgent():
    """
       A class that encapsulates the code dictating the
       behaviour of the Wordle playing agent

       ...

       Attributes
       ----------
       dictionary : list
           a list of valid words for the game
       letter : list
           a list containing valid characters in the game
       word_length : int
           the number of letters per guess word
       num_guesses : int
           the max. number of guesses per game
       mode: str
           indicates whether the game is played in 'easy' or 'hard' mode

       Methods
       -------
       AgentFunction(percepts)

           Returns the next word guess given state of the game in percepts

       deleteItems(deleted_items, possible_words)

           Deletes the incorrect words from the possible list of words

       frequencyChecker(possible_words, letters)

           Returns a list of scores for each letter based on their frequency in the possible words list
       """

    def __init__(self, dictionary, letters, word_length, num_guesses, mode, possible_words, word):
        """
      :param dictionary: a list of valid words for the game
      :param letters: a list containing valid characters in the game
      :param word_length: the number of letters per guess word
      :param num_guesses: the max. number of guesses per game
      :param mode: indicates whether the game is played in 'easy' or 'hard' mode
      """

        self.word = word
        self.dictionary = dictionary
        self.letters = letters
        self.word_length = word_length
        self.num_guesses = num_guesses
        self.mode = mode
        self.possible_words = possible_words

    def deleteItems(deleted_items, possible_words):
        """Deletes the impossible words from the possible words list

        :param deleted_items: A lsit of the words that should be removed
        :param possible_words: The current list of possible words
        """
        for d in deleted_items:
            if d in possible_words:
                possible_words.remove(d)

    def frequencyChecker(self, possible_words, letters):
        """Returns a list of each letter's corresponding frequency out of the words in the possible words list

        :param possible_words: The current list of possible words
        :param letters: A list of all the letters in the alphabet
        :return: A list of each letter's frequency score
        """
        # Creating a score list of length as long as the corresponding languages alphabet is
        scores = [0] * len(self.letters)
        for i in possible_words:
            temp_scores = helper.word_to_letter_indices(i, letters)
            for x in temp_scores:
                scores[x] += 1
        return scores

    def AgentFunction(self, percepts):

        """Returns the next word guess given state of the game in percepts

      :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
      :return: string - a word from self.dictionary that is the next guess
      """

        # This is how you extract three different parts of percepts.
        guess_counter, letter_indexes, letter_states = percepts
        correct_letters = []  # list of indexes of correct letters in the correct spot
        correct_letters_char = []  # list of characters that are in the correct spot
        wrong_spot_letters = []  # list of indexes of correct letters that are in the wrong spot
        wrong_spot_letters_char = []  # list of characters that are correct but in the wrong spot
        wrong_letters = []  # list for the indexes of any incorrect letters in the word
        deleted_items = []  # list to store the items to be deleted
        if guess_counter == 0:
            self.possible_words = list(self.dictionary)
        else:
            i = 0
            # Loop saving the places of each correct/wrong position letter
            while i < len(letter_states):
                # If the letter is in the correct spot
                if letter_states[i] == 1:
                    correct_letters.append(i)
                    # Removing the words that don't have the correct letter in the correct spot
                    for x in correct_letters:
                        # Adding the correct letters to a list for future use to prevent words being taken out with
                        # multiple of the same letters when only one is correct
                        if self.word[x] not in correct_letters_char:
                            correct_letters_char.append(self.word[x])
                        for y in self.possible_words:
                            if self.word[x] != y[x]:
                                deleted_items.append(y)
                    i += 1
                # If the letter is correct but in the wrong spot
                elif letter_states[i] == -1:
                    wrong_spot_letters.append(i)
                    # Deleting words that don't contain the right characters in the wrong place in them
                    for x in wrong_spot_letters:
                        # Adding correct letters to a list for future use to prevent words being taken out with
                        # multiple of the same letters when only one is correct
                        if self.word[x] not in wrong_spot_letters_char:
                            wrong_spot_letters_char.append(self.word[x])
                        for y in self.possible_words:
                            if self.word[x] not in y:
                                deleted_items.append(y)
                            # Deleting words with the right character in the wrong place
                            if self.word[x] == y[x]:
                                deleted_items.append(y)
                    i += 1
                # If the letter is incorrect
                elif letter_states[i] == 0:
                    wrong_letters.append(i)
                    for x in wrong_letters:
                        for y in self.possible_words:
                            # If a wrong letter is in a possible word, delete it BUGGED: Sometimes deletes every
                            # possible word
                            if self.word[x] in y and self.word[x] not in correct_letters_char\
                                    and self.word[x] not in wrong_spot_letters_char:
                                deleted_items.append(y)
                    i += 1
        # Deleting all impossible words from possible words
        WordleAgent.deleteItems(deleted_items, self.possible_words)
        print("Possible words left: ", len(self.possible_words))
        # Getting the most common letter from the remaining words
        scores = WordleAgent.frequencyChecker(self, self.possible_words, self.letters)
        top_index = [scores.index(max(scores))]
        word_index = 0
        # Implementing the frequency checker to guess words with the most common remaining letters in them
        for i in self.possible_words:
            # If the most common letter is in a word of the possible words, add it to a list to be guessed from
            if helper.letter_indices_to_word(top_index, self.letters) in i:
                common_letter_words = [self.possible_words.index(i)]
                common_index = np.random.randint(0, len(common_letter_words))
                word_index = common_letter_words[common_index]
            else:
                word_index = np.random.randint(0, len(self.possible_words))
        # Making sure it doesn't try to remove a word from possible words
        # when there are none left in the case it gets the word correct
        if len(self.possible_words) > 0:
            self.word = self.possible_words[word_index]
            self.possible_words.remove(self.word)
        return self.word
