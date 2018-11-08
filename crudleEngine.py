from sfml import sf
import pyperclip
import json
import random
import time


debug_mode = False

background_color = 34,35,28
background_color2 = 84,85,78
window_size = 1280 ,800
window = sf.RenderWindow(sf.VideoMode(*window_size), "Test",sf.Style.CLOSE)
window.vertical_synchronization = True
image = sf.Image.from_file("icon.png")
window.set_icon(image.width, image.height, bytes(image.pixels))    
move_keys = [sf.Keyboard.W,sf.Keyboard.S,sf.Keyboard.A,sf.Keyboard.D]
down_keys = [sf.Keyboard.S,sf.Keyboard.DOWN]
up_keys = [sf.Keyboard.W,sf.Keyboard.UP]
left_keys = [sf.Keyboard.A,sf.Keyboard.LEFT]
right_keys = [sf.Keyboard.D,sf.Keyboard.RIGHT]
confirm_keys = [sf.Keyboard.SPACE,sf.Keyboard.RETURN]

clock = sf.Clock()
clock.restart()
#------------------------------------------------------------------------------

def teleport(level_name):
    state_machine.states[len(state_machine.states)-2].level.load("data/files/levels/"+level_name+".json")
    #
def group(iterable, count):
    return zip(*[iter(iterable)] * count)
    #
def test_button_function():
    print("button pressed")
    #-
def close_window():
    window.close()
    #-
def begin_game():
    state_machine.setState(State("game_state"))
    #-
