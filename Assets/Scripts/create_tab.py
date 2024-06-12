import customtkinter as ctk
import Assets.Scripts.variables as vary
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import segno


class CreateTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=vary.colors[3])
        vary.create_tab = self

        self.input_frame = ctk.CTkFrame(master=self, fg_color=vary.colors[3], corner_radius=5)
        self.output_frame = ctk.CTkFrame(master=self, fg_color=vary.colors[3], corner_radius=5)

        # input frame widgets
        self.lbl = ctk.CTkLabel(master=self.input_frame, text='Create', font=('segio', 30), corner_radius=5)
        self.lbl_1 = ctk.CTkLabel(
            master=self.input_frame, text='  Enter the data:', font=('segio', 15)
        )
        self.entry = ctk.CTkTextbox(
            master=self.input_frame, width=(vary.width - 28) / 2, height=160, undo=True,
            activate_scrollbars=False
        )
        self.generate_btn = ctk.CTkButton(
            master=self.input_frame, width=(vary.width - 30) / 2, height=30, text='Generate'
        )

        # output frame widgets
        self.space_out = ctk.CTkLabel(master=self.output_frame, text='', height=10, corner_radius=5)
        self.output_field = ctk.CTkLabel(
            master=self.output_frame, width=(vary.width - 65) / 2, height=219, corner_radius=5, text='', image=''
        )
        self.clear_btn = ctk.CTkButton(master=self.output_frame, text='Clear')
        self.save_btn = ctk.CTkButton(master=self.output_frame, text='Save')

        self.clear_btn.bind('<Button-1>', self.clear_btn_action)
        self.generate_btn.bind('<Button-1>', self.generate_btn_action)
        self.save_btn.bind('<Button-1>', self.save_btn_action)

        array_one = [
            self.lbl, self.lbl_1, self.space_out
        ]

        array_two = [
            self.entry, self.output_field
        ]

        array_three = [
            self.clear_btn, self.save_btn
        ]

        array_four = [
            self.clear_btn, self.generate_btn, self.save_btn
        ]

        for i in array_one:
            i.configure(anchor='w', width=(vary.width - 20) / 2)

        for i in array_two:
            i.configure(font=('segio', 12))

        for i in array_three:
            i.configure(width=(((vary.width - 65) / 2) / 2) - 10, height=30)

        for i in array_four:
            i.configure(fg_color=vary.colors[0], hover_color=vary.colors[1])
            i.configure(font=('segio', 15))

        self.input_frame.grid(row=0, column=0)
        self.output_frame.grid(row=0, column=1)

        self.lbl.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.lbl_1.grid(row=1, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.entry.grid(row=2, column=0, pady=5)
        self.generate_btn.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        self.space_out.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.output_field.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.save_btn.grid(row=2, column=0, padx=5, pady=5)
        self.clear_btn.grid(row=2, column=1, padx=5, pady=5)

    def generate_btn_action(self, event):
        data = self.entry.get('0.0', ctk.END)
        if data != '\n':
            qr = segno.make_qr(data)
            qr.save(
                out=f'Assets/QRs/qr_{vary.number}.png',
                scale=10,
                border=2,
                light=vary.colors[4],
                dark=vary.colors[5]
            )
            self.img = Image.open(f'Assets/QRs/qr_{vary.number}.png')
            self.res_img = self.img.resize((200, 200))
            self.image = ImageTk.PhotoImage(self.res_img)
            self.output_field.configure(image=self.image)
            vary.number += 1
            txt = open('Assets/Data/number.txt', 'w')
            txt.write(f'{vary.number}')

    def clear_btn_action(self, event):
        self.entry.delete('0.0', ctk.END)
        self.output_field.configure(image='')

    def save_btn_action(self, event):
        if self.output_field.cget('image') != '':
            photo = Image.open(f'Assets/QRs/qr_{vary.number-1}.png')
            try:
                f = fd.asksaveasfile(initialfile='QR_Scanner.png', defaultextension=".png",
                                     filetypes=[
                                         ("PNG image", "*.png"), ("JPG image", "*.jpg"), ("All image files", "*.*")
                                     ])
                if not f:
                    return
                else:
                    photo.save(f.name)

            except Exception as e:
                print(e)

