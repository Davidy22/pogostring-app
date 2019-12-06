from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.factory import Factory
from kivy.garden.navigationdrawer import NavigationDrawer
from kivmob import KivMob, TestIds

from functools import partial
from src.parse import *
import json	
	
class removeAds(StackLayout):
	def __init__(self, **kwargs):
		super(removeAds, self).__init__(**kwargs)
	

class stringManipulation(TabbedPanel):
	def __init__(self, **kwargs):
		super(stringManipulation, self).__init__(**kwargs)
		f = open("dump.json")
		self.pokemonData = json.load(f)
		self.orientation = "lr-tb"

		self.default_tab_text = "Pokemon"
		options = TabbedPanelItem(text = "Options")
		io = TabbedPanelItem(text = "Import/Export")
		bulk = TabbedPanelItem(text = "Bulk select")
		self.add_widget(options)
		self.add_widget(io)
		self.add_widget(bulk)
		
		
		pScroll = ScrollView()
		oScroll = ScrollView()
		options.add_widget(oScroll)
		iScroll = ScrollView()
		io.add_widget(iScroll)
		bScroll = ScrollView()
		bulk.add_widget(bScroll)
		
		self.size_hint=(1, None)
		self.size=(Window.width, Window.height)
		
		# Pokemon tab
		pokemonScreen = StackLayout()
		self.default_tab_content = pokemonScreen
		regions = ScrollView(size_hint_y = None)
		regions.height = 80
		regions.do_scroll_y = False
		regions.do_scroll_x = True
		regionBar = GridLayout(rows = 1)
		regions.add_widget(regionBar)
		
		pokemonList = GridLayout(cols = 5, size_hint_y = None)
		gen = 0
		for i in self.pokemonData:
			button = Factory.Pokemon(size_hint_y = None)
			button.image_source = "images/"+i+".png"
			button.subtext = self.pokemonData[i]["name"]
			button.background_disabled_normal = ""
			button.background_disabled_down = ""
			button.background_normal = ""
			button.pid = i
			self.pokemonData[i]["button"] = button
			button.bind(on_press = self.pokemonPressed)
			pokemonList.add_widget(button)
			
			if gen < self.pokemonData[i]["gen"]:
				gen = self.pokemonData[i]["gen"]
				self.addRegionButton(pScroll, regionBar, "Gen %d" % gen, gen, button)
			
			button.background_color = (0.4 + 0.6*(gen/7), 1 - 0.6*(gen/7), 0.5, 1)

		self.lastPokemon = button
		pokemonList.bind(minimum_height=pokemonList.setter('height'))
		pokemonScreen.add_widget(regions)
		pokemonScreen.add_widget(pScroll)
		pScroll.add_widget(pokemonList)

		# IO tab
		ioList = StackLayout(size_hint_y = None)
		self.imp = TextInput()
		ioList.add_widget(self.imp)
		inControls = GridLayout(cols = 4, size_hint_y = None)
		importButton = Button(text = "Import")
		importButton.bind(on_press = self.importString)
		addButton = Button(text = "Add")
		importButton.bind(on_press = self.addString)
		subtractButton = Button(text = "Subtract")
		importButton.bind(on_press = self.subtractString)
		invertButton = Button(text = "Invert")
		importButton.bind(on_press = self.invertString)
		inControls.add_widget(importButton)
		inControls.add_widget(addButton)
		inControls.add_widget(subtractButton)
		inControls.add_widget(invertButton)
		ioList.add_widget(inControls)
		ioList.add_widget(GridLayout(height = 5))
		self.exp = TextInput()
		ioList.add_widget(self.exp)
		exportButton = Button(text = "Copy")
		exportButton.bind(on_press = lambda x: Clipboard.copy(self.exp.text))
		ioList.add_widget(exportButton)
		iScroll.add_widget(ioList)
		
		# Bulk tab
		bulkList = StackLayout(size_hint_y = None)
		bulkList.add_widget(Label(text = "Quick Select"))
		quickSelect = GridLayout(cols = 4, size_hint_y = None)
		self.bulkSelectButton(quickSelect, "All", self.switchAll, True)
		self.bulkSelectButton(quickSelect, "Stage one", self.switchStage, True, 1)
		self.bulkSelectButton(quickSelect, "Stage two", self.switchStage, True, 2)
		self.bulkSelectButton(quickSelect, "Stage three", self.switchStage, True, 3)
		self.bulkSelectButton(quickSelect, "Baby", self.switchTag, True, "baby")
		self.bulkSelectButton(quickSelect, "Can evolve", self.switchTag, True, "can-evolve")
		self.bulkSelectButton(quickSelect, "12 candy", self.switchTag, True, "12-candy")
		self.bulkSelectButton(quickSelect, "25 candy", self.switchTag, True, "25-candy")
		self.bulkSelectButton(quickSelect, "50 candy", self.switchTag, True, "50-candy")
		self.bulkSelectButton(quickSelect, "100 candy", self.switchTag, True, "100-candy")
		self.bulkSelectButton(quickSelect, "400 candy", self.switchTag, True, "400-candy")
		self.bulkSelectButton(quickSelect, "Legendary", self.switchTag, True, "legendary")
		self.bulkSelectButton(quickSelect, "Mythical", self.switchTag, True, "mythical")
		bulkList.add_widget(quickSelect)
		
		bulkList.add_widget(Label(text = "Quick Deselect"))
		quickDeselect = GridLayout(cols = 4, size_hint_y = None)
		self.bulkSelectButton(quickDeselect, "All", self.switchAll, False)
		self.bulkSelectButton(quickDeselect, "Stage one", self.switchStage, False, 1)
		self.bulkSelectButton(quickDeselect, "Stage two", self.switchStage, False, 2)
		self.bulkSelectButton(quickDeselect, "Stage three", self.switchStage, False, 3)
		self.bulkSelectButton(quickDeselect, "Baby", self.switchTag, False, "baby")
		self.bulkSelectButton(quickDeselect, "Can evolve", self.switchTag, False, "can-evolve")
		self.bulkSelectButton(quickDeselect, "12 candy", self.switchTag, False, "12-candy")
		self.bulkSelectButton(quickDeselect, "25 candy", self.switchTag, False, "25-candy")
		self.bulkSelectButton(quickDeselect, "50 candy", self.switchTag, False, "50-candy")
		self.bulkSelectButton(quickDeselect, "100 candy", self.switchTag, False, "100-candy")
		self.bulkSelectButton(quickDeselect, "400 candy", self.switchTag, False, "400-candy")
		self.bulkSelectButton(quickDeselect, "Legendary", self.switchTag, False, "legendary")
		self.bulkSelectButton(quickDeselect, "Mythical", self.switchTag, False, "mythical")
		bulkList.add_widget(quickDeselect)
		
		bScroll.add_widget(bulkList)
		
		# Options tab
		optionsList = GridLayout(cols = 3, size_hint_y = None)
		oScroll.add_widget(optionsList)
	
	def pokemonPressed(self, button):
		selected = []
		for pokemonID in self.pokemonData:
			if self.pokemonData[pokemonID]["button"].state == "down":
				selected.append(pokemonID)
		self.exp.text = condense(selected)

	def importString(self, button):
		parsedList = parse(self.imp.text)
		parsedList = [str(i) for i in parsedList]
		for pokemonID in self.pokemonData:
			if pokemonID in parsedList:
				self.pokemonData[pokemonID]["button"].state = "down"
			else:
				self.pokemonData[pokemonID]["button"].state = "normal"
		self.switch_to(self.tab_list[3])

	def addString(self, button):
		parsedList = parse(self.imp.text)
		parsedList = [str(i) for i in parsedList]
		for pokemonID in parsedList:
			self.pokemonData[pokemonID]["button"].state = "down"
		self.switch_to(self.tab_list[3])

	def subtractString(self, button):
		parsedList = parse(self.imp.text)
		parsedList = [str(i) for i in parsedList]
		for pokemonID in parsedList:
			self.pokemonData[pokemonID]["button"].state = "normal"
		self.switch_to(self.tab_list[3])

	def invertString(self, button):
		for pokemonID in self.pokemonData:
			if self.pokemonData[pokemonID]["button"].state == "down":
				self.pokemonData[pokemonID]["button"].state = "normal"
			else:
				self.pokemonData[pokemonID]["button"].state = "down"
		self.switch_to(self.tab_list[3])
	
	def switchAll(self, *args):
		# True = Select, False = Deselect
		for pokemonID in self.pokemonData:
			if args[0] == True:
				self.pokemonData[pokemonID]["button"].state = "down"
			else:
				self.pokemonData[pokemonID]["button"].state = "normal"
		self.switch_to(self.tab_list[3])
		
	def switchStage(self, *args):
		# True = Select, False = Deselect
		if args[0] == True:
			targetState = "down"
		else:
			targetState = "normal"
		stage = args[1]
		for pokemonID in self.pokemonData:
			if stage == self.pokemonData[pokemonID]["stage"]:
				self.pokemonData[pokemonID]["button"].state = targetState
		self.switch_to(self.tab_list[3])
	
	def switchTag(self, *args):
		# True = Select, False = Deselect
		if args[0] == True:
			targetState = "down"
		else:
			targetState = "normal"
		tag = args[1]
		for pokemonID in self.pokemonData:
			if tag in self.pokemonData[pokemonID]["keywords"]:
				self.pokemonData[pokemonID]["button"].state = targetState
		self.switch_to(self.tab_list[3])
	
	def bulkSelectButton(self, buttonParent, buttonText, buttonFunction, mode, param = None):
		temp = Button(text = buttonText)
		if param is None:
			temp.bind(on_press = lambda x : buttonFunction(mode))
		else:
			temp.bind(on_press = lambda x : buttonFunction(mode, param))
		buttonParent.add_widget(temp)
	
	def addRegionButton(self, scrollview, bar, name, number, scrollto):
		temp = Button(text = name)
		def tempScroll(x):
			scrollview.scroll_to(scrollto)
		temp.bind(on_press = tempScroll)
		bar.add_widget(temp)

