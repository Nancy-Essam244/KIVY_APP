import kivy
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, ShaderTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.clock import Clock
import pulp
import numpy as np
from kivy.graphics import Color, Rectangle

# المجموعات
energy_sources = ["Barley", "Corn, yellow", "Sorghum, grain", "Wheat bran"]
protein_sources = ["Soybean meal, solvent", "Soybean meal, dehulled solvent", 
                   "Fish meal, herring", "Meat meal", "Poultry by-product meal"]

ingredients_data = {
    "Barley": {"protein": 11.0, "energy": 2800, "calcium": 0.05},
    "Blood_meal": {"protein": 80.0, "energy": 2600, "calcium": 0.30},
    "Corn": {"protein": 8.5, "energy": 3300, "calcium": 0.03},
    "Fat": {"protein": 0.0, "energy": 8800, "calcium": 0.00},
    "Feather_meal": {"protein": 85.0, "energy": 2500, "calcium": 0.20},
    "Fish_meal_herring": {"protein": 60.0, "energy": 2900, "calcium": 5.5},
    "Fish_meal_menhaden": {"protein": 62.0, "energy": 3000, "calcium": 5.0},
    "Fish_meal_white": {"protein": 58.0, "energy": 2800, "calcium": 4.5},
    "Meat_meal": {"protein": 55.0, "energy": 2800, "calcium": 5.0},
    "Meat_and_bone_meal": {"protein": 50.0, "energy": 2600, "calcium": 10.0},
    "Poultry_byproduct_meal": {"protein": 60.0, "energy": 3000, "calcium": 4.0},
    "Sesame_meal": {"protein": 42.0, "energy": 2400, "calcium": 1.2},
    "Sorghum": {"protein": 10.0, "energy": 3100, "calcium": 0.04},
    "Soybean_heat": {"protein": 44.0, "energy": 2800, "calcium": 0.25},
    "Soybean_meal_solvent": {"protein": 44.0, "energy": 2700, "calcium": 0.25},
    "Soybean_meal_dehulled": {"protein": 48.0, "energy": 2800, "calcium": 0.25},
    "Sunflower_meal": {"protein": 35.0, "energy": 2200, "calcium": 0.35},
    "Wheat_bran": {"protein": 16.0, "energy": 1700, "calcium": 0.13},
    "Bone_meal": {"protein": 0.0, "energy": 0.0, "calcium": 30.0},
    "Calcium_carbonate": {"protein": 0.0, "energy": 0.0, "calcium": 38.0},
    "limestone": {"protein": 0.0, "energy": 0.0, "calcium": 36.0},
    "oyster": {"protein": 0.0, "energy": 0.0, "calcium": 35.0},
    "Phosphate_dicalcium": {"protein": 0.0, "energy": 0.0, "calcium": 23.0},
}

requirements = {
    "Starter": {"protein": 23, "energy": 3000, "calcium": 1.0},
    "Grower": {"protein": 20, "energy": 3100, "calcium": 0.9},
    "Finisher": {"protein": 18, "energy": 3200, "calcium": 0.8}
}



def show_error(msg):
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    layout.add_widget(Label(text=msg, color=(1,0,0,1), font_size='18sp'))

    btn = Button(text="OK", size_hint=(1, None), height=40)
    layout.add_widget(btn)

    popup = Popup(title="Selection Error", content=layout,
                  size_hint=(0.6, 0.4), auto_dismiss=False)
    btn.bind(on_release=popup.dismiss)
    popup.open()