def inPolygon(x, y, xp, yp):
    c=0
    for i in range(len(xp)):
        if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and \
            (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c    
    return c 
#print(inPolygon(100, 0, (-100, 100, 100, -100), (100, 100, -100, -100)))
def default_event_handler(event):                                           
    if event == sf.Event.CLOSED:
        window.close()
    elif event == sf.Event.KEY_PRESSED:
        if event['code'] == sf.Keyboard.TILDE:
            state_machine.addState(Console())
    elif event == sf.Event.RESIZED:
        visibleArea = [0, 0, event['width'],event['height']]
        window.view = sf.View(visibleArea)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class Loot(object):
    """docstring for Loot"""
    def __init__(self, arg):
        super(Loot, self).__init__()
        self.arg = arg   
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class Animation(object):                                                    
    def __init__(self,animation_name,x_begin,y_begin,width,height,x_step,y_step,frame_count,speed):
        self.frames = []
        self.name = animation_name
        for i in range(frame_count):
            self.frames.append([x_begin+i*x_step,y_begin+i*y_step,width,height])
        
        self.currentFrame = 0
        self.speed = speed
        self.isPlaying = False

    def tick(self,time):
        if not self.isPlaying:
            return

        self.currentFrame = self.currentFrame + self.speed*time

        if self.currentFrame>=len(self.frames)-1:
            self.currentFrame=0

    #currentFrame
    #texture
    #vector<rect>

#------------------------------------------------------------------------------

class AnimationManager(object):                                             
    def __init__(self):
        self.animations = []

    def create(self,Animation):
        self.animations.append(Animation)

    def update(self,sprite,time):
        for animation in self.animations:
            if animation.isPlaying:
                animation.tick(time)
                sprite.texture_rectangle = animation.frames[int(animation.currentFrame)]

    def play(self,animation_name):
        for animation in self.animations:
            if animation.name == animation_name:
                if not animation.isPlaying:
                    animation.isPlaying = True
                    animation.currentFrame = 0
            else:
                animation.isPlaying = False

#------------------------------------------------------------------------------

class Player(sf.Drawable):                                                  
    def __init__(self):
        super(Player, self).__init__()
        self.texture = sf.Texture.from_file("data/images/basic_human.png")
        self.sprite = sf.Sprite(self.texture)
        self.sprite.texture_rectangle = [25,15,100,170]
        self.x_pos = 0
        self.y_pos = 0
        self.direction = 0
        self.x_speed = 0
        self.y_speed = 0
        self.movespeed = 0.3
        self.maxHP = 100
        self.currntHP = 95
        self.animations = AnimationManager()
        self.animations.create(Animation("walk_forward",25,15+190,75,185,0,190,5,0.0125))
        self.animations.create(Animation("walk_back",275,15+190,75,185,0,190,5,0.0125))
        self.animations.create(Animation("walk_left",155,15+190,75,185,0,190,5,0.0125))
        self.animations.create(Animation("walk_right",410,15+190,75,185,0,190,5,0.0125))
        self.animations.create(Animation("stay_forward",25,15,75,155,0,185,1,0.01))
        self.animations.create(Animation("stay_back",275,15,75,155,0,185,1,0.01))
        self.animations.create(Animation("stay_left",155,15,75,155,0,185,1,0.01))
        self.animations.create(Animation("stay_right",410,15,75,155,0,185,1,0.01))

        self.animations.play("stay_back")
        self.sprite.position = [window.size.x/2,window.size.y/2]
        self.sprite.origin = [36,140]
        self.magic_hand = sf.CircleShape()
        self.magic_hand.radius = 10
        self.x_magicoffset = 0
        self.y_magicoffset = 0
        self.usable_counter = None 
        self.inventory = []

    def addObject(self,code):
        self.inventory.append(code)

    def moveTo(self,x,y):
        self.sprite.position = [x,y]

    def recoverHP(self,value):
        self.currntHP+=value
        if self.currntHP>self.maxHP:
            self.currntHP=self.maxHP

    def draw(self,target,states):
        target.draw(self.sprite)
        target.draw(self.magic_hand)
        #for obj in self.inventory:
        #    target.draw(obj)

    def update(self,time):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
            self.y_speed = 1
            self.x_speed = -1.73
            self.y_magicoffset = 10
            self.x_magicoffset = -17
            self.animations.play("walk_back")
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.A):
            self.y_speed = -1
            self.x_speed = -1.73
            self.y_magicoffset = -10
            self.x_magicoffset = -17
            self.animations.play("walk_left")
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.D):
            self.y_speed = 1
            self.x_speed = 1.73
            self.y_magicoffset = 10
            self.x_magicoffset = 17
            self.animations.play("walk_right")
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.W):
            self.y_speed = -1
            self.x_speed = 1.73
            self.y_magicoffset = -10
            self.x_magicoffset = 17
            self.animations.play("walk_forward")

        self.sprite.move([self.x_speed*time*self.movespeed,self.y_speed*time*self.movespeed])
        self.animations.update(self.sprite,time)
        self.magic_hand.position = self.sprite.position.x+self.x_magicoffset*3,self.sprite.position.y+self.y_magicoffset*3

    def event_handler(self,event):
        if event == sf.Event.KEY_RELEASED:
            if event['code'] in move_keys:
                if event['code'] in up_keys:
                    self.animations.play("stay_forward")
                elif event['code'] in down_keys:
                    self.animations.play("stay_back")
                elif event['code'] in left_keys:
                    self.animations.play("stay_left")
                elif event['code'] in right_keys:
                    self.animations.play("stay_right")
                self.y_speed = 0
                self.x_speed = 0
        if event == sf.Event.KEY_PRESSED:       
            if event['code'] in confirm_keys:
                if self.usable_counter != None:
                    self.usable_counter.activate()
            if event['code'] == sf.Keyboard.I:
                state_machine.addState(InventoryState(self))

        '''if event == sf.Event.KEY_PRESSED:
            if event['code'] == sf.Keyboard.S:
                self.y_speed = 1
                self.x_speed = -2
                self.animations.play("walk_back")

            if event['code'] == sf.Keyboard.W:
                self.y_speed = -1
                self.x_speed = 2
                self.animations.play("walk_forward")    

            if event['code'] == sf.Keyboard.A:
                self.y_speed = -1
                self.x_speed = -2
                self.animations.play("walk_left")

            if event['code'] == sf.Keyboard.D:
                self.y_speed = 1
                self.x_speed = 2
                self.animations.play("walk_right")
        ''' 

#------------------------------------------------------------------------------

class Dialogable(object):                                                   
    def __init__(self,dialog_background='data/images/default_dialog_background.png',dialog_icon='data/images/default_dialog_icon.png',dialog_file="data/files/dialogs/default.json",label="default",name="Неизвестно"):
        self.dialog_background=dialog_background
        self.dialog_icon=dialog_icon
        self.dialog_file=dialog_file
        self.label = label
        self.name = name

#------------------------------------------------------------------------------