class screens(ScreenManager):
	def __init__(self, **kwargs):
		super(screens, self).__init__(**kwargs)
		startScreen = Screen(name = "start")
		buyScreen = Screen(name = "buy")
		startScreen.add_widget(stringManipulation())
		buyScreen.add_widget(removeAds())
		self.add_widget(startScreen)
		self.add_widget(buyScreen)
	

class main(NavigationDrawer):
	def __init__(self, **kwargs):
		super(main, self).__init__(**kwargs)
		self.menu = GridLayout(cols = 1)
		self.appBody = screens()
		self.addMenuButton("Edit string", "start")
		self.addMenuButton("Remove ads", "buy")
		self.add_widget(self.menu)
		self.add_widget(self.appBody)
		self.ads = KivMob(TestIds.APP)
		self.ads.new_banner(TestIds.BANNER, top_pos=False)
		self.ads.request_banner()
		self.ads.show_banner()
	
	def addMenuButton(self, text, goto):
		temp = Button(text = text, height = 10)
		temp.bind(on_press = (lambda x : self.switchScreen(goto)))
		self.menu.add_widget(temp)
	
	def switchScreen(self, dest):
		self.appBody.current = dest
	


class pogostring(App):

	def build(self):
		return main()


if __name__ == '__main__':
	pogostring().run()
