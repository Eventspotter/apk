from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.metrics import dp
import json
import os

# Set default window size for mobile preview
Window.size = (360, 640)

class MainMenuScreen(Screen):
    pass

class SignUpScreen(Screen):
    def validate_signup(self):
        username = self.ids.username_input.text.strip()
        password1 = self.ids.password_input.text.strip()
        password2 = self.ids.repassword_input.text.strip()
        
        if not username or not password1 or not password2:
            self.show_popup("Error", "All fields are required!")
            return False
        
        if len(username) < 4:
            self.show_popup("Error", "Username must be at least 4 characters!")
            return False
            
        if len(password1) < 6:
            self.show_popup("Error", "Password must be at least 6 characters!")
            return False
            
        if password1 != password2:
            self.show_popup("Error", "Passwords don't match!")
            return False
            
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                users = json.load(f)
                if username in users:
                    self.show_popup("Error", "Username already exists!")
                    return False
        else:
            users = {}
            
        users[username] = {
            "password": password1,
            "profile": None
        }
        
        with open("users.json", "w") as f:
            json.dump(users, f)
            
        self.manager.current = 'create_profile'
        self.manager.get_screen('create_profile').username = username
        return True
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message, color=(0, 0, 0, 1)))
        
        btn = Button(text="OK", size_hint=(1, None), height=dp(50))
        btn.background_color = (0.2, 0.6, 1, 1)
        content.add_widget(btn)
        
        popup = Popup(title=title,
                      content=content,
                      size_hint=(0.8, 0.4),
                      separator_color=(0.2, 0.6, 1, 1))
        
        btn.bind(on_press=popup.dismiss)
        popup.open()

class LoginScreen(Screen):
    def validate_login(self):
        username = self.ids.login_username.text.strip()
        password = self.ids.login_password.text.strip()
        
        if not username or not password:
            self.show_popup("Error", "Both fields are required!")
            return False
            
        if not os.path.exists("users.json"):
            self.show_popup("Error", "No users registered yet!")
            return False
            
        with open("users.json", "r") as f:
            users = json.load(f)
            if username not in users:
                self.show_popup("Error", "Username not found!")
                return False
                
            if users[username]["password"] != password:
                self.show_popup("Error", "Incorrect password!")
                return False
                
        self.show_user_profile(username, users[username])
        return True
    
    def show_user_profile(self, username, user_data):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        header = BoxLayout(size_hint=(1, None), height=dp(50))
        header.add_widget(Label(text=f"Welcome {username}!", font_size='20sp', bold=True))
        content.add_widget(header)
        
        if user_data["profile"] and "image" in user_data["profile"]:
            img_container = BoxLayout(size_hint=(1, None), height=dp(150))
            image = Image(source=user_data["profile"]["image"], size_hint=(None, None), size=(dp(120), dp(120)))
            img_container.add_widget(image)
            content.add_widget(img_container)
        
        info_box = BoxLayout(orientation='vertical', spacing=dp(5))
        if user_data["profile"]:
            for key, value in user_data["profile"].items():
                if key != "image":
                    info_box.add_widget(Label(text=f"[b]{key.title()}:[/b] {value}", markup=True))
        
        scroll = ScrollView()
        scroll.add_widget(info_box)
        content.add_widget(scroll)
        
        close_btn = Button(text="Close", size_hint=(1, None), height=dp(50))
        close_btn.background_color = (0.2, 0.6, 1, 1)
        content.add_widget(close_btn)
        
        popup = Popup(title="Your Profile",
                      content=content,
                      size_hint=(0.9, 0.8),
                      separator_color=(0.2, 0.6, 1, 1))
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message, color=(0, 0, 0, 1)))
        
        btn = Button(text="OK", size_hint=(1, None), height=dp(50))
        btn.background_color = (0.2, 0.6, 1, 1)
        content.add_widget(btn)
        
        popup = Popup(title=title,
                      content=content,
                      size_hint=(0.8, 0.4),
                      separator_color=(0.2, 0.6, 1, 1))
        
        btn.bind(on_press=popup.dismiss)
        popup.open()

