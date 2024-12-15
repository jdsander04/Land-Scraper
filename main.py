from tkinter import filedialog
import customtkinter
from tkintermapview import TkinterMapView
from LandData.Terrain import Terrain
import os
from LandData.elevationAPI import Tessadem

customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):

    APP_NAME = "LandScraper"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.folder = None
        self.polygon = None
        self.terrain = None  # Initialize terrain
        self.oldSW = (0, 0)
        self.oldNE = (0, 0)
        self.marker_list = []  # Initialize marker list

        if not os.path.exists("API_KEY") or os.path.getsize("API_KEY") == 0:
            self.init_api_key_ui()
        else:
            self.init_main_ui()

    def init_api_key_ui(self):
        """Initialize UI for API key submission."""
        self.title(f"{App.APP_NAME} - API Key Required")
        self.geometry("400x400")
        self.minsize(400, 400)

        self.api = Tessadem()

        # Header label
        self.header_label = customtkinter.CTkLabel(self, text="Enter API Key", font=("Arial", 20))
        self.header_label.pack(pady=(50, 10))

        # Textbox for API key input
        self.text_box = customtkinter.CTkTextbox(self, width=300, height=100)
        self.text_box.pack(pady=(0, 50))

        # Submit button
        self.button = customtkinter.CTkButton(self, text="Submit", command=self.submit_key)
        self.button.pack(pady=(0, 50))

        # message label
        self.message_label = customtkinter.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=(0, 10))

    def init_main_ui(self):
        """Initialize the main application UI."""
        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        # Set up frames
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.init_left_frame()
        self.init_right_frame()

    def init_left_frame(self):
        """Set up the left frame with options."""
        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        row_counter = 0

        # Export options
        self.export_dropdown = customtkinter.CTkLabel(self.frame_left, text="Export:", anchor="w")
        self.export_dropdown.grid(row=row_counter, column=0, padx=(20, 20), pady=(20, 0))
        row_counter += 1

        self.export_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["object", "png", "jpg", "GEOTIFF"],
                                                              command=self.change_export)
        self.export_option_menu.grid(row=row_counter, column=0, padx=(20, 20), pady=(10, 0))
        row_counter += 1

        # Folder button
        self.folder_button = customtkinter.CTkButton(master=self.frame_left, text="Choose Folder",
                                                     command=self.folder_button_clicked)
        self.folder_button.grid(row=row_counter, column=0, padx=(20, 20), pady=(20, 0))
        row_counter += 1

        # Export button
        self.export_button = customtkinter.CTkButton(master=self.frame_left, text="Export",
                                                     command=self.export_event)
        self.export_button.grid(row=row_counter, column=0, padx=(20, 20), pady=(20, 0))
        row_counter += 1

        # Map options
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=row_counter, column=0, padx=(20, 20), pady=(20, 0))
        row_counter += 1

        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", 
                                                                                     "Google satellite", "Google hybrid"],
                                                           command=self.change_map)
        self.map_option_menu.grid(row=row_counter, column=0, padx=(20, 20), pady=(10, 0))
        row_counter += 1

        # Appearance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=row_counter, column=0, padx=(20, 20), pady=(20, 0))
        row_counter += 1

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                        command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=row_counter, column=0, padx=(20, 20), pady=(10, 20))

    def init_right_frame(self):
        """Set up the right frame with the map."""
        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, column=0, sticky="nswe", padx=0, pady=0)
        self.map_widget.add_right_click_menu_command(label="Set Marker", command=self.set_marker_event, pass_coords=True)

        # Set default map and appearance values
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")

    def submit_key(self):
        """Handles API key submission."""
        key = self.text_box.get("1.0", "end-1c").strip()

        # Validate the API key
        if not key:
            print("API key cannot be empty!")  # Replace with a proper error message
            return
        
        if not self.api.CheckAPIKeyValidity(key):
            self.message_label.configure(text="Invalid API key!")  # Replace with a proper error message
            return

        with open("API_KEY", "w") as f:
            f.write(key)

        # Clear the API key submission UI
        self.header_label.destroy()
        self.text_box.destroy()
        self.button.destroy()
        self.message_label.destroy()

        # Initialize the main UI
        self.init_main_ui()


    def set_marker_event(self, coords: tuple):
        # If there are already two markers, delete the first one and remove it from the list
        if len(self.marker_list) == 2:
            self.marker_list[0].delete()
            self.marker_list.pop(0)

        # Add the new marker and append it to the list
        new_marker = self.map_widget.set_marker(coords[0], coords[1])
        self.marker_list.append(new_marker)

        # Remove any existing polygon first, if it exists
        if hasattr(self, 'polygon') and self.polygon is not None:
            self.polygon.delete()
            self.polygon = None

        # Create a new bounding box if there are exactly two markers
        if len(self.marker_list) == 2:
            marker1, marker2 = self.marker_list
            # Draw a polygon using the bounding box from the two marker positions
            self.polygon = self.map_widget.set_polygon([
                (marker1.position[0], marker1.position[1]),
                (marker2.position[0], marker1.position[1]),
                (marker2.position[0], marker2.position[1]),
                (marker1.position[0], marker2.position[1])
            ])

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()
    
    def folder_button_clicked(self):
        self.folder = filedialog.askdirectory()
        if len(self.folder) > 16:
            self.folder_button.configure(text=self.folder[:7] + "..." + self.folder[-7:])
        else:
            self.folder_button.configure(text=self.folder)
        print(self.folder)

    def export_event(self):
        export = self.export_option_menu.get()

        sw = (min(self.marker_list[0].position[0], self.marker_list[1].position[0]),
              min(self.marker_list[0].position[1], self.marker_list[1].position[1]))
        ne = (max(self.marker_list[0].position[0], self.marker_list[1].position[0]),
              max(self.marker_list[0].position[1], self.marker_list[1].position[1]))
        
        if abs(sw[0] - ne[0]) > 39.9 or abs(sw[1] - ne[1]) > 39.9:
            return #TODO: show error
        print(sw, ne)

        if sw != self.oldSW or ne != self.oldNE:
            self.terrain = Terrain(sw, ne)
            self.oldSW = sw
            self.oldNE = ne
        
        print(self.terrain.terrainInfo.elevationDataNPArray)

        if export == "object":
            self.terrain.MakeObjFile("test", self.folder)
        elif export == "png":
            self.terrain.MakePngFile("test", self.folder)
        elif export == "jpg":
            self.terrain.MakeJpgFile("test", self.folder)
        elif export == "GEOTIFF":
            self.terrain.MakeGeotiffFile("test", self.folder)
        
    def change_export(self, new_export: str):
        if new_export == "object":
            pass
        elif new_export == "png":
            pass
        elif new_export == "jpg":
            pass

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google hybrid":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()