class Usable(object):                                                       
    def __init__(self,action):
        self.action=action

    def activate(self):
        exec(self.action)

#------------------------------------------------------------------------------

class NPC(Dialogable,sf.Sprite,Usable):                                     
    def __init__(self,config_file):
        with open(config_file) as data_file:    
            self.data = json.load(data_file)
        Dialogable.__init__(self,dialog_background=self.data['Dialog_background'],
                                  dialog_icon=self.data['Dialog_icon'],
                                  dialog_file=self.data['Dialog_file'],
                                  label=self.data['Dialog_label'],
                                  name=self.data['Name'])
        self.normal_texture = sf.Texture.from_file(self.data["Texture_file"])
        sf.Sprite.__init__(self,self.normal_texture)
        Usable.__init__(self,self.data['Action'])
        self.renderstate = sf.RenderStates()
        self.selected_texture = sf.Texture.from_file("data/images/test_succub_npc_selected.png")
        self.selected = False
        #self.activate()
        
    def draw(self, target, states):
        target.draw(self, self.renderstate)

    def update(self,player):
        if not self.selected:
            if player.magic_hand.position.x>self.position.x and player.magic_hand.position.y>self.position.y and player.magic_hand.position.x<self.position.x+self.texture.width and player.magic_hand.position.y<self.position.y+self.texture.height:
                self.selected = True
                self.texture = self.selected_texture
        
        else:
            player.usable_counter = self
            if not (player.magic_hand.position.x>self.position.x and player.magic_hand.position.y>self.position.y and player.magic_hand.position.x<self.position.x+self.texture.width and player.magic_hand.position.y<self.position.y+self.texture.height):
                self.selected = False
                self.texture = self.normal_texture

#------------------------------------------------------------------------------

class ButtonPool(sf.Drawable):                                              
    """docstring for ButtonPool"""

    def __init__(self,button):
        super(ButtonPool, self).__init__()
        self.buttons = []
        self.buttons.append(button)
        self.focused=0
        self.buttons[self.focused].focus()

    def __getitem__(self,key):
        return self.buttons[key]
        
    def addButton(self,button):
        self.buttons.append(button)

    def draw(self, target, states):
        for button in self.buttons:
            target.draw(button, states)

    def catchEvent(self,event):
        if event == sf.Event.KEY_PRESSED:
            if event['code'] in up_keys: 
                self.focused = self.focused-1
                if(self.focused<0):
                    self.focused = len(self.buttons)-1
                for button in self.buttons:
                    button.unfocus()
                self.buttons[self.focused].focus()

            elif event['code'] in down_keys:
                self.focused = self.focused+1
                if(self.focused>len(self.buttons)-1):
                    self.focused = 0
                for button in self.buttons:
                    button.unfocus()
                self.buttons[self.focused].focus()

            elif event['code'] in confirm_keys:
                self.buttons[self.focused].on_click()

#------------------------------------------------------------------------------

class Button(sf.Drawable):                                                  
    """docstring for Button"""

    def __init__(self, func = test_button_function, texture_path="data/texture.png",focused_texture_path="data/texture_focused.png",x=0,y=0):
        super(Button, self).__init__()
        self.focused = False
        self.texture = sf.Texture.from_file(texture_path)
        self.texture_focused = sf.Texture.from_file(focused_texture_path )
        self.sprite = sf.Sprite(self.texture)
        self.action = func
        self.setPosition(x,y)

    def bind_action(self,func):
        self.action=func

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def focus(self):
        self.sprite.texture = self.texture_focused 
        self.focused = True

    def unfocus(self):
        self.sprite.texture = self.texture
        self.focused = False

    def on_click(self):
        self.action()

    def setPosition(self,x,y):
        self.sprite.position = x,y

#------------------------------------------------------------------------------

class State(object):                                                        
    """docstring for State"""
    def __init__(self,name):
        super(State, self).__init__()
        #self.name = name
        #exec(open("data/"+name+".py").read(),globals())
        #on_init(self)

        self.scope = {}   
        exec(open("data/files/states/"+name+".py").read(),globals()  ,self.scope)
        locals().update(self.scope)
        self.scope['on_init'](self)
    
    def draw(self):
        self.scope['on_draw'](self)
        #on_draw(self)
        #exec(open("data/"+self.name+"_draw.py").read())
    def update(self):
        self.scope['on_update'](self)
        #on_update(self)
        #exec(open("data/"+self.name+"_update.py").read())
    def eventHandle(self):
        self.scope['on_event'](self)
        #on_event(self)
        #exec(open("data/"+self.name+"_event.py").read())

