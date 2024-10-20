import customtkinter
from tkintermapview import TkinterMapView
from LandData.Terrain import Terrain

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "LandScraper"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):

        self.terrain: Terrain
        self.oldSW: tuple = (0, 0)
        self.oldNE: tuple = (0, 0)

        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        #self.bind("<Mouse-3>", self.place_marker)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(0, weight=1)

        self.export_dropdown = customtkinter.CTkLabel(self.frame_left, text="Export:", anchor="w")
        self.export_dropdown.grid(row=2, column=0, padx=(20, 20), pady=(20, 0))

        self.export_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["object", "png", "jpg"],
                                                               command=self.change_export)
        self.export_option_menu.grid(row=3, column=0, padx=(20, 20), pady=(10, 0))

        self.export_button = customtkinter.CTkButton(master=self.frame_left,
                                                      text="Export",
                                                      command=self.export_event)
        self.export_button.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite", "Google hybrid"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=6, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.add_right_click_menu_command(label="Set Marker", command=self.set_marker_event, pass_coords=True)

        # Set default values
        #self.map_widget.set_address("Berlin, Germany")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")

    def set_marker_event(self, coords: tuple):
        if len(self.marker_list) == 2:
            self.marker_list[0].delete()
            del self.marker_list[0]
        self.marker_list.append(self.map_widget.set_marker(coords[0], coords[1]))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

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
            self.terrain.MakeObjFile("test")
        elif export == "png":
            self.terrain.MakePngFile("test")
        elif export == "jpg":
            pass
        
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