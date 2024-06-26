from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import FileSharer
import time
import os
from kivy.core.clipboard import Clipboard
import webbrowser

Builder.load_file('frontend.kv')


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


class CameraScreen(Screen):
    def start(self):
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera.opacity = 1


    def stop(self):
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        if not os.path.exists("files"):
            os.makedirs("files")
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f"files/{current_time}.png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = "Create a Link First!"
    def create_link(self):
        try:
            file_path = App.get_running_app().root.ids.camera_screen.filepath
            # fileshare = FileSharer(filepath=file_path)
            self.url = "filestack.com" # fileshare.share()
            self.ids.link.text = self.url
        except:
            self.ids.link.text = "Error"

    def copy_link(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


MainApp().run()
