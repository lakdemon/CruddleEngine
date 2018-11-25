def on_init(self):
	sprite = sf.Sprite(sf.Texture.from_file("data/images/loading.png"))
	window.clear()
	window.draw(sprite)
	window.display()
	#time.sleep(5)
	#self.sprite = sf.Sprite(sf.Texture.from_file("data/testmap.jpg"))
	self.one = 0
	self.level = Level("data/files/levels/first_room.json")
	self.interface = PlayerInterface()
	self.camera = sf.View()
	self.camera.reset([0,0,1280,800])
	clock.restart()
	self.player = Player()
	
	self.shader = sf.Shader.from_file(fragment="data/blur.frag")
	self.shader.set_parameter("source")
	#self.param1 = 0.0003
	#self.param2 = 0.0003
	self.shader.set_parameter("offsetFactor",0.0003,0.0003)
	self.renderstates = sf.RenderStates()
	self.renderstates.shader = self.shader
	self.texture = sf.Texture.create(window.size.x,window.size.y)
	self.texture.update(window);
	self.sprite = sf.Sprite(self.texture)
	self.filter = sf.Sprite(sf.Texture.from_file("data/images/filter.png"))
	#self.test_npc = NPC("data/files/npc/testnpc.json")
	QuestSystem.addQuest("data/files/quests/testquest.py")


def on_event(self):
	for event in window.events:
		default_event_handler(event)
		self.player.event_handler(event)
		if event == sf.Event.KEY_PRESSED:
			if event['code'] == sf.Keyboard.ESCAPE:
				state_machine.addState(State("game_menu"))
			if event['code'] == sf.Keyboard.LEFT:
				print("STATE")
				state_machine.addState(State("quests_state"))
		if event == sf.Event.LOST_FOCUS:
			state_machine.addState(State("game_menu"))
		#if event == sf.Event.RESIZED:
		#	self.camera.reset([0, 0, event['width'],event['height']])
		#	window.view = self.camera
    

def on_draw(self):
	window.clear(sf.Color(0, 121, 57))
	#window.clear(sf.Color(25,25,25))
	#window.draw(self.sprite)
	window.draw(self.level)
	#window.draw(self.test_npc)
	window.draw(self.player)
	self.level.draw_transparent()
	window.draw(self.interface)
	window.draw(self.filter)
	#window.display()
	#window.clear()
	self.texture.update(window);
	#self.sprite.texture=self.texture
	window.draw(self.sprite,self.renderstates)



def on_update(self):
	#self.param1 += random.uniform(-0.0003,0.0003)
	#self.param2 += random.uniform(-0.0003,0.0003)
	#self.shader.set_parameter("offsetFactor",self.param1,self.param2)
	#self.renderstates.shader = self.shader

	time = clock.elapsed_time.seconds
	clock.restart()
	time = time*600
	self.player.update(time)
	self.level.update(self.player,time)
	self.camera.reset([self.player.sprite.position.x-window.size.x/2, self.player.sprite.position.y-window.size.y/2, *self.camera.size])
	window.view=self.camera
	self.interface.update(self.camera.center)
	#self.level.update(self.player,time)

	self.filter.position = self.sprite.position = [self.player.sprite.position.x-window.size.x/2, self.player.sprite.position.y-window.size.y/2]
	

	#self.level.update(sf.Mouse.get_position(window).x,sf.Mouse.get_position(window).y)
	#pass
	#window.view = self.camera
	#if self.level.solids[0].isInside(sf.Mouse.get_position(window).x,sf.Mouse.get_position(window).y):
	#	pass
		#print("inside")
	#else:
	#	pass
		#print("not inside") 