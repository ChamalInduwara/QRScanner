import customtkinter as ctk
import Assets.Scripts.variables as vary
import tkinter.filedialog as fd
import cv2
from PIL import Image, ImageTk


class ScanTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=vary.colors[3])
        vary.scan_tab = self

        self.input_frame = ctk.CTkFrame(master=self, fg_color=vary.colors[3], corner_radius=5)
        self.output_frame = ctk.CTkFrame(master=self, fg_color=vary.colors[3], corner_radius=5)

        self.img = Image.open(f'Assets/Images/open.png')
        self.res_img = self.img.resize((25, 25))
        self.image = ImageTk.PhotoImage(self.res_img)

        # input frame widgets
        self.lbl = ctk.CTkLabel(master=self.input_frame, text='Scan', font=('segio', 30), corner_radius=5)
        self.space_inp = ctk.CTkLabel(master=self.input_frame, text='', height=20)
        self.space_inp_1 = ctk.CTkLabel(master=self.input_frame, text='', height=90)
        self.lbl_1 = ctk.CTkLabel(
            master=self.input_frame, text='  Choose the location of the QR Code:', font=('segio', 15)
        )
        self.entry = ctk.CTkEntry(master=self.input_frame, width=((vary.width - 20) / 2) - 60, height=30)
        self.choose_btn = ctk.CTkButton(master=self.input_frame, width=30, height=30, text='', image=self.image)
        self.scan_btn = ctk.CTkButton(master=self.input_frame, width=(vary.width - 30) / 2, height=30, text='Scan')

        # output frame widgets
        self.space_out = ctk.CTkLabel(master=self.output_frame, text='', height=10, corner_radius=5)
        self.output_field = ctk.CTkTextbox(
            master=self.output_frame, width=(vary.width - 65) / 2, height=219, corner_radius=5,
            activate_scrollbars=False, state='disabled'
        )
        self.clear_btn = ctk.CTkButton(master=self.output_frame, text='Clear')
        self.copy_btn = ctk.CTkButton(master=self.output_frame, text='Copy')

        self.choose_btn.bind('<Button-1>', self.choose_btn_action)
        self.scan_btn.bind('<Button-1>', self.scan_btn_action)
        self.clear_btn.bind('<Button-1>', self.clear_btn_action)
        self.copy_btn.bind('<Button-1>',
                           lambda: self.clipboard_append(self.output_field.get('0.0', ctk.END)))

        array_one = [
            self.lbl, self.lbl_1, self.space_inp, self.space_out, self.space_inp_1
        ]

        array_two = [
            self.entry, self.output_field
        ]

        array_three = [
            self.clear_btn, self.copy_btn
        ]

        array_four = [
            self.clear_btn, self.scan_btn, self.copy_btn, self.choose_btn
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
        self.space_inp.grid(row=1, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.lbl_1.grid(row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.entry.grid(row=3, column=0, pady=5)
        self.choose_btn.grid(row=3, column=1, pady=5)
        self.space_inp_1.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
        self.scan_btn.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        self.space_out.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.output_field.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.copy_btn.grid(row=2, column=0, padx=5, pady=5)
        self.clear_btn.grid(row=2, column=1, padx=5, pady=5)

    def clear_btn_action(self, event):
        self.output_field.configure(state='normal')
        self.output_field.delete('0.0', ctk.END)
        self.output_field.configure(state='disabled')
        self.entry.delete('0', ctk.END)

    def scan_btn_action(self, event):
        img = cv2.imread(self.entry.get())
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)

        if bbox is not None:
            txt = data
        else:
            txt = 'No QR Code'

        self.output_field.configure(state='normal')
        self.output_field.delete('0.0', ctk.END)
        self.output_field.insert('0.0', txt)
        self.output_field.configure(state='disabled')

    def choose_btn_action(self, event):
        try:
            filetypes = (
                ('PNG image', '*.png'),
                ('JPG image', '*.jpg'),
                ('All image files', '*.*')
            )

            f = fd.askopenfile(filetypes=filetypes)
            self.entry.delete('0', ctk.END)
            self.entry.insert('0', f.name)

        except Exception as e:
            print(e)
