class Hangman:
    def __init__(self, target):
        self.target = target
        self.tries = 0
        self.used = set()
        temp = []
        for letter in target:
            if letter == ' ':
                temp.append(' ')
            else:
                temp.append('_')
        self.player = temp
        self.board = [['_________',
                       '|         |',
                       '|        ',
                       '|        ',
                       '|        ',
                       '|',
                       '|'],
                        ['_________',
                         '|         |',
                         '|         0',
                         '|        ',
                         '|        ',
                         '|',
                         '|'],
                         ['_________',
                         '|         |',
                         '|         0',
                         '|         |',
                         '|         ',
                         '|',
                         '|'],
                          ['_________',
                         '|         |',
                         '|         0',
                         '|         |',
                         '|        / ',
                         '|',
                         '|'],
                            ['_________',
                         '|         |',
                         '|         0',
                         '|         |',
                         '|        / \\',
                         '|',
                         '|'],
                            ['_________',
                         '|         |',
                         '|         0',
                         '|        /|',
                         '|        / \\',
                         '|',
                         '|'],
                            ['_________',
                         '|         |',
                         '|         0',
                         '|        /|\\',
                         '|        / \\',
                         '|',
                         '|']]
    
    def guess(self, letter):
        if len(letter) != 1:
            print("Invalid input")
            return False
        
        if letter in self.used:
            print("You have already tried you idiot. Try again")
            return False
        
        elif letter not in self.target:
            self.tries += 1
            print("Incorrect. Try again dumbo")
            return False
        
        self.used.add(letter)
       
        for i in range(len(self.target)):
            if self.target[i] == letter:
                self.player[i] = letter
        return True
   
    def displayWord(self):
        return " ".join(self.player)
    
    def displayBoard(self):
        for line in self.board[self.tries]:
            print(line)
            
    def run(self):
        print("Welcome to Hangman")
        self.displayBoard()
        self.displayWord()
        while '_' in self.player:
            print("Guess a letter: ")
            while not self.guess(input()):
                self.displayBoard()
                if self.tries == 6:
                    print("Game Over")
                    return
            print(self.displayWord())
        
        print("Congratulations! You won")
            
        
    
game = Hangman("ANASTASIA DOESN'T NEED SUFFRAGE")
game.run()