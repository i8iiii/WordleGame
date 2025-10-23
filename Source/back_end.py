class Wordle:
    def __init__(self, secret: str):
        self.secret = secret.lower()
        self.guesses = []
        self.game_over = False
        self.win = False
        
    def check_guess(self, guess: str):
        guess = guess.lower()
        feedback = []
        temp_secret = list(self.secret)
        
        for i in range(len(guess)):
            if (guess[i] == temp_secret[i]):
                feedback.append({'letter': guess[i].upper(), 'status': 'correct'})
                temp_secret[i] = None
            else: 
                feedback.append({'letter': guess[i].upper(), 'status': 'pending'})
            
        for i in range(len(guess)):
            if feedback[i]['status'] == 'pending':
                if feedback[i]['letter'].lower() in temp_secret:
                    feedback[i]['status'] = 'present'
                    temp_secret[temp_secret.index(feedback[i]['letter'].lower())] = None
                else:
                    feedback[i]['status'] = 'absent'
                        
        self.guesses.append(feedback)
        
        if all(f['status'] == 'correct' for f in feedback):
            self.game_over = True
            self.win = True
        elif len(self.guesses) >= 6:
            self.game_over = True
            self.win = False
            
        return feedback
        