import customtkinter as ctk
import Assets.Scripts.variables as vary
import Assets.Scripts.scan_tab as scan
import Assets.Scripts.create_tab as create
import Assets.Scripts.settings as set


class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=vary.colors[3])
        self.frame = set.Settings(self)
        self.frame.pack()


class ScanTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=vary.colors[3])
        self.frame = scan.ScanTab(self)
        self.frame.pack()


class CreateTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=vary.colors[3])
        self.frame = create.CreateTab(self)
        self.frame.pack()


class TabWidget(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        vary.tab_view = self

        # create tabs
        tabs = ['Scan', 'Create', 'Settings']
        for i in tabs:
            self.add(i)
            self.tab(i).configure(fg_color=vary.colors[3])

        self.configure(width=vary.width, height=vary.height, fg_color=vary.colors[2])
        self._segmented_button.configure(
            fg_color=vary.colors[3], font=('segio', 15), unselected_hover_color=vary.colors[1],
            unselected_color=vary.colors[0], selected_color=vary.colors[2], selected_hover_color=vary.colors[0])

        # add widgets on tabs
        self.scan_tab = ScanTab(master=self.tab("Scan"))
        self.create_tab = CreateTab(master=self.tab("Create"))
        self.settings_tab = SettingsTab(master=self.tab("Settings"))

        self.scan_tab.pack()
        self.create_tab.pack()
        self.settings_tab.pack()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        x = (self.winfo_screenwidth() / 2) - (vary.width / 2)
        y = ((self.winfo_screenheight() - 120) / 2) - (vary.height / 2)

        self.title('QR Scanner')
        self.geometry(f'{vary.width}x{vary.height}+{int(x)}+{int(y)}')
        self.iconbitmap('Assets/Images/icon_1.ico')
        self.resizable(0, 0)
        self.configure(fg_color=vary.colors[2])
        self.protocol('WM_DELETE_WINDOW', self.close_event_handler)

        self.tab_wdj = TabWidget(master=self)
        self.tab_wdj.pack()

    def close_event_handler(self):
        f = open('Assets/Data/colors.txt', 'w')
        txt = ''
        for i in vary.colors:
            txt = txt + i + '\n'
        f.write(txt)
        f = open('Assets/Data/number.txt', 'w')
        f.write(f'{vary.number}')
        self.quit()

