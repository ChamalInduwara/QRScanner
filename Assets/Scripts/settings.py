import customtkinter as ctk
import Assets.Scripts.variables as vary
import segno
import os
from PIL import Image, ImageTk
import tkinter.colorchooser as ch


class Settings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=vary.colors[3])
        vary.settings_tab = self

        self.frame_1 = ctk.CTkFrame(master=self, fg_color=vary.colors[3])
        self.frame_2 = ctk.CTkFrame(master=self, fg_color=vary.colors[3])

        qr = segno.make_qr('Demo Qr for Preview')
        qr.save(
            out=f'Assets/Images/demo.png',
            scale=10,
            border=2,
            light=vary.colors[4],
            dark=vary.colors[5]
        )

        self.img = Image.open(f'Assets/Images/demo.png')
        self.res_img = self.img.resize((200, 200))
        self.image = ImageTk.PhotoImage(self.res_img)

        self.img_1 = Image.open(f'Assets/Images/color.png')
        self.res_img_1 = self.img_1.resize((20, 20))
        self.image_1 = ImageTk.PhotoImage(self.res_img_1)

        self.lbl = ctk.CTkLabel(
            master=self, text='Settings', font=('segio', 30), corner_radius=5, width=vary.width - 10, anchor='w'
        )
        self.choose_clr_one_lbl = ctk.CTkLabel(master=self.frame_1, text=f'Choose background color:')
        self.choose_clr_two_lbl = ctk.CTkLabel(master=self.frame_1, text=f'Choose foreground color:')
        self.space = ctk.CTkLabel(master=self.frame_1, text='', height=60)
        self.space_1 = ctk.CTkLabel(master=self.frame_1, text='', height=20)
        self.space_2 = ctk.CTkLabel(master=self.frame_1, text='', height=20)

        self.choose_clr_one_btn = ctk.CTkButton(master=self.frame_1, text='', image=self.image_1)
        self.choose_clr_two_btn = ctk.CTkButton(master=self.frame_1, text='', image=self.image_1)

        self.reset_btn = ctk.CTkButton(master=self.frame_1, text='Reset to Default')
        self.clear_btn = ctk.CTkButton(master=self.frame_1, text='Clear Cache')

        self.preview = ctk.CTkLabel(master=self.frame_2, text='', image=self.image)

        self.reset_btn.bind('<Button-1>', self.reset_btn_action)
        self.clear_btn.bind('<Button-1>', self.clear_cache_action)
        self.choose_clr_one_btn.bind('<Button-1>', lambda x: self.pick_colors(None, 1))
        self.choose_clr_two_btn.bind('<Button-1>', lambda x: self.pick_colors(None, 2))

        array_one = [
            self.choose_clr_two_lbl, self.choose_clr_one_lbl
        ]

        array_two = [
            self.choose_clr_two_btn, self.choose_clr_one_btn
        ]

        array_three = [
            self.reset_btn, self.clear_btn
        ]

        for i in array_one:
            i.configure(font=('segio', 15), anchor='w')

        for i in array_two:
            i.configure(width=30, height=30, fg_color=vary.colors[0], hover_color=vary.colors[1])

        for i in array_three:
            i.configure(
                width=(((vary.width - 65) / 2) / 2) - 10, height=30, fg_color=vary.colors[0], hover_color=vary.colors[1]
            )

        self.lbl.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.frame_1.grid(row=1, column=0, padx=5, pady=5)
        self.frame_2.grid(row=1, column=1, padx=5, pady=5)

        self.space_2.grid(row=0, column=0, padx=5, pady=5)
        self.choose_clr_one_lbl.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.choose_clr_one_btn.grid(row=1, column=1, padx=5, pady=5)
        self.space_1.grid(row=2, column=0, padx=5, pady=5)
        self.choose_clr_two_lbl.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.choose_clr_two_btn.grid(row=3, column=1, padx=5, pady=5)
        self.space.grid(row=4, column=0, padx=5, pady=5)
        self.reset_btn.grid(row=5, column=0, padx=5, pady=5)
        self.clear_btn.grid(row=5, column=1, padx=5, pady=5)

        self.preview.grid(row=0, column=0, padx=5, pady=5, sticky='n')

    def clear_cache_action(self, event):
        vary.create_tab.output_field.configure(image='')
        vary.create_tab.entry.delete('0.0', ctk.END)
        vary.scan_tab.output_field.configure(state='normal')
        vary.scan_tab.output_field.delete('0.0', ctk.END)
        vary.scan_tab.output_field.configure(state='disabled')
        vary.scan_tab.entry.delete('0', ctk.END)
        for i in range(1, vary.number):
            os.remove(f'Assets/QRs/qr_{i}.png')
        vary.number = 1

    def pick_colors(self, event, num):
        if num == 1:
            color = ch.askcolor(title='Choose Background Color')
        elif num == 2:
            color = ch.askcolor(title='Choose Foreground Color')
            
        if color[1] is not None:
            if num == 1:
                vary.colors[4] = color[1]
            elif num == 2:
                vary.colors[5] = color[1]
            self.saving_the_colors()
            self.updating_the_image()

    def reset_btn_action(self, event):
        vary.colors[4] = '#ffffff'
        vary.colors[5] = '#101010'
        self.saving_the_colors()
        self.updating_the_image()

    def saving_the_colors(self):
        f = open('Assets/Data/colors.txt', 'w')
        txt = ''
        for i in vary.colors:
            txt = txt + i + '\n'
        f.write(txt)

    def updating_the_image(self):
        qr = segno.make_qr('Demo Qr for Preview')
        qr.save(
            out=f'Assets/Images/demo.png',
            scale=10,
            border=2,
            light=vary.colors[4],
            dark=vary.colors[5]
        )

        self.img = Image.open(f'Assets/Images/demo.png')
        self.res_img = self.img.resize((200, 200))
        self.image = ImageTk.PhotoImage(self.res_img)
        self.preview.configure(image=self.image)