#---------------------------------------------------------------

class InventoryState(State):                                                
    """docstring for In"""
    def __init__(self, target):
        self.camera = sf.View()
        self.camera.reset([0,0,1280,800])
        window.view = self.camera
        self.texture = sf.Texture.create(window.size.x,window.size.y)
        self.texture.update(window);
        self.sprite = sf.Sprite(self.texture)
        self.background = sf.Sprite(sf.Texture.from_file("data/images/inventory_background.png"))
        codes = state_machine.states[len(state_machine.states)-1].player.inventory
        self.inventory = []
        for code in codes:
            self.inventory.append(InventoryObject(code))
        begin = {'x':355,'y':162}
        self.offset = 57
        group_by = 10
        counter = -1
        row = 0
        for c,obj in enumerate(self.inventory,0):
            counter+=1
            if counter >= 10:
                counter=0
                row+=1
            obj.sprite.position = [begin['x']+counter*self.offset,begin['y']+self.offset*row]
        
        self.info_table = sf.Text("",sf.Font.from_file("data/font.ttf"),20)
        self.cursor = sf.Sprite(sf.Texture.from_file("data/images/inventory_cursor.png"))
        self.cursor.position = [begin['x']-6,begin['y']-7]
        self.info_table.position = [begin['x']+self.offset,begin['y']+self.offset]
        self.cursor_target = 0
        #self.cursor.position = [self.inventory[self.cursor_target].position.x-6,self.inventory[self.cursor_target].position.y-8]
        try:
            self.info_table.string = self.inventory[0].description
        except Exception as e:
            print(e)

    def draw(self):
        window.clear()
        window.draw(self.sprite)
        window.draw(self.background)
        for obj in self.inventory:
            window.draw(obj)
        window.draw(self.cursor)
        window.draw(self.info_table)

    def update(self):
        pass

    def eventHandle(self):
        for event in window.events:
            if event == sf.Event.KEY_PRESSED:

                if event['code'] == sf.Keyboard.ESCAPE:
                    state_machine.removeThisState()   
                if event['code'] in right_keys:
                    try:
                        self.cursor_target+=1
                        self.cursor.position = [self.inventory[self.cursor_target].sprite.position.x-6,self.inventory[self.cursor_target].sprite.position.y-8]
                        self.info_table.string =self.inventory[self.cursor_target].description
                        self.info_table.position = [self.inventory[self.cursor_target].sprite.position.x+self.offset,self.inventory[self.cursor_target].sprite.position.y+self.offset]
                    except Exception as e:
                        print(e)
                        self.cursor_target-=1
                if event['code'] in left_keys:
                    try:
                        self.cursor_target-=1
                        if self.cursor_target<0:
                            self.cursor_target=0 
                        self.cursor.position = [self.inventory[self.cursor_target].sprite.position.x-6,self.inventory[self.cursor_target].sprite.position.y-8]
                        self.info_table.string =self.inventory[self.cursor_target].description
                        self.info_table.position = [self.inventory[self.cursor_target].sprite.position.x+self.offset,self.inventory[self.cursor_target].sprite.position.y+self.offset]
                    except Exception as e:
                        print(e)
                        self.cursor_target+=1
                if event['code'] in confirm_keys:
                    try:
                        self.inventory[self.cursor_target].activate()
                        self.inventory.pop(self.cursor_target)
                    except Exception as e:
                        print(e)
                if event['code'] in up_keys:
                    try:
                        self.cursor_target-=10
                        if self.cursor_target<0:
                            self.cursor_target+=10
                        self.cursor.position = [self.inventory[self.cursor_target].sprite.position.x-6,self.inventory[self.cursor_target].sprite.position.y-8]
                        self.info_table.string =self.inventory[self.cursor_target].description
                        self.info_table.position = [self.inventory[self.cursor_target].sprite.position.x+self.offset,self.inventory[self.cursor_target].sprite.position.y+self.offset]
                    except Exception as e:
                        print(e)
                if event['code'] in down_keys:
                    try:
                        self.cursor_target+=10
                        if self.cursor_target>=len(self.inventory):
                            self.cursor_target-=10
                        self.cursor.position = [self.inventory[self.cursor_target].sprite.position.x-6,self.inventory[self.cursor_target].sprite.position.y-8]
                        self.info_table.string =self.inventory[self.cursor_target].description
                        self.info_table.position = [self.inventory[self.cursor_target].sprite.position.x+self.offset,self.inventory[self.cursor_target].sprite.position.y+self.offset]
                    except Exception as e:
                        print(e)

#------------------------------------------------------------------------------

class InventoryObject(sf.Drawable,Usable):                                  
    """docstring for InventoryObject"""
    def __init__(self,obj_code):
        #super(InventoryObject, self).__init__()
        sf.Drawable.__init__(self)
        with open("data/files/configs/inventory_objects.json") as data_file:    
            data = json.load(data_file)
        for obj in data['inventory_objects']:
            if obj['obj_code'] == obj_code:
                data = obj
                break
        self.code = data['obj_code']
        Usable.__init__(self,data['action'])
        self.texture = sf.Texture.from_file("data/images/icons.png")
        self.sprite = sf.Sprite(self.texture)
        self.sprite.texture_rectangle = data['text_rect']
        self.description = data['description']

    def draw(self,target,states):
        target.draw(self.sprite)

#------------------------------------------------------------------------------

class Console(State):                                                       
    """docstring for Console"""
    log = sf.Text("",sf.Font.from_file("data/font.ttf"),20)

    def __init__(self):
        self.camera = sf.View()
        self.camera.reset([0,0,1280,800])
        window.view = self.camera
        self.texture = sf.Texture.create(window.size.x,window.size.y)
        self.texture.update(window);
        self.sprite = sf.Sprite(self.texture)
        self.rect = sf.RectangleShape()
        self.rect.position = 0,0
        self.rect.size = window.size.x,window.size.y/2
        self.rect.fill_color = sf.Color(30,30,30,200)
        self.text = sf.Text("",sf.Font.from_file("data/files/fonts/Bricks.otf"),20)
        self.ps1 = sf.Text("->: ",sf.Font.from_file("data/font.ttf"),20)
        self.ps1.position = 0,window.size.y/2-30
        self.text.position = 25,window.size.y/2-30
        self.shader = sf.Shader.from_file(fragment="data/blur.frag")
        self.shader.set_parameter("source")
        self.shader.set_parameter("offsetFactor",0.00075,0.00075)
        self.states = sf.RenderStates()
        self.states.shader = self.shader

    def draw(self):
        window.draw(self.sprite,self.states)
        window.draw(self.rect)
        window.draw(self.log)
        window.draw(self.ps1)
        window.draw(self.text)


    def update(self):
        pass

    def eventHandle(self):
        for event in window.events:
            if event == sf.Event.KEY_PRESSED and event['code'] == sf.Keyboard.ESCAPE or event == sf.Event.KEY_PRESSED and event['code'] == sf.Keyboard.TILDE:
                state_machine.removeThisState()
            elif event == sf.Event.KEY_PRESSED and event['code'] == sf.Keyboard.BACK_SPACE:
                self.text.string = self.text.string[:-1] 
            elif event == sf.Event.KEY_PRESSED and event['code'] == sf.Keyboard.F1:
                self.text.string += pyperclip.paste()
            elif event == sf.Event.KEY_PRESSED and event['code'] == sf.Keyboard.RETURN:
                try:
                    self.log.string += "->"+self.text.string+"\n"
                    exec(self.text.string)
                    result = "Sucsessful"
                except Exception as e:
                    result = e
                    print(e)
                self.text.string = ""
                self.log.string += str(result)+"\n"
            elif event == sf.Event.TEXT_ENTERED:
                if event['unicode'] != '\x08' and event['unicode']!='\r':
                    #print(self.text.string)
                    self.text.string += event['unicode']                    
                    #list1 = self.text.string
                    #list2 = list(list1)
                    #print (list2)
                    #list3 = list2[:-1]
                    #print(list3)

#------------------------------------------------------------------------------

class DialogButton(sf.Drawable):                                            
    """docstring for DialofButton"""
    def __init__(self,dialog,text,action):
        super(DialogButton,self).__init__()
        #self.sprite = #sf.Sprite(sf.Texture.from_file("data/texture.png"))
        self.text = sf.Text(text,sf.Font.from_file("data/font.ttf"))
        self.focused = False
        self.action = action
        self.text.color = sf.Color(133, 109, 48) 
        self.dialog = dialog

    def draw(self, target, states):
        #if self.focused:
        #target.draw(self.sprite, states)
        target.draw(self.text, states)

    def activate(self):
        
        exec(self.action)

#------------------------------------------------------------------------------

class Dialog(State):                                                        
    """docstring for Dialog"""

    def __init__(self,target):
        self.background_image = sf.Sprite(sf.Texture.from_file(target.dialog_background))
        self.dialog_icon = sf.Sprite(sf.Texture.from_file(target.dialog_icon))
        self.label = target.label
        self.next_label = self.label
        ### ATTENTION ^ BUG IF STRING IS EMPTY` 
        self.name = sf.Text(target.name,sf.Font.from_file("data/font.ttf"),40)
        self.name.position = 300, 475
        #self.name.string = target.name
        self.name.color = sf.Color(241, 213, 169)
        #self.dialog_file = target.dialog_file
        with open(target.dialog_file) as data_file:    
            self.data = json.load(data_file)
        #print(self.data[self.label])
        #self.font = sf.Font.from_file()
        self.text = sf.Text(self.data[self.label]['text'],sf.Font.from_file("data/font.ttf"),40)
        #self.text.string = self.data[self.label]['text']
        self.text.position = 500, 610
        self.text.color = sf.Color(45, 35, 18)
        self.answers=[]
        self.cursor = sf.RectangleShape()
        self.cursor.fill_color = sf.Color(30,40,50,60)
        self.cursor.size = 300,30
        self.cursor.position = 50,565
        self.loadAnswers()
        self.texture = sf.Texture.create(window.size.x,window.size.y)
        self.texture.update(window);
        self.sprite = sf.Sprite(self.texture)
        self.camera = sf.View()
        self.camera.reset([0,0,1280,800])
        window.view = self.camera



    def loadText(self):
        self.label = self.next_label
        self.text.string = self.data[self.label]['text']


    def loadAnswers(self):
        self.answers = []
        self.cursor.position = 50,565
        answers = [i for i in self.data[self.label]['answers']]
        #print(answers)
        for answer in answers:
            self.answers.append(DialogButton(self,answer['answer_text'],answer['action']))

        y=560-30
        for answer in self.answers:
            y+=30
            answer.text.position = 50, y

        for answer in self.answers:
            answer.focused = False
        self.answers[0].focused = True

    def draw(self):
        window.draw(self.sprite)
        window.draw(self.dialog_icon)
        window.draw(self.background_image)
        window.draw(self.cursor)
        window.draw(self.text)
        window.draw(self.name)
        for answer in self.answers:
            window.draw(answer)
            #print(answer.text)
    

    def update(self):
        pass

    def eventHandle(self):
        for event in window.events:
            default_event_handler(event)
            if event == sf.Event.KEY_PRESSED: 
                if event['code'] in down_keys:
                    try: 
                        for i in range(0,len(self.answers)):
                            if self.answers[i].focused == True:
                                self.answers[i+1].focused = True
                                self.answers[i].focused = False
                                break
                        self.cursor.position = self.cursor.position.x, self.cursor.position.y + 30
                    except Exception as e:
                        pass
                if event['code'] in up_keys:
                    try: 
                        for i in range(0,len(self.answers)):
                            if self.answers[i].focused == True:
                                if i == 0:
                                    self.answers[len(self.answers)].focused = True
                                self.answers[i-1].focused = True
                                self.answers[i].focused = False
                                break
                        self.cursor.position = self.cursor.position.x, self.cursor.position.y - 30
                    except Exception as e:
                        pass

                if event['code'] in confirm_keys:
                    for answer in self.answers:
                        if answer.focused:
                            answer.activate()
                    self.loadText()
                    self.loadAnswers()

    def closeDialog(self):
        state_machine.removeThisState()

#------------------------------------------------------------------------------

class PlayerInterface(sf.Drawable):                                         
    def __init__(self):
        super(PlayerInterface,self).__init__()
        self.healthline = sf.Sprite(sf.Texture.from_file("data/images/healthline.png"))
        self.healthbar = sf.Sprite(sf.Texture.from_file("data/images/healthbar3.png"))
        self.inventory = sf.Sprite(sf.Texture.from_file("data/images/fast_inventory.png"))


    def draw(self,target,states):
        target.draw(self.healthline)
        target.draw(self.healthbar)
        target.draw(self.inventory)

    def update(self,position):
        self.healthline.position = [position.x-window.size.x/2,position.y-window.size.y/2]
        self.healthbar.position = [position.x-window.size.x/2,position.y-window.size.y/2]
        self.inventory.position = [position.x-window.size.x/2,position.y-window.size.y/2]

#------------------------------------------------------------------------------

class StateMachine(object):                                                 
    """docstring for StateMachine"""
    states = []
    def __init__(self):
        super(StateMachine, self).__init__()

    def addState(self,state):
        self.states.append(state)
   
    def removeState(self):
        pass

    def removeThisState(self):
        clock.restart()
        self.states.pop()

    def setState(self,state):
        self.states.clear()
        self.states.append(state)

    def lastState(self):
        return self.states[len(self.states)-1]
    
    def eventHandle(self):
        #for state in self.states:
            #state.eventHandle()
        self.states[len(self.states)-1].eventHandle()

    def update(self):
        #for state in self.states:
            #state.update()
        self.states[len(self.states)-1].update()
    
    def draw(self):
        for state in self.states:
            state.draw()
        window.display()

#------------------------------------------------------------------------------

class GameObject(sf.Drawable,Usable):                                       
    """docstring for GameObject"""
    def __init__(self,config_file="data/files/configs/test_game_object.json",position=[0,0]):
        super(GameObject, self).__init__()
        self.transparent    = False
        self.solid          = False
        self.usable         = False
        self.is_solid       = False
        self.is_transparent = False
        self.is_usable      = False
        with open(config_file) as data_file:    
            data = json.load(data_file)
        self.texture = sf.Texture.from_file(data['texture'])
        self.sprite = sf.Sprite(self.texture)
        
        if data['is_solid']=="true":
            self.solid = True
            self.is_solid = False
            self.x_solid  = data['x_solid']
            self.y_solid  = data['y_solid']
        else:
            self.solid = False
        
        if data['is_transparent']=="true":
            self.transparent = True
            self.is_transparent = False
            self.x_transparent  = data["x_transparent"]
            self.y_transparent  = data["y_transparent"]
            self.transparent_texture = sf.Texture.from_file(data['transparent_texture'])
        else:
            self.is_transparent = False
     
        try:
            if data['is_usable']=="true":
                self.usable = True
                self.is_usable = False
                self.x_usable  = data['x_usable']
                self.y_usable  = data['y_usable']
                self.usable_texture = sf.Texture.from_file(data['usable_texture'])
                Usable.__init__(self,data['action'])
            else:
                self.usable = False
        except Exception as e:
            pass
            #print(config_file[19::] + " -> hasn't field 'is_usable'")

        self.setPosition(*position)


    def update(self,player,time):
        x_pos = player.sprite.position.x
        y_pos = player.sprite.position.y
        if self.transparent:
            if inPolygon(x_pos,y_pos,self.x_transparent,self.y_transparent):
                if  self.is_transparent == False:
                    self.is_transparent = True
                    self.sprite.texture = self.transparent_texture
                    self.sprite.color = sf.Color(255,255,255,125)
            else:
                if  self.is_transparent == True:
                    self.is_transparent = False
                    self.sprite.texture = self.texture
                    self.sprite.color = sf.Color(255,255,255,255)
        if self.solid:
            if inPolygon(x_pos,y_pos,self.x_solid,self.y_solid):
                player.sprite.move([player.x_speed*time*player.movespeed*(-1),player.y_speed*time*player.movespeed*(-1)])

        x_pos = player.magic_hand.position.x
        y_pos = player.magic_hand.position.y

        if self.usable:
            if inPolygon(x_pos,y_pos,self.x_usable,self.y_usable):
                if not self.is_usable:
                    self.is_usable = True
                    self.sprite.texture = self.usable_texture
                player.usable_counter = self
            else:
                if self.is_usable:
                    self.is_usable = False
                    self.sprite.texture = self.texture

    def draw(self,target,states):
        target.draw(self.sprite)
        if debug_mode:
            if self.usable:
                lines = sf.VertexArray(len(self.x_usable)-1,sf.PrimitiveType.POINTS)
                #lines = []
                for x,y in zip(self.x_usable,self.y_usable):
                    lines.append(sf.Vertex([x,y],sf.Color.RED))
                window.draw(lines)

    def setPosition(self,x_p,y_p):
        self.sprite.position = [x_p,y_p]
        if self.solid:
            self.x_solid = [x+x_p for x in self.x_solid]
            self.y_solid = [y+y_p for y in self.y_solid]
        if self.transparent:
            self.x_transparent = [x+x_p for x in self.x_transparent]
            self.y_transparent = [y+y_p for y in self.y_transparent]
        if self.usable:
            self.x_usable = [x+x_p for x in self.x_usable]
            self.y_usable = [y+y_p for y in self.y_usable]

    def move(self,x_offset,y_offset):
        self.sprite.position = [self.sprite.position.x+x_offset,self.sprite.position.y+y_offset]
        if self.solid:
            self.x_solid = [x+x_offset for x in self.x_solid]
            self.y_solid = [y+y_offset for y in self.y_solid]
        if self.transparent:
            self.x_transparent = [x+x_offset for x in self.x_transparent]
            self.y_transparent = [y+y_offset for y in self.y_transparent]
        if self.usable:
            self.x_usable = [x+x_offset for x in self.x_usable]
            self.y_usable = [y+y_offset for y in self.y_usable]

#------------------------------------------------------------------------------

class Level(sf.Drawable):                                                   
    """docstring for Level"""
    def __init__(self, config_file="data/files/levels/test_level.json"):
        super(Level, self).__init__()
        with open(config_file) as data_file:    
            self.data = json.load(data_file)
        self.name = self.data['level_name']
        self.game_objects = []
        self.npcs = []
        self.loot  = []
        self.usable = []
        for g_object in self.data['game_objects']:
            self.game_objects.append(GameObject(g_object['object'],position=g_object['position']))
        for f_npc in self.data['npc']:
            self.npcs.append(NPC(f_npc))

        self.floating_name = sf.Text(self.name,sf.Font.from_file("data/files/fonts/Bricks.otf"),100)
        self.time_of_text_live = 250
        #self.revers
        #self.game_objects[1].move(800,0)
        #        try:
        #              self.game_objects[2].setPosition(400,0)
        #        except Exception as e:
        #            print(e)

    def draw(self, target, states):
        for g_object in self.game_objects:
            if not g_object.is_transparent:
                target.draw(g_object)
        for npc in self.npcs:
            target.draw(npc)

    def draw_transparent(self):
        for g_object in self.game_objects:
            if g_object.is_transparent:
                window.draw(g_object)
        if self.time_of_text_live > 0:
            window.draw(self.floating_name)

    def update(self,player,time):
        player.usable_counter = None
        for g_object in self.game_objects:
            g_object.update(player,time)
        for npc in self.npcs:
            npc.update(player)
        if self.time_of_text_live > 0:
            self.time_of_text_live -= 2
            self.floating_name.color = sf.Color(255,255,255,self.time_of_text_live)
            self.floating_name.position = player.sprite.position.x-window.size.x/5,player.sprite.position.y-window.size.y/3

    def load(self,config_file):
        sprite = sf.Sprite(sf.Texture.from_file("data/images/loading.png"))
        window.clear()
        window.draw(sprite)
        window.display()
        self.time_of_text_live = 250
        with open(config_file) as data_file:    
            self.data = json.load(data_file)
        self.name = self.data['level_name']
        self.game_objects.clear()
        self.usable.clear()
        self.npcs.clear()
        self.loot.clear()
        for g_object in self.data['game_objects']:
            self.game_objects.append(GameObject(g_object['object'],position=g_object['position']))
        for f_npc in self.data['npc']:
            self.npcs.append(NPC(f_npc))
        self.floating_name = sf.Text(self.name,sf.Font.from_file("data/files/fonts/Bricks.otf"),100)
        self.time_of_text_live = 250

#------------------------------------------------------------------------------

state_machine = StateMachine()
