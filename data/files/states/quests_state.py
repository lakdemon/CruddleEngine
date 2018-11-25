

def on_init(self):
	self.quests = []
	for quest in QuestSystem.quests:
		self.quests.append(sf.Text(quest.questName,sf.Font.from_file("data/font.ttf"),20))
	self.texture = sf.Texture.create(window.size.x,window.size.y)
	self.texture.update(window);
	self.sprite = sf.Sprite(self.texture)
	self.camera = sf.View()
	self.camera.reset([0,0,1280,800])
	self.shader = sf.Shader.from_file(fragment="data/blur.frag")
	self.shader.set_parameter("source")
	self.shader.set_parameter("offsetFactor",0.001,0.001)
	self.states = sf.RenderStates()
	self.states.shader = self.shader
	self.rect = sf.RectangleShape()
	self.rect.fill_color = sf.Color(0,0,0,200)
	self.rect.size = window.size.x, window.size.y
	#self.buttons[1].bind_action(lambda : state_machine.addState(Dialog(Dialogable(dialog_icon="data/dialog_icon.png",dialog_file="data/files/dialogs/succubus.json",label='test_label',name='Суккуб'))))
	window.view = self.camera

def on_event(self):
	for event in window.events:
		default_event_handler(event)
		if event == sf.Event.KEY_PRESSED:
			if event['code'] == sf.Keyboard.ESCAPE:
				state_machine.removeThisState()


def on_draw(self): 
	window.clear()
	window.draw(self.sprite,self.states)
	window.draw(self.rect)
	for text in self.quests:
		window.draw(text)
	

def on_update(self):
	pass