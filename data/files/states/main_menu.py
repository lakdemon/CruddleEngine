def on_init(self):
	self.buttons = ButtonPool(Button(func=begin_game,texture_path="data/begin_button.png",focused_texture_path="data/begin_button_focused.png"))
	self.buttons.addButton(Button(texture_path="data/loadgame_button.png",focused_texture_path="data/loadgame_button_focused.png"))
	self.buttons.addButton(Button(texture_path="data/options_button.png",focused_texture_path="data/options_button_focused.png"))
	self.buttons.addButton(Button(texture_path="data/info_button.png",focused_texture_path="data/info_button_focused.png"))
	self.buttons.addButton(Button(func=close_window,texture_path="data/exit_button.png",focused_texture_path="data/exit_button_focused.png"))
	self.buttons_back_tex = sf.Texture.from_file("data/main_menu_buttonback4.png")
	self.background_tex = sf.Texture.from_file("data/main_menu.jpg")
	self.background = sf.Sprite(self.background_tex)
	self.buttons_back = sf.Sprite(self.buttons_back_tex)
	self.logo = sf.Sprite(sf.Texture.from_file("data/logo.png"))
	self.camera = sf.View()
	self.camera.reset([0,0,1280,800])
	window.view = self.camera

def on_event(self):
	for event in window.events:
		default_event_handler(event)
		self.buttons.catchEvent(event)

def on_draw(self):
	window.clear()
	window.draw(self.background)
	window.draw(self.buttons_back)
	window.draw(self.buttons)
	window.draw(self.logo)

def on_update(self):
	pass


#background x from 125 to 500 and y from 0 to 800
#