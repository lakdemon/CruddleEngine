

def on_init(self):
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
	self.background = sf.Sprite(sf.Texture.from_file("data/game_menu_back.png"))
	self.buttons = ButtonPool(Button(texture_path="data/game_menu_button1.png",focused_texture_path="data/game_menu_button1_focused.png"))
	self.buttons.addButton(Button(texture_path="data/game_menu_button2.png",focused_texture_path="data/game_menu_button2_focused.png"))
	self.buttons.addButton(Button(texture_path="data/game_menu_button3.png",focused_texture_path="data/game_menu_button3_focused.png"))
	self.buttons[0].bind_action(lambda : state_machine.removeThisState())
	self.buttons[2].bind_action(lambda : state_machine.setState(State("main_menu")))
	#self.buttons[1].bind_action(lambda : state_machine.addState(Dialog(Dialogable(dialog_icon="data/dialog_icon.png",dialog_file="data/files/dialogs/succubus.json",label='test_label',name='Суккуб'))))
	window.view = self.camera

def on_event(self):
	for event in window.events:
		default_event_handler(event)
		self.buttons.catchEvent(event)
		if event == sf.Event.KEY_PRESSED:
			if event['code'] == sf.Keyboard.ESCAPE:
				state_machine.removeThisState()


def on_draw(self):
	window.clear()
	window.draw(self.sprite,self.states)
	window.draw(self.rect)
	window.draw(self.background)
	window.draw(self.buttons)
	

def on_update(self):
	pass