Builder.load_string("""                   
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 20
        
        #Using canvas.before to add image to the background            
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)   #optional base color here its white
            Rectangle:
                pos: self.pos  
                size: self.size
                source:'Cute ducklings for animal lovers.jpg'
                          
        Label:
            text: 'Healthy chicken'
            font_size: '40sp'
            color: (0.65, 0.16, 0.16, 1) #dark brown color
            size_hint_y: None
            height: 100
            halign: 'center'
            valign: 'middle'
            
        Widget:
            size_hint_y: 1
        
       
        Button:
            text: 'Start'
            size_hint: (None, None)
            size: 200, 70
            pos_hint: {'center_x': 0.5}
            background_color: (1, 0.85, 0, 1)
            on_press: root.manager.current = 'settings'
            
            
        

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 30
        padding: 40

        canvas.before:
            Color:
                rgba: (0.9, 1, 0.9, 1)   # soft light green background
            Rectangle:
                pos: self.pos
                size: self.size
                    
        # Title label at top
        Label:
            text: 'Choose Broilers Age Range'
            font_size: '28sp'
            color: (0.2, 0.4, 0.2, 1)  # dark green text
            size_hint_y: None
            height: 60
        
        # Dropdown button
        Button:
            id: mainbutton
            text: 'Press to Choose Broilers age range '
            size_hint: (None, None)
            size: 380, 60
            pos_hint: {"center_x": 0.5}
            background_color: (1, 0.85, 0.4, 1)  # golden yellow
            color: (1, 1, 1, 1)
            on_release: root.dropdown.open(self)
        
        # Spacer to push ingredients button a bit lower
        Widget:
            size_hint_y: 0.3
                    
        Label:
            text: 'Select Exactly 3 Ingredients'
            font_size: '20sp'
            color: (0.2, 0.4, 0.2, 1)
            size_hint_y: None
            height: 30

        # Scrollable Ingredients (CENTERED rows)
        ScrollView:
            size_hint: (1, 1)

            GridLayout:
                id: ingredients_grid
                cols: 1
                spacing: 8
                size_hint_y: None
                height: self.minimum_height
                size_hint_x: 1
                padding: [10, 8, 10, 8]

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Barley"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Blood meal"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Corn, yellow"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Fat (animal, hydrolized)"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Feather meal, hydrolized"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Fish meal, herring"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Fish meal, menhaden"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Fish meal, white"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Meat meal"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Meat-and bone meal"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Poultry by-product meal"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Sesame meal, expeller"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Sorghum, grain"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Soybean, heat processed"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Soybean meal, solvent"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Soybean meal, dehulled solvent"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Sunflower meal, dehulled solvent"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Wheat bran"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Bone meal"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Calcium carbonate"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Limestone, ground"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Oyster shell, ground"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

                BoxLayout:
                    size_hint_y: None
                    height: 40
                    size_hint_x: None
                    width: root.width * 0.85
                    pos_hint: {"center_x": 0.5}
                    spacing: 8
                    padding: [8, 0, 0, 0]

                    CheckBox:
                        size_hint_x: None
                        width: 30
                    Label:
                        text: "Phosphate dicalcium"
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        color: (0, 0.6, 0, 1)
                        font_size: "16sp"

        Button:
            text: "Next"
            size_hint: (None, None)
            size: 200, 50
            pos_hint: {"center_x": 0.5}
            background_color: (0.2, 0.6, 0.8, 1)
            color: (1, 1, 1, 1)
            on_press: root.validate_and_go_next()

        
                    
        # Back button at bottom
        Button:
            text: 'Back to menu'
            size_hint: (None, None)
            size: 200, 50
            pos_hint: {"center_x": 0.5}
            background_color: (0.8, 0.3, 0.3, 1)  # reddish
            color: (1, 1, 1, 1)
            on_press: root.manager.current = 'menu'
                    

<CalculationScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 20

        canvas.before:
            Color:
                rgba: (0.95, 0.98, 0.95, 1)   # Very light pastel green
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            id: title_label
            text: "Ready to Calculate Ration"
            font_size: '26sp'
            color: (0.2, 0.4, 0.2, 1)   # Dark green
            size_hint_y: None
            height: 50
            bold: True

        # This container will either show the centered button OR the results
        BoxLayout:
            id: content_container
            orientation: 'vertical'
            size_hint: (1, 0.8)  # Take 80% of space for content

            # Centered button (initially visible)
            BoxLayout:
                id: button_container
                orientation: 'vertical'
                size_hint: (1, 1)

                Button:
                    id: calculate_btn
                    text: "Start Calculations"
                    size_hint: (None, None)
                    size: 250, 65
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    background_color: (0.3, 0.7, 0.3, 1)  # Nice green
                    color: (1, 1, 1, 1)
                    font_size: '18sp'
                    on_press: root.start_calculations()

            # Results container (initially empty and hidden)
            ScrollView:
                id: results_scrollview
                size_hint: (1, 1)
                opacity: 0  # Initially hidden
                
                BoxLayout:
                    id: results_container
                    orientation: 'vertical'
                    spacing: 10
                    size_hint_y: None
                    height: self.minimum_height
                    padding: [10, 10, 10, 10]

        # Navigation buttons at bottom (fixed height)
        BoxLayout:
            size_hint_y: None
            height: 60
            spacing: 20
            padding: [0, 10, 0, 0]

            Button:
                text: "Back to Settings"
                size_hint: (0.5, None)
                height: 50
                background_color: (1, 0.8, 0.4, 1)  # Orange
                color: (1, 1, 1, 1)
                font_size: '16sp'
                on_press: root.manager.current = 'settings'

            Button:
                text: "Back to Main Menu"
                size_hint: (0.5, None)
                height: 50
                background_color: (0.8, 0.3, 0.3, 1)  # Red
                color: (1, 1, 1, 1)
                font_size: '16sp'
                on_press: root.manager.current = 'menu'

""")


class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create dropdown
        self.dropdown = DropDown()

        # Add Broilers feed stages
        feed_stages = ["Starter", "Grower", "Finisher"]

        for stage in feed_stages:
            btn = Button(text=stage, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.set_option(btn.text))
            self.dropdown.add_widget(btn)

    def set_option(self, text):
        """Set chosen option on main button text and close dropdown"""
        self.ids.mainbutton.text = text
        self.dropdown.dismiss()

    def validate_and_go_next(self):
        selected = []
        for child in self.ids.ingredients_grid.children:
            checkbox = None
            label = None
            for widget in child.children:
                if isinstance(widget, CheckBox):
                    checkbox = widget
                if isinstance(widget, Label):
                    label = widget

            if checkbox and checkbox.active and label:
                selected.append(label.text.strip().lower())

        print("DEBUG Selected:", selected)

        # Count selected ingredients
        selected_count = len(selected)
        
        # validation على الـ Age Range
        if self.ids.mainbutton.text == "Press to Choose Broilers age range ":
            show_error("Please choose a broilers age range before proceeding.")
            return
        
        # Check if exactly 3 ingredients are selected
        if selected_count != 3:
            show_error("Please select exactly 3 ingredients for the calculation.")
            return
            
        # Normalize sources
        energy = [e.lower().strip() for e in energy_sources]
        protein = [p.lower().strip() for p in protein_sources]

        if not any(ing in energy for ing in selected):
            show_error("Please select at least one energy source (e.g., Corn).")
            return
        if not any(ing in protein for ing in selected):
            show_error("Please select at least one protein source (e.g., Soybean meal).")
            return

        self.manager.current = "calculation"

    def get_selected_ingredients(self):
        """Get the selected ingredients by their group names"""
        selected = []
        for child in self.ids.ingredients_grid.children:
            checkbox = None
            label_widget = None
            
            # Find checkbox and label in this row
            for widget in child.children:
                if isinstance(widget, CheckBox):
                    checkbox = widget
                elif isinstance(widget, Label):
                    label_widget = widget
            
            # If checkbox is active, map the label text to data key
            if checkbox and checkbox.active and label_widget:
                label_text = label_widget.text.strip()
                
                # Map label text to data key
                ingredient_map = {
                    "Barley": "Barley",
                    "Blood meal": "Blood_meal", 
                    "Corn, yellow": "Corn",
                    "Fat (animal, hydrolized)": "Fat",
                    "Feather meal, hydrolized": "Feather_meal",
                    "Fish meal, herring": "Fish_meal_herring",
                    "Fish meal, menhaden": "Fish_meal_menhaden",
                    "Fish meal, white": "Fish_meal_white",
                    "Meat meal": "Meat_meal",
                    "Meat-and bone meal": "Meat_and_bone_meal",
                    "Poultry by-product meal": "Poultry_byproduct_meal",
                    "Sesame meal, expeller": "Sesame_meal",
                    "Sorghum, grain": "Sorghum",
                    "Soybean, heat processed": "Soybean_heat",
                    "Soybean meal, solvent": "Soybean_meal_solvent",
                    "Soybean meal, dehulled solvent": "Soybean_meal_dehulled",
                    "Sunflower meal, dehulled solvent": "Sunflower_meal",
                    "Wheat bran": "Wheat_bran",
                    "Bone meal": "Bone_meal",
                    "Calcium carbonate": "Calcium_carbonate",
                    "Limestone, ground": "limestone",
                    "Oyster shell, ground": "oyster",
                    "Phosphate dicalcium": "Phosphate_dicalcium"
                }
                
                if label_text in ingredient_map:
                    selected.append(ingredient_map[label_text])
                else:
                    print(f"DEBUG: Could not map label: {label_text}")
        
        print(f"DEBUG: Mapped ingredients: {selected}")
        return selected

class CalculationScreen(Screen):
    def start_calculations(self):
        try:
            # Get selected ingredients
            settings_screen = self.manager.get_screen("settings")
            selected_ingredients = settings_screen.get_selected_ingredients()
            
            if len(selected_ingredients) != 3:
                self.show_error_on_screen("Please select exactly 3 ingredients for this calculation.")
                return
            
            # Hide the button and show loading
            self.hide_button_show_loading()
            
            # Schedule calculation
            Clock.schedule_once(lambda dt: self.do_calculation(selected_ingredients), 0.5)
            
        except Exception as e:
            self.show_error_on_screen(f"Calculation error: {str(e)}")
    
    def hide_button_show_loading(self):
        """Hide the centered button and show loading message"""
        # Hide the button container
        self.ids.button_container.opacity = 0
        self.ids.button_container.height = 0
        
        # Show the results scrollview
        self.ids.results_scrollview.opacity = 1
        
        # Clear any previous results and show loading
        self.ids.results_container.clear_widgets()
        
        loading_layout = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=150,
            padding=20
        )
        
        loading_label = Label(
            text="Calculating optimal mix...\n\nPlease wait",
            font_size='20sp',
            color=(0.3, 0.3, 0.3, 1),
            bold=True,
            halign='center'
        )
        
        loading_layout.add_widget(loading_label)
        self.ids.results_container.add_widget(loading_layout)
        
        # Update title
        self.ids.title_label.text = "Calculating..."
    
    def show_results_on_screen(self, solution, ingredients, age_range):
        """Show calculation results directly on the screen with pastel colors"""
        # Make sure results container is visible
        self.ids.results_scrollview.opacity = 1
        
        # Clear previous results
        self.ids.results_container.clear_widgets()
        
        # Update title
        self.ids.title_label.text = "Calculation Results"
        
        # Check if solution is valid
        if any(x < 0 for x in solution) or any(x > 97 for x in solution):
            self.show_error_on_screen("No valid solution found. Please try different ingredients.")
            return
        
        # Main results container
        main_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=400,
            spacing=10,
            padding=[10, 10, 10, 10]
        )
        
        # Header with pastel blue background
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=50,
            padding=[10, 5, 10, 5]
        )
        # FIXED: Use Kivy's Color properly
        header_layout.canvas.before.clear()
        with header_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.7, 0.8, 1, 1)  # Pastel blue
            Rectangle(pos=header_layout.pos, size=header_layout.size)
        
        header_label = Label(
            text="[b]Final Ration Mixture[/b]",
            font_size='20sp',
            color=(0.1, 0.1, 0.5, 1),
            markup=True
        )
        header_layout.add_widget(header_label)
        main_container.add_widget(header_layout)
        
        # Ingredients table with pastel yellow background
        table_layout = GridLayout(
            cols=2,
            size_hint_y=None,
            height=200,
            spacing=5,
            padding=[15, 10, 15, 10]
        )
        # FIXED: Use Kivy's Color properly
        table_layout.canvas.before.clear()
        with table_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 0.9, 1)  # Pastel yellow
            Rectangle(pos=table_layout.pos, size=table_layout.size)
        
        # Table headers
        table_layout.add_widget(Label(
            text="[b]Ingredient[/b]", 
            font_size='16sp', 
            color=(0, 0, 0, 1),
            markup=True
        ))
        table_layout.add_widget(Label(
            text="[b]%[/b]", 
            font_size='16sp', 
            color=(0, 0, 0, 1),
            markup=True,
            halign='right'
        ))
        
        # Add main ingredients
        main_ingredients_total = 0
        for i, ing in enumerate(ingredients):
            percentage = max(0, min(97, solution[i]))
            ing_name = ing.replace('_', ' ').title()
            
            table_layout.add_widget(Label(
                text=ing_name, 
                font_size='14sp', 
                color=(0, 0, 0, 1)
            ))
            table_layout.add_widget(Label(
                text=f"{percentage:.2f}", 
                font_size='14sp', 
                color=(0, 0, 0, 1),
                halign='right'
            ))
            main_ingredients_total += percentage
        
        # Add fixed additives
        additives = [
            ("Dicalcium Phosphate", 1.00),
            ("Limestone", 0.91),
            ("Methionine", 0.06)
        ]
        
        for name, percent in additives:
            table_layout.add_widget(Label(
                text=name, 
                font_size='14sp', 
                color=(0, 0, 0, 1)
            ))
            table_layout.add_widget(Label(
                text=f"{percent:.2f}", 
                font_size='14sp', 
                color=(0, 0, 0, 1),
                halign='right'
            ))
        
        # Calculate remaining additives
        remaining_additives = 3.00 - (1.00 + 0.91 + 0.06)
        table_layout.add_widget(Label(
            text="Additives*", 
            font_size='14sp', 
            color=(0, 0, 0, 1)
        ))
        table_layout.add_widget(Label(
            text=f"{remaining_additives:.2f}", 
            font_size='14sp', 
            color=(0, 0, 0, 1),
            halign='right'
        ))
        
        # Total row
        final_total = main_ingredients_total + 3.00
        table_layout.add_widget(Label(
            text="[b]Total[/b]", 
            font_size='16sp', 
            color=(0, 0, 0, 1),
            markup=True
        ))
        table_layout.add_widget(Label(
            text=f"[b]{final_total:.2f}[/b]", 
            font_size='16sp', 
            color=(0, 0, 0, 1),
            markup=True,
            halign='right'
        ))
        
        main_container.add_widget(table_layout)
        
        # Calculation note with pastel green background
        note_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=40,
            padding=[10, 5, 10, 5]
        )
        # FIXED: Use Kivy's Color properly
        note_layout.canvas.before.clear()
        with note_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.9, 1, 0.9, 1)  # Pastel green
            Rectangle(pos=note_layout.pos, size=note_layout.size)
        
        note_label = Label(
            text=f"* Calculated as [3.00 - (1.00 + 0.91 + 0.06)]",
            font_size='12sp',
            color=(0.2, 0.4, 0.2, 1)
        )
        note_layout.add_widget(note_label)
        main_container.add_widget(note_layout)
        
        # Nutrient analysis with pastel orange background
        nutrient_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            spacing=5,
            padding=[15, 10, 15, 10]
        )
        # FIXED: Use Kivy's Color properly
        nutrient_layout.canvas.before.clear()
        with nutrient_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 0.95, 0.8, 1)  # Pastel orange
            Rectangle(pos=nutrient_layout.pos, size=nutrient_layout.size)
        
        nutrient_label = Label(
            text="[b]Nutrient Analysis:[/b]",
            font_size='16sp',
            color=(0.5, 0.3, 0.1, 1),
            markup=True
        )
        nutrient_layout.add_widget(nutrient_label)
        
        # Calculate nutrients
        protein_achieved = sum(solution[i] * ingredients_data[ingredients[i]]["protein"] / 100 for i in range(3))
        energy_achieved = sum(solution[i] * ingredients_data[ingredients[i]]["energy"] / 100 for i in range(3))
        calcium_achieved = sum(solution[i] * ingredients_data[ingredients[i]]["calcium"] / 100 for i in range(3))
        calcium_achieved += (1.00 * 23.0 + 0.91 * 36.0) / 100
        
        req = requirements[age_range]
        
        nutrient_text = f"• Protein: {protein_achieved:.1f}% (Target: {req['protein']}%)\n"
        nutrient_text += f"• Energy: {energy_achieved:.0f} kcal/kg (Target: {req['energy']})\n"
        nutrient_text += f"• Calcium: {calcium_achieved:.2f}% (Target: {req['calcium']}%)"
        
        nutrient_details = Label(
            text=nutrient_text,
            font_size='14sp',
            color=(0.3, 0.2, 0.1, 1),
            halign='left'
        )
        nutrient_layout.add_widget(nutrient_details)
        
        main_container.add_widget(nutrient_layout)
        
        # Add everything to the main container
        self.ids.results_container.add_widget(main_container)
    
    def show_error_on_screen(self, message):
        """Show error message directly on the screen with detailed information"""
        # Make sure results container is visible
        self.ids.results_scrollview.opacity = 1
        
        # Hide the button container
        self.ids.button_container.opacity = 0
        self.ids.button_container.height = 0
        
        # Clear previous results
        self.ids.results_container.clear_widgets()
        
        # Update title
        self.ids.title_label.text = "Calculation Error"
        
        # Main error container
        error_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=250,  # Reduced height since we removed the button
            spacing=15,
            padding=[20, 20, 20, 20]
        )
        with error_container.canvas.before:
            Color(1, 0.9, 0.9, 1)  # Pastel red
            Rectangle(pos=error_container.pos, size=error_container.size)
        
        # Error icon and main message
        main_error_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=80
        )
        
        error_icon = Label(
            text="❌",
            font_size='30sp',
            size_hint_y=None,
            height=40
        )
        main_error_layout.add_widget(error_icon)
        
        main_error_label = Label(
            text="[b]Calculation Failed[/b]",
            font_size='20sp',
            color=(0.8, 0.2, 0.2, 1),
            markup=True,
            size_hint_y=None,
            height=40
        )
        main_error_layout.add_widget(main_error_label)
        
        error_container.add_widget(main_error_layout)
        
        # Detailed error message
        detail_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=150  # Increased height for better text display
        )
        
        detail_label = Label(
            text=message,
            font_size='16sp',
            color=(0.6, 0.1, 0.1, 1),
            halign='center',
            valign='middle',
            text_size=(400, None)
        )
        detail_layout.add_widget(detail_label)
        
        # Additional helpful information
        help_label = Label(
            text="\nPlease go back to Settings and adjust your selection.",
            font_size='14sp',
            color=(0.5, 0.1, 0.1, 1),
            halign='center',
            text_size=(400, None)
        )
        detail_layout.add_widget(help_label)
        
        error_container.add_widget(detail_layout)
        
        self.ids.results_container.add_widget(error_container)
    
    def do_calculation(self, selected_ingredients):
        """Perform the calculation with the selected ingredients"""
        try:
            print(f"DEBUG: Starting calculation with ingredients: {selected_ingredients}")
            
            # Get age range and requirements
            settings_screen = self.manager.get_screen("settings")
            age_range = settings_screen.ids.mainbutton.text
            req = requirements[age_range]
            
            print(f"DEBUG: Age range: {age_range}, Requirements: {req}")
            
            # Solve using simple linear algebra
            solution = self.solve_three_equations(selected_ingredients, req)
            
            print(f"DEBUG: Solution: {solution}")
            
            # Show results on screen
            self.show_results_on_screen(solution, selected_ingredients, age_range)
            
        except Exception as e:
            print(f"DEBUG: Error in calculation: {str(e)}")
            import traceback
            traceback.print_exc()
            self.show_error_on_screen(f"Calculation error: {str(e)}")
    
    def on_enter(self):
        """Reset the screen when entering"""
        # Show the button container
        self.ids.button_container.opacity = 1
        self.ids.button_container.height = 200
        
        # Hide the results scrollview
        self.ids.results_scrollview.opacity = 0
        
        # Clear results
        self.ids.results_container.clear_widgets()
        
        # Reset title
        self.ids.title_label.text = "Ready to Calculate Ration"
        
        # Reset button
        self.ids.calculate_btn.text = "Start Calculations"
        self.ids.calculate_btn.background_color = (0.3, 0.7, 0.3, 1)
        self.ids.calculate_btn.disabled = False
    
    def solve_three_equations(self, ingredients, requirements):
        """
        Solve system of 3 equations with 3 unknowns for ANY ingredient combination
        """
        
        print(f"DEBUG: Solving for {ingredients} with req: {requirements}")
        
        # Get ingredient data
        ing1_data = ingredients_data[ingredients[0]]
        ing2_data = ingredients_data[ingredients[1]]
        ing3_data = ingredients_data[ingredients[2]]
        
        print(f"DEBUG: {ingredients[0]}: Protein={ing1_data['protein']}%, Energy={ing1_data['energy']}")
        print(f"DEBUG: {ingredients[1]}: Protein={ing2_data['protein']}%, Energy={ing2_data['energy']}")
        print(f"DEBUG: {ingredients[2]}: Protein={ing3_data['protein']}%, Energy={ing3_data['energy']}")
        
        # Try multiple approaches to find a solution
        
        # Approach 1: Direct linear algebra
        try:
            A = np.array([
                [ing1_data["protein"], ing2_data["protein"], ing3_data["protein"]],
                [ing1_data["energy"], ing2_data["energy"], ing3_data["energy"]],
                [1, 1, 1]
            ])
            B = np.array([
                requirements["protein"] * 97,
                requirements["energy"] * 97, 
                97
            ])
            
            print(f"DEBUG: Matrix A:\n{A}")
            print(f"DEBUG: Vector B: {B}")
            
            solution = np.linalg.solve(A, B)
            print(f"DEBUG: Direct solution: {solution}")
            
            # Check if solution is physically possible (all positive)
            if all(x >= -0.1 for x in solution):  # Small tolerance for rounding errors
                # Adjust any slightly negative values to zero
                adjusted_solution = [max(0, x) for x in solution]
                
                # Re-normalize to 97% if needed
                total = sum(adjusted_solution)
                if abs(total - 97) > 0.1:
                    adjusted_solution = [x * 97 / total for x in adjusted_solution]
                
                print(f"DEBUG: Adjusted solution: {adjusted_solution}")
                return adjusted_solution
                
        except np.linalg.LinAlgError as e:
            print(f"DEBUG: Linear algebra failed: {e}")
        
        # Approach 2: Linear programming with relaxed constraints
        return self.solve_with_linear_programming(ingredients, requirements)

    def solve_with_linear_programming(self, ingredients, requirements):
        """Enhanced linear programming that uses ALL ingredients"""
        print("DEBUG: Using enhanced linear programming")
        
        prob = pulp.LpProblem("FeedFormulation", pulp.LpMinimize)
        
        # Variables with minimum usage constraints
        x1 = pulp.LpVariable(ingredients[0], lowBound=5, upBound=80)   # At least 5%
        x2 = pulp.LpVariable(ingredients[1], lowBound=5, upBound=80)   # At least 5%
        x3 = pulp.LpVariable(ingredients[2], lowBound=5, upBound=80)   # At least 5%
        
        # Get ingredient data
        ing1_data = ingredients_data[ingredients[0]]
        ing2_data = ingredients_data[ingredients[1]]
        ing3_data = ingredients_data[ingredients[2]]
        
        # Objective: minimize cost or balance nutrients
        # Let's minimize the deviation from requirements
        protein_dev = pulp.LpVariable("protein_dev", lowBound=0)
        energy_dev = pulp.LpVariable("energy_dev", lowBound=0)
        
        prob += protein_dev + energy_dev  # Minimize total deviation
        
        # Protein constraint
        protein_total = (
            x1 * ing1_data["protein"] +
            x2 * ing2_data["protein"] +
            x3 * ing3_data["protein"]
        )
        protein_target = requirements["protein"] * 97
        
        prob += protein_total >= protein_target
        prob += protein_total - protein_target <= protein_dev
        
        # Energy constraint  
        energy_total = (
            x1 * ing1_data["energy"] +
            x2 * ing2_data["energy"] +
            x3 * ing3_data["energy"]
        )
        energy_target = requirements["energy"] * 97
        
        prob += energy_total >= energy_target
        prob += energy_total - energy_target <= energy_dev
        
        # Sum to 97%
        prob += (x1 + x2 + x3 == 97)
        
        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        print(f"DEBUG: LP status: {pulp.LpStatus[prob.status]}")
        
        if prob.status == 1:
            solution = [x1.value(), x2.value(), x3.value()]
            
            # Calculate actual nutrients
            actual_protein = sum(solution[i] * ingredients_data[ingredients[i]]["protein"] for i in range(3)) / 100
            actual_energy = sum(solution[i] * ingredients_data[ingredients[i]]["energy"] for i in range(3)) / 100
            
            print(f"DEBUG: Enhanced LP solution: {solution}")
            print(f"DEBUG: Achieved - Protein: {actual_protein:.1f}%, Energy: {actual_energy:.0f}")
            
            return solution
        else:
            print("DEBUG: Enhanced LP failed, trying without minimum constraints")
            # Fallback to original method without minimum constraints
            return self.solve_with_linear_programming_fallback(ingredients, requirements)

    def solve_with_linear_programming_fallback(self, ingredients, requirements):
        """Fallback without minimum constraints"""
        prob = pulp.LpProblem("FeedFormulation_Fallback", pulp.LpMinimize)
        
        x1 = pulp.LpVariable(ingredients[0], lowBound=0, upBound=97)
        x2 = pulp.LpVariable(ingredients[1], lowBound=0, upBound=97) 
        x3 = pulp.LpVariable(ingredients[2], lowBound=0, upBound=97)
        
        ing1_data = ingredients_data[ingredients[0]]
        ing2_data = ingredients_data[ingredients[1]]
        ing3_data = ingredients_data[ingredients[2]]
        
        # Simple objective
        prob += x1 + x2 + x3
        
        # Constraints
        prob += (
            x1 * ing1_data["protein"] +
            x2 * ing2_data["protein"] +
            x3 * ing3_data["protein"] >= requirements["protein"] * 97
        )
        
        prob += (
            x1 * ing1_data["energy"] +
            x2 * ing2_data["energy"] +
            x3 * ing3_data["energy"] >= requirements["energy"] * 97
        )
        
        prob += (x1 + x2 + x3 == 97)
        
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        if prob.status == 1:
            return [x1.value(), x2.value(), x3.value()]
        else:
            # Last resort: proportional distribution based on protein content
            protein_sum = sum(ingredients_data[ing]["protein"] for ing in ingredients)
            return [97 * ingredients_data[ing]["protein"] / protein_sum for ing in ingredients]
    
    def show_loading(self):
        """Show loading popup"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        content.add_widget(Label(text="Calculating optimal mix...", font_size='18sp'))
        
        self.loading_popup = Popup(
            title="Processing",
            content=content,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )
        self.loading_popup.open()
    
    def show_results(self, solution, ingredients, age_range):
        """Show calculation results with detailed analysis"""
        if hasattr(self, 'loading_popup'):
            self.loading_popup.dismiss()
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Always show results, even if not perfect
        result_text = "[b]Final Ration Mixture[/b]\n\n"
        
        # Table header
        result_text += "[color=000000][b]Ingredient[/b]".ljust(30) + "[b]%[/b][/color]"
        result_text += "[color=000000]" + "─" * 35 + "[/color]"
        
        main_ingredients_total = 0
        # Add each main ingredient row
        for i, ing in enumerate(ingredients):
            percentage = max(0, min(97, solution[i]))
            ing_name = ing.replace('_', ' ').title()
            result_text += f"[color=000000]{ing_name:<28} {percentage:>6.2f}[/color]\n"
            main_ingredients_total += percentage
        
        # Calculate additives (fixed 3%)
        additives_total = 3.00
        
        # Add fixed additives rows
        result_text += f"[color=000000]{'Dicalcium Phosphate':<28}  1.00[/color]\n"
        result_text += f"[color=000000]{'Limestone':<28}  0.91[/color]\n"
        result_text += f"[color=000000]{'Methionine':<28}  0.06[/color]\n"
        
        # Calculate the remaining additives
        remaining_additives = additives_total - (1.00 + 0.91 + 0.06)
        result_text += f"[color=000000]{'Additives':<28}{remaining_additives:>6.2f}*[/color]\n"
        
        # Add total row
        result_text += "[color=000000]" + "─" * 35 + "[/color]\n"
        final_total = main_ingredients_total + additives_total
        result_text += f"[color=000000][b]{'Total':<28}[/b][b]{final_total:>6.2f}[/b][/color]\n"
        
        # Add calculation note
        result_text += f"\n* Calculated as [3.00 - (1.00 + 0.91 + 0.06)]\n"
        
        # Show nutrient analysis
        result_text += "\n[b]Nutrient Analysis:[/b]\n"
        
        # Calculate actual nutrients achieved
        protein_achieved = sum(solution[i] * ingredients_data[ingredients[i]]["protein"] / 100 for i in range(3))
        energy_achieved = sum(solution[i] * ingredients_data[ingredients[i]]["energy"] / 100 for i in range(3))
        calcium_achieved = sum(solution[i] * ingredients_data[ingredients[i]]["calcium"] / 100 for i in range(3))
        
        # Add nutrients from fixed additives
        calcium_achieved += (1.00 * 23.0 + 0.91 * 36.0) / 100
        
        req = requirements[age_range]
        
        result_text += f"• Protein: {protein_achieved:.1f}% (Target: {req['protein']}%)\n"
        result_text += f"• Energy: {energy_achieved:.0f} kcal/kg (Target: {req['energy']})\n" 
        result_text += f"• Calcium: {calcium_achieved:.2f}% (Target: {req['calcium']}%)\n"
        
        # Add quality assessment
        protein_diff = abs(protein_achieved - req['protein']) / req['protein'] * 100
        energy_diff = abs(energy_achieved - req['energy']) / req['energy'] * 100
        
        if protein_diff <= 5 and energy_diff <= 5:
            result_text += "\n✅ Excellent match with requirements!"
        elif protein_diff <= 10 and energy_diff <= 10:
            result_text += "\n⚠️ Good match - close to requirements"
        else:
            result_text += "\n📊 Solution found - consider adjusting ingredients"
        
        result_label = Label(
            text=result_text,
            font_name='DejaVuSans',
            font_size='14sp',
            halign="left",
            valign="top",
            text_size=(450, None),
            color=(0, 0, 0, 1),
            markup=True
        )
        content.add_widget(result_label)
        
        # Close button
        close_btn = Button(
            text="Close", 
            size_hint_y=None, 
            height=50,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Calculation Results",
            content=content,
            size_hint=(0.85, 0.8)
        )
        
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
           


class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=ShaderTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CalculationScreen(name='calculation'))

        return sm
    
MyApp().run() 
