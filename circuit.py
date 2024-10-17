from cmu_graphics import *

class LogicGate:

    nextInputLabel = ord('A')
    
    def __init__(self,x,y,gateType):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 40
        self.gateType = gateType
        self.highlighted = False
        self.radius = 5
        self.label = None
        

    def draw(self,app):
        
        if app.highlightedGates is not None and self in app.highlightedGates:
            drawRect(self.x, self.y, self.width, self.height, fill='lightGreen', border='black')


        if self.gateType == 'And':
            drawRect(self.x, self.y, 60, 40, fill=None, border='black')
            drawLabel('And', self.x+ self.width/2, self.y + self.height/2, size=16, bold=True)  # Adjusted label position
            drawCircle(self.x, self.y +self.height//3, self.radius)  
            drawCircle(self.x, self.y +2*self.height//3, self.radius)  
            drawCircle(self.x +self.width, self.y+self.height//2, self.radius)
            
        elif self.gateType == 'Or':
            drawRect(self.x,self.y, 60, 40,fill=None, border='black')
            drawLabel('Or', self.x+ self.width/2, self.y + self.height/2, size=16, bold=True)  # Adjusted label position
            drawCircle(self.x, self.y +self.height//3, self.radius)  
            drawCircle(self.x, self.y +2*self.height//3, self.radius)  
            drawCircle(self.x +self.width, self.y+self.height//2, self.radius)
        
        elif self.gateType == 'Not':
            drawRect(self.x,self.y, 60, 40,fill=None, border='black')
            drawLabel('Not', self.x+ self.width/2, self.y + self.height/2, size=16, bold=True)  # Adjusted label position
            drawCircle(self.x, self.y+self.height//2, self.radius)  
            drawCircle(self.x +self.width, self.y+self.height//2, self.radius)
            
        elif self.gateType == 'Input':
            drawRect(self.x, self.y, 60, 40, fill=None, border='black')
            if self.label:
                drawLabel(self.label, self.x + self.width/2, self.y + self.height/2, size=16, bold=True)  
            else:
                drawLabel('Input', self.x + self.width/2, self.y + self.height/2, size=16, bold=True)  
            drawCircle(self.x + self.width, self.y + self.height//2, self.radius)
    
        elif self.gateType == 'Output':
            drawRect(self.x,self.y, 60, 40,fill=None, border='black')
            drawLabel('Output', self.x+ self.width/2, self.y + self.height/2, size=16, bold=True)  # Adjusted label position
            drawCircle(self.x, self.y+self.height//2, self.radius)  

        
    def isInside(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

                
        
            

####################################################
# onAppStart: called only once when app is launched
####################################################

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.gates = []
    app.highlightedGates = set()
    app.currentGate = None

    andGate = LogicGate(25,50,'And')
    app.gates.append(andGate)
    
    orGate = LogicGate(25,110,'Or')
    app.gates.append(orGate)
    
    notGate = LogicGate(25,170,'Not')
    app.gates.append(notGate)
    
    inputGate = LogicGate(25,230,'Input')
    app.gates.append(inputGate)
    
    outputGate = LogicGate(25,290,'Output')
    app.gates.append(outputGate)

####################################################
# Code used by multiple screens
####################################################

def onKeyPressHelper(app, key):
    # Since every screen does the same thing on key presses, we can
    # write the main logic here and just have them call this helper fn
    # You should add/edit some code here...
    if   key == 'e': setActiveScreen('editScreen')
    elif key == 'r': setActiveScreen('runScreen')

def drawScreenTitle(app, screenTitle):
    drawLabel('Logic Circuit Simulator', app.width/2, 20, size=16, bold=True)
    drawLabel('Press e to edit or r to run', app.width/2, 40, size=14)
    drawLabel(screenTitle, app.width/2, 60, size=14, bold=True)

    
    
####################################################
# editScreen
####################################################

def editScreen_redrawAll(app):
    drawScreenTitle(app, 'Edit Mode')
    drawLine(100,50,100,600)
    
    for gate in app.gates:
        gate.draw(app)


    
    

def editScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

def editScreen_onMouseDrag(app, mouseX, mouseY):
    if app.currentGate in app.highlightedGates and app.currentGate.x > 100:
        app.currentGate.x = mouseX - 30
        app.currentGate.y = mouseY - 20

def editScreen_onMousePress(app, mouseX, mouseY):
    app.highlightedGates.clear()
    for gate in app.gates:
        if gate.isInside(mouseX, mouseY):
            app.highlightedGates.add(gate)
            app.currentGate = gate
            
    if mouseX > 100 and app.currentGate is not None and app.currentGate.x <= 100:
        # If a gate is highlighted, copy its properties and draw it at the clicked position
        if app.currentGate:
            new_gate = LogicGate(mouseX-30, mouseY-20, app.currentGate.gateType)
            app.gates.append(new_gate)
            app.currentGate = new_gate
            app.highlightedGates.add(new_gate)

            # Update the next input label only if the new gate is an input gate
            if new_gate.gateType == 'Input':
                new_gate.label = chr(LogicGate.nextInputLabel)
                LogicGate.nextInputLabel += 1



    

    
####################################################
# runScreen
####################################################

def runScreen_redrawAll(app):
        drawScreenTitle(app, 'Run Mode')


def runScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)
 
    
####################################################
# main function
####################################################

def main():
    
    runAppWithScreens(initialScreen='editScreen')

main()