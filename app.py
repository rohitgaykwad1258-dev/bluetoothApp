import asyncio
import math
from threading import Thread

from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.scrollview import MDScrollView

from scanner import scan_ble_devices

class BluetoothUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.05, 0.06, 0.07, 1)
        
        main_layout = MDBoxLayout(orientation='vertical', spacing="12dp", padding="16dp")
        
        title = MDLabel(
            text="Bluetooth Radar",
            font_style="Headline",
            role="medium",
            bold=True,
            size_hint_y=None,
            height="50dp"
        )
        main_layout.add_widget(title)
        
        scroll = MDScrollView()
        self.list_container = MDBoxLayout(
            orientation='vertical',
            spacing="12dp",
            size_hint_y=None
        )
        self.list_container.bind(minimum_height=self.list_container.setter('height'))
        
        self.placeholder = MDLabel(
            text="Press scan to search nearby Bluetooth devices.",
            halign="center",
            size_hint_y=None,
            height="100dp"
        )
        self.list_container.add_widget(self.placeholder)
        scroll.add_widget(self.list_container)
        main_layout.add_widget(scroll)
        
        self.scan_btn = MDButton(
            style="filled",
            pos_hint={"center_x": 0.5},
            on_release=self.start_scan
        )
        self.btn_text = MDButtonText(
            text="Scan Devices", 
            font_style="Title",
            role="medium",
            bold=True
        )
        self.scan_btn.add_widget(self.btn_text)
        main_layout.add_widget(self.scan_btn)
        
        self.add_widget(main_layout)

    def start_scan(self, instance):
        self.btn_text.text = "Scanning (5s)..."
        self.scan_btn.disabled = True
        self.list_container.clear_widgets()
        self.list_container.add_widget(MDLabel(
            text="Searching Bluetooth signals...",
            halign="center",
            size_hint_y=None,
            height="100dp"
        ))
        Thread(target=self.run_async_scanner, daemon=True).start()

    def run_async_scanner(self):
        try:
            devices = asyncio.run(scan_ble_devices())
            Clock.schedule_once(lambda dt: self.update_display(devices))
        except Exception as err:
            err_msg = str(err)
            Clock.schedule_once(lambda dt: self.show_error(err_msg))

    def calculate_distance(self, rssi, tx_power=-59, n=2.2):
        if rssi == 0:
            return -1.0
        return math.pow(10, (tx_power - rssi) / (10 * n))

    def update_display(self, devices):
        self.list_container.clear_widgets()
        self.scan_btn.disabled = False
        self.btn_text.text = "Scan Devices"
        
        if devices:
            for dev in devices:
                dist = self.calculate_distance(dev['rssi'])
                card = MDCard(
                    orientation='vertical',
                    size_hint_y=None,
                    height="80dp",
                    padding="12dp",
                    style="filled"
                )
                lbl = MDLabel(
                    text=f"[b]{dev['name']}[/b]\nMAC: {dev['address']} | Dist: {dist:.1f}m",
                    markup=True
                )
                card.add_widget(lbl)
                self.list_container.add_widget(card)
        else:
            self.list_container.add_widget(MDLabel(
                text="No Bluetooth devices found.\nMake sure Bluetooth is ON.",
                halign="center",
                size_hint_y=None,
                height="100dp"
            ))

    def show_error(self, err_msg, *args):
        self.list_container.clear_widgets()
        self.scan_btn.disabled = False
        self.btn_text.text = "Scan Devices"
        self.list_container.add_widget(MDLabel(
            text=f"Error: {err_msg}",
            halign="center",
            size_hint_y=None,
            height="100dp"
        ))

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return BluetoothUI()

if __name__ == "__main__":
    MainApp().run()