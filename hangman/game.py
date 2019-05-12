from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self, letter, hit = None, miss = None):
        self.letter = letter
        self.hit = hit
        self.miss= miss
        
        if miss and hit:
            raise InvalidGuessAttempt()
    
    def is_hit(self):
        if self.hit:
            return True
        return False
    def is_miss(self):
        if self.miss:
            return True
        return False
            


class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer
        self.masked = '*'*len(self.answer)
        if len(self.answer) == 0 or len(self.masked)==0:
            raise InvalidWordException()
            
    def uncover_word(self, letter):
            
        new_word = self.masked
        letter = letter.lower()
        self.answer = self.answer.lower()

        for idx, char in enumerate(self.answer):
            if char == letter:
                new_word = self.masked[:idx] + char + self.masked[idx+1:]
                self.masked = new_word
            
        self.masked = new_word
            
        return self.masked
        
    def perform_attempt(self, letter):
        
        if len(letter)>1:
            raise InvalidGuessedLetterException()
        if len(self.answer) != len(self.masked):
            raise InvalidWordException()
            
        if letter.lower() in self.answer.lower():
            attempt = GuessAttempt(letter, hit = True)
            self.masked = self.uncover_word(letter)
        else:
            attempt = GuessAttempt(letter, miss = True)
        return attempt
    
    

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
    
    def __init__(self, word_list = WORD_LIST, number_of_guesses = 5):
        self.word_list = word_list
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        selected_word= self.select_random_word(word_list)
        self.word = GuessWord(selected_word)
        
        

    def is_won (self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses ==0 and self.word.answer != self.word.masked:
            return True
        return False
    
    def is_finished(self):
        if self.is_lost() or self.is_won():
            return True
        return False
     
        
    def guess(self, letter):
        
        if self.is_finished():
            raise GameFinishedException()
        
        self.previous_guesses.append(letter.lower()) 
        attempt = self.word.perform_attempt(letter)
        
        if attempt.is_miss():
            self.remaining_misses -=1
            if self.remaining_misses < 1:
                raise GameLostException()
                
        if self.is_won():
            raise GameWonException()
            
        return attempt
                