class CreateProfileScreen(Screen):
    username = StringProperty("")
    
    def capture_selfie(self):
        self.show_popup("Info", "Selfie captured! (simulated)")
        return "assets/default_avatar.png"
    
    def save_profile(self):
        name = self.ids.name_input.text.strip()
        age = self.ids.age_input.text.strip()
        email = self.ids.email_input.text.strip()
        
        if not name:
            self.show_popup("Error", "Name is required!")
            return False
            
        selfie_path = self.capture_selfie()
        
        with open("users.json", "r") as f:
            users = json.load(f)
            
        users[self.username]["profile"] = {
            "image": selfie_path,
            "name": name,
            "age": age,
            "email": email
        }
        
        with open("users.json", "w") as f:
            json.dump(users, f)
            
        self.show_popup("Success", "Profile saved successfully!")
        self.manager.current = 'main_menu'
        return True
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=message, color=(0, 0, 0, 1)))
        
        btn = Button(text="OK", size_hint=(1, None), height=dp(50))
        btn.background_color = (0.2, 0.6, 1, 1)
        content.add_widget(btn)
        
        popup = Popup(title=title,
                      content=content,
                      size_hint=(0.8, 0.4),
                      separator_color=(0.2, 0.6, 1, 1))
        
        btn.bind(on_press=popup.dismiss)
        popup.open()

class ScreenManagement(ScreenManager):
    pass

Builder.load_string('''
<MainMenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        
        Label:
            text: 'INFO-PROTO'
            font_size: 30
            size_hint_y: None
            height: 50
            
        Button:
            text: 'Sign Up'
            font_size: 20
            on_press: root.manager.current = 'signup'
            
        Button:
            text: 'Login'
            font_size: 20
            on_press: root.manager.current = 'login'

<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15
        
        Label:
            text: 'Create Account'
            font_size: 25
            size_hint_y: None
            height: 40
            
        TextInput:
            id: username_input
            hint_text: 'Username'
            size_hint_y: None
            height: 40
            
        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: 40
            
        TextInput:
            id: repassword_input
            hint_text: 'Re-enter Password'
            password: True
            size_hint_y: None
            height: 40
            
        Button:
            text: 'Sign Up'
            size_hint_y: None
            height: 50
            on_press: root.validate_signup()
            
        Button:
            text: 'Back'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'main_menu'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15
        
        Label:
            text: 'Login'
            font_size: 25
            size_hint_y: None
            height: 40
            
        TextInput:
            id: login_username
            hint_text: 'Username'
            size_hint_y: None
            height: 40
            
        TextInput:
            id: login_password
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: 40
            
        Button:
            text: 'Login'
            size_hint_y: None
            height: 50
            on_press: root.validate_login()
            
        Button:
            text: 'Back'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'main_menu'

<CreateProfileScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        
        Label:
            text: 'Create Your Profile'
            font_size: 25
            size_hint_y: None
            height: 40
            
        Button:
            text: 'Take Selfie'
            size_hint_y: None
            height: 50
            on_press: root.capture_selfie()
            
        TextInput:
            id: name_input
            hint_text: 'Full Name'
            size_hint_y: None
            height: 40
            
        TextInput:
            id: age_input
            hint_text: 'Age'
            input_filter: 'int'
            size_hint_y: None
            height: 40
            
        TextInput:
            id: email_input
            hint_text: 'Email'
            size_hint_y: None
            height: 40
            
        Button:
            text: 'Save Profile'
            size_hint_y: None
            height: 50
            on_press: root.save_profile()
            
        Button:
            text: 'Cancel'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'main_menu'
''')

class MyApp(App):
    def build(self):
        sm = ScreenManagement()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CreateProfileScreen(name='create_profile'))
        return sm

if __name__ == '__main__':
    MyApp().run()
