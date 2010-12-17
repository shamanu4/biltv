# To change this template, choose Tools | Templates
# and open the template in the editor.


class Roll():

    def __init__(self):
        self.cash = 100
        self.bid = [None,None]
        self.black = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
        self.red = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
        self.odd = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35)
        self.even = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36)

    def s(self,bid,sum):
        self.bid=[bid,sum]
        self.cash -= sum
        print "Bid placed: %s sum %s. cash: %s" % (self.bid[0],self.bid[1],self.cash)

    def win(self,multiplier):
        self.cash += self.bid[1]*multiplier
        print "You WIN! %s. cash: %s" % (self.bid[1]*multiplier,self.cash)

    def roll(self):
        import random        
        rand = random.randrange(0, 37)
        color= "ZERO"
        parity = "ZERO"
        if rand in self.red:
            color="RED"
            if self.bid[0] == 'r':
                self.win(2)
        if rand in self.black:
            color="BLACk"
            if self.bid[0] == 'b':
                self.win(2)
        if rand in self.odd:
            parity="ODD"
            if self.bid[0] == 'o':
                self.win(2)
        if rand in self.even:
            parity="EVEN"
            if self.bid[0] == 'e':
                self.win(2)
        if color == 'ZERO':
            if self.bid[0] == 'z' or self.bid == 0:
                self.win(36)
        if self.bid[0] == rand:
            self.win(36)        
        print "%s [%s] [%s]" % (rand,color,parity)
        self.bid = [None,None]



