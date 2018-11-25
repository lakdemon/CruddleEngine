def on_init(self):
	self.finished = False
	self.questID = 0
	self.questName = "Начало"
	self.description = "Поговорить с отцом"

def on_update(self,signal,sender,reciver):
	if signal == SIGNAL.DIALOGENDED:
		#if reciver.name == "отец":
		self.complete()

def on_complete(self):
	self.finish()

def on_finish(self):
	self.finished = True
	state_machine.states[len(state_machine.states)-1].level.game_objects[1].setAction("state_machine.lastState().level.load('data/files/levels/test_level.json') or PLAYER().moveTo(300,300)")

