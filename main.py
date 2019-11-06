import kivy

from kivmob import KivMob, TestIds
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewLabel

class KivMobTest(App):
    
    def build(self):
        self.ads = KivMob(TestIds.APP)
        self.ads.new_interstitial(TestIds.INTERSTITIAL)
        self.ads.request_interstitial()
        return Button(text='Show Interstitial',
                      on_release=lambda a:self.ads.show_interstitial())
                      
    def on_resume(self):
        self.ads.request_interstitial()

KivMobTest().run()
