import customtkinter


class TitleTop(customtkinter.CTkToplevel):
    def __init__(self, master, text):
        super().__init__()

        self.after(10)
        self.master = master
        master.minsize(200, 100)
        self.after(100, lambda: self.overrideredirect(True))
        self.transparent_color = self._apply_appearance_mode(self._fg_color)
        self.attributes("-transparentcolor", self.transparent_color)
        self.resizable(True, True)
        self.transient(self.master)
        self.config(background=self.transparent_color)
        self.x_offset = 50
        self.y_offset = 6

        master.bind("<Configure>", lambda _: self.change_dimension())
        master.bind("<Destroy>", lambda _: self.destroy())
        master.bind("<Map>", lambda e: self.withdraw)

        text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
        title = customtkinter.CTkLabel(
            self,
            text=text,
            fg_color="transparent",
            font=("Roboto Medium", -16),
            text_color=text_color,
            height=10,
        )
        title.grid(row=0, column=0, padx=(0, 10))

    def change_dimension(self):
        width = self.master.winfo_width() - 130 - self.x_offset
        if width < 0:
            self.withdraw()
            return
        if self.master.state() == "iconic":
            self.withdraw()
            return
        height = self.master.winfo_height()
        x = self.master.winfo_x() + self.x_offset
        y = self.master.winfo_y() + self.y_offset
        if self.master.state() == "zoomed":
            y += 4
            x -= 7
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()
