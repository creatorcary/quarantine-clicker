# Logan Cary
# Quarantine Clicker
# A game where you recursively click things to earn money
# CS125 Final Project, Wilkes University
# Created Mon Jul 6 2020
#
# Icons from flaticon.com; Designers: surang, Freepik, prettycons
#
# Milestone 1:  Set up GUI with graphics library
#               7/7/20
# Milestone 2:  Create money variable and allow it to increase when items are clicked
#               Fill up click meters
#               7/7/20
# Milestone 3:  Allow items to be upgraded with money
#               7/7/20
# Milestone 4:  Add managers to automate clicking
#               7/8/20
# Milestone 5:  Allow certain items to be unlocked with money
#               - start with one clicker and buy the rest
# Milestone 6:  Allow game to be saved and resumed using file I/O
# Milestone 7:  Create tutorial
# Milestone 8:  Add music, SFX, particle effects
# Milestone 9:  Tweak upgrade costs, robot costs, rewards
# Milestone 10: Fix runaway text


from graphics import *
from math import ceil


class QClicker:

    # static constants for GraphWin dimensions
    WIN_WIDTH  = 768
    WIN_HEIGHT = 432

    arrow = u'\u2191'

    def __init__(self):
        # Initialize member fields
        self.win = GraphWin("Quarantine Clicker", QClicker.WIN_WIDTH, QClicker.WIN_HEIGHT,\
                            autoflush=False)
        self.money = 0.0
        self.moneyField = Rectangle(Point(74,40), Point(574,110))
        self.moneyText = Text(Point(190,75), "$0.00")
        
        # tuple of "clickers" represented by dictionaries
        # KEYS: name, file, clickCap, reward, meter,
        #       text, button, icon, upgradeText, robotText, robots
        self.clickers = (
            {"name":"Bake Bread", "file":"bread.gif", "clickCap":3, "reward":.50},\
            {"name":"Home Workout", "file":"workout.gif", "clickCap":5, "reward":2.00},\
            {"name":"Stream Show", "file":"netflix.gif", "clickCap":7, "reward":5.00},\
            {"name":"Call Grandma", "file":"phone.gif", "clickCap":9, "reward":9.50},\
            {"name":"Play Online Game", "file":"vr-gaming.gif", "clickCap":11, "reward":15.25},\
            {"name":"Sell Homemade Mask", "file":"face-mask.gif", "clickCap":13, "reward":23.00}
        )

        # Draw background
        Image(Point(QClicker.WIN_WIDTH/2, QClicker.WIN_HEIGHT/2), "background.gif").draw(self.win)

        # Draw money icon and field at top of window
        self.moneyField.setFill("gray")
        self.moneyField.draw(self.win)
        Image(Point(74,74), "coin.gif").draw(self.win)

        # Draw text that displays money variable
        self.moneyText.setTextColor("white")
        self.moneyText.setSize(36)
        self.moneyText.draw(self.win)

        # Draw clickers
        self.drawClickers()

    # draws "clickers" while adding more information to them
    def drawClickers(self):
        padX = 64
        padY = 200
        rLength = 300
        
        for i in range(len(self.clickers)):
            # Determines x,y of where clicker icon will go
            x = (i%2) * (QClicker.WIN_WIDTH/2) + padX
            y = (i//2 % 3) * (QClicker.WIN_HEIGHT/5) + padY

            # Draw the following for every clicker:
            
            # upgrade tab
            tab = Rectangle(Point(x+2*rLength//3, y-40), Point(x+rLength-5, y-20))
            tab.setFill("white")
            tab.draw(self.win)

            # robot tab
            rtab = Rectangle(Point(x+20, y-40), Point(x+170, y-20))
            rtab.setFill("white")
            rtab.draw(self.win)

            # empty gray click meter
            r = Rectangle(Point(x,y-20), Point(x+rLength,y+20))
            r.setFill("gray")
            r.draw(self.win)

            # upgrade text (displays cost of upgrade on upgrade tab)
            ut = Text(Point(x+5*rLength//6, y-30), QClicker.arrow + " cost: " +
                      format(10*self.clickers[i]["reward"], ',.2f'))
            ut.setTextColor("red")
            ut.draw(self.win)
            self.clickers[i]["upgradeText"] = ut

            # robot text (displays cost of robot on robot tab)
            rt = Text(Point(x+95, y-30), "hire robot: " +
                      format((self.clickers[i]["clickCap"]-2)*50, ',.2f'))
            rt.setTextColor("red")
            rt.draw(self.win)
            self.clickers[i]["robotText"] = rt
            self.clickers[i]["robots"] = 0

            # green meter
            self.clickers[i]["position"] = Point(x,y)
            self.clickers[i]["meter"] = Rectangle(Point(x,y-20), Point(x+20,y+20))
            self.clickers[i]["meter"].setFill("green")
            self.clickers[i]["meter"].draw(self.win)

            # text (displays the name and reward of the clicker)
            t = Text(Point(x + rLength/2, y), self.clickers[i]["name"] + " - $" +
                     format(self.clickers[i]["reward"], ',.2f'))
            t.setTextColor("white")
            t.setStyle("italic")
            t.draw(self.win)
            self.clickers[i]["text"] = t

            # button (white circle under clicker icon)
            c = Circle(Point(x,y), 32)
            c.setFill("white")
            c.draw(self.win)
            self.clickers[i]["button"] = c

            # icon
            img = Image(Point(x,y), self.clickers[i]["file"]).draw(self.win)
            self.clickers[i]["icon"] = img

    # checks if a clicker was clicked and handles the click
    def checkIconClick(self, p):
        for c in self.clickers:
            
            if p.getX() <= c["position"].getX()+32 and p.getX() >= c["position"].getX()-32 and\
               p.getY() <= c["position"].getY()+32 and p.getY() >= c["position"].getY()-32:
                # this clicker was clicked
                # move meter forward
                c["meter"].p2.x += 280 / c["clickCap"]
                         
                self.updateMeter(c)
                return True

        return False

    # checks if an upgrade tab was clicked and handles the click
    def checkUpgradeClick(self, p):
        for c in self.clickers:
            textp = c["upgradeText"].getAnchor()
            
            if p.getX() <= textp.getX()+50 and p.getX() >= textp.getX()-50 and\
               p.getY() <= textp.getY()+10 and p.getY() >= textp.getY()-10:
                # this tab was clicked
                cost = c["reward"]*10
                
                if self.money >= cost:
                    # the player can afford the upgrade
                    self.money -= cost
                    c["reward"] = round(c["reward"] * 1.2, 2)
                    c["text"].setText(c["name"] + " - $" +
                                      format(c["reward"], ',.2f'))
                    c["upgradeText"].setText(QClicker.arrow + " cost: " +
                                      format(10*c["reward"], ',.2f'))
                    self.updateText()
                    
                return True

        return False

    # checks if a robot tab was clicked and handles the click
    def checkRobotClick(self, p):
        for c in self.clickers:
            textp = c["robotText"].getAnchor()
            
            if p.getX() <= textp.getX()+75 and p.getX() >= textp.getX()-75 and\
               p.getY() <= textp.getY()+10 and p.getY() >= textp.getY()-10:
                # this tab was clicked
                cost = (c["clickCap"]-2) * 50 * (c["robots"]+1)
                
                if self.money >= cost:
                    # the player can afford the upgrade
                    self.money -= cost
                    c["robots"] += 1
                    c["robotText"].setText("hire robot: " +
                                      format((c["clickCap"]-2)*50*(c["robots"]+1), ',.2f'))
                    self.updateText()
                    
                return True

        return False

    # advance click meters for all clickers with robots
    def robotClicks(self):
        for c in self.clickers:
            if c["robots"]:
                pixPerRobot = 5 / c["clickCap"]
                c["meter"].p2.x += c["robots"] * pixPerRobot
                self.updateMeter(c)

    # changes colors of all upgrade text from red/green to show if
    # the player can afford the upgrade
    def changeTabColors(self):
        for c in self.clickers:
            
            # upgrades
            if self.money >= c["reward"]*10:
                c["upgradeText"].setTextColor("green")
            else:
                c["upgradeText"].setTextColor("red")
                
            # robots
            if self.money >= (c["clickCap"]-2)*50*(c["robots"]+1):
                c["robotText"].setTextColor("green")
            else:
                c["robotText"].setTextColor("red")

    # redraws everything over the meter when it is updated
    # must be called every time a green meter changes
    def updateMeter(self, c):
        while ceil(c["meter"].p2.x) >= c["position"].getX() + 300: # meter is full
            # clear meter
            c["meter"].p2.x -= 280 

            # collect reward
            self.money += c["reward"]
            self.updateText()
        
        c["meter"].redraw(self.win)
        c["button"].redraw(self.win)
        c["icon"].redraw(self.win)
        c["text"].redraw(self.win)

    # updates moneyText to display value of money variable
    # must be called every time money variable changes
    def updateText(self):
        oldText = self.moneyText.getText()
        newText = "$" + format(self.money, ',.2f')
        self.moneyText.setText(newText)
        # move text 14 pixels for every new or lost character to keep it aligned left
        dx = (len(newText)-len(oldText)) * 14
        self.moneyText.move(dx,0)

    # main game loop
    def loop(self):
        while self.win.isOpen():
            click = self.win.checkMouse() # returns None if there was no click,
                                          # otherwise returns a Point
            if click:
                if not self.checkIconClick(click):
                    if not self.checkUpgradeClick(click):
                        self.checkRobotClick(click)
                    
            self.changeTabColors()
            self.robotClicks()
            update(60) # refreshes the window no more than 60 times per second

if __name__ == "__main__":
    game = QClicker()
    game.loop()
