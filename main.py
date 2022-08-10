from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox

from logic import Logic

logic = Logic()


class GUI:
    def __init__(self):
        # Variables for TKinter to use to display images / text
        self.image = None
        self.thumbnail = None
        self.image_filepath = None
        self.watermark_thumbnail = None
        self.watermark_filepath = None
        self.watermark = None

        self.root = Tk()
        self.root.title("Watermark Generator")

        self.root.minsize(1200, 900)
        self.root_frame = Frame(width=1200, height=900)
        self.root_frame.pack()
        self.root_frame.grid_columnconfigure(0, minsize=800)
        self.root_frame.grid_columnconfigure(1, minsize=400)
        self.root_frame.grid_rowconfigure(1, minsize=800)


        # PRIMARY DISPLAY FRAME ELEMENTS
        self.logo = Label(self.root_frame, text="Watermark Generator", font="Monaco 50", )
        self.logo.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        self.picture_frame = Frame(self.root_frame, padding=10, width=900, height=800)
        self.picture_frame.grid(row=1, column=0, )
        self.picture_frame.grid_rowconfigure(0, minsize=800)

        self.buttons_frame = Frame(self.root_frame, padding=10, width=300, border=1, relief="raised", borderwidth=1)
        self.buttons_frame.grid(row=1, column=1)
        self.buttons_frame.grid_columnconfigure(0, minsize=300)
        self.buttons_frame.grid_rowconfigure(0, minsize=300)
        self.buttons_frame.grid_rowconfigure(1, minsize=100)
        self.buttons_frame.grid_rowconfigure(2)
        self.buttons_frame.grid_rowconfigure(5, minsize=300)


        #############    BUTTON FRAME ELEMENTS  ####################

        # WATERMARK DISPLAY AREA
        self.watermark_frame = Frame(self.buttons_frame, borderwidth=1 )
        self.watermark_frame.grid(row=0, column=0,)
        self.watermark_display = Label(self.watermark_frame)
        self.watermark_display.pack()
        self.watermark_path = Label(self.watermark_frame, font=('Arial', 10, ''))
        self.watermark_path.pack()

        # WATERMARK OPTIONS AREA

        self.watermark_open = Button(self.buttons_frame, state="disabled", command=self.open_watermark, text="Watermark from file", width=15,)
        self.watermark_open.grid(row=1, column=0, pady=(0,20))


        self.watermark_text_entry = Entry(self.buttons_frame, width=18)
        self.watermark_text_entry.grid(row=2, column=0, pady=(20, 0), )
        self.watermark_text_btn = Button(self.buttons_frame, state="disabled", text="Watermark from text", command=self.watermark_from_text, width=15)
        self.watermark_text_btn.grid(row=3, column=0, pady=(0, 20))

        self.watermark_options_frame = Frame(self.buttons_frame, padding=(0, 0, 0, 0), borderwidth=3, relief="raised", border=2)

        # ______WATERMARK OPTIONS _____
        self.watermark_options_label = Label(self.watermark_options_frame, text="Watermark Options: ", font=("Arial 20 bold"))
        self.watermark_options_label.grid(row=2, column=0)

        # WATERMARK SIZE
        self.watermark_size = StringVar()
        self.watermark_size.set("Medium")
        self.watermark_location_label = Label(self.watermark_options_frame, text="Watermark size:", )
        self.watermark_location_label.grid(row=3, column=0, pady=(15, 5))
        self.watermark_size_frame = Frame(self.watermark_options_frame)
        self.watermark_size_frame.grid(row=4, column=0)
        self.watermark_size_choices_large = Radiobutton(self.watermark_size_frame, variable=self.watermark_size,
                                                        value="Large", text="Lg")
        self.watermark_size_choices_large.grid(row=0, column=0, padx=2)
        self.watermark_size_choices_med = Radiobutton(self.watermark_size_frame, variable=self.watermark_size,
                                                      value="Medium", text="Med")
        self.watermark_size_choices_med.grid(row=0, column=1, padx=2)
        self.watermark_size_choices_small = Radiobutton(self.watermark_size_frame, variable=self.watermark_size,
                                                        value="Small", text="Sm")
        self.watermark_size_choices_small.grid(row=0, column=2, padx=2)

        # WATERMARK LOCATION
        self.watermark_location_label = Label(self.watermark_options_frame, text="Watermark Location:", )
        self.watermark_location_label.grid(row=7, column=0, pady=(15, 5))
        self.watermark_location_choices = ['Center', 'Top-Left', 'Top-Right', 'Bottom-Left', 'Bottom-Right']
        self.watermark_location_choicesvar = StringVar(value=self.watermark_location_choices)
        self.watermark_location_listbox = Listbox(self.watermark_options_frame,
                                                  listvariable=self.watermark_location_choicesvar,
                                                  height=len(self.watermark_location_choices),
                                                  width=15,
                                                  selectmode="multiple")
        self.watermark_location_listbox.grid(row=8, column=0)
        # self.watermark_location_listbox.bind("<<ListboxSelect>>", lambda x: self.watermark_image())
        self.watermark_add_button = Button(self.watermark_options_frame, command=self.watermark_image, text="Add Watermark", width=15)
        self.watermark_add_button.grid(row=9, column=0)
        self.batch_process_btn = Button(self.watermark_options_frame, command=self.batch_process, text="Directory Batch Process")
        self.batch_process_btn.grid(row=10, column=0, pady=10)

        # IMAGE LOAD AREA
        self.load_btn = Button(self.picture_frame, command=lambda: self.open_file(), text="Open File")
        self.load_btn.grid(row=2, column=0, padx=10)

        # IMAGE SAVE AREA
        self.save_btn = Button(self.picture_frame, state="disabled", command=self.save_file, text="Save File")
        self.save_btn.grid(row=2, column=1, padx=10)

        self.watermark_clear = Button(self.picture_frame, state="disabled", command=lambda: self.open_file(refresh=True),
                                      text="Clear Watermark",)

        self.watermark_clear.grid(row=2, column=2, padx=10)

        # IMAGE FRAME ELEMENTS
        self.img_display = Label(self.picture_frame)
        self.img_display.grid(row=0, column=0, columnspan=3)
        self.img_filepath = Label(self.picture_frame)
        self.img_filepath.grid(row=1, column=0, columnspan=3)

        messagebox.showinfo("How to use", "1. Use Open File to load an image\n\n"
                                          "2. Choose a file watermark or generate one from text\n\n"
                                          "3. Select size and location(s) for watermark\n\n"
                                          "4. Save File or bath process to watermark all images in current directory")





    def open_file(self, refresh=False):

        # Call logic.open_file to get thumbnail and image_filepath
        if not refresh:
            self.image_filepath = filedialog.askopenfilename()
        try:
            self.thumbnail, self.image_filepath = logic.open_file(self.image_filepath)
        except:
            return
        # Send to display
        self.display_image()
        self.save_btn["state"] = "!disabled"
        self.watermark_clear["state"] = "!disabled"
        self.watermark_open['state'] = "!disabled"
        self.watermark_text_btn['state'] = "!disabled"

    def open_watermark(self):
        if not self.watermark_filepath:
            self.watermark_filepath = filedialog.askopenfilename()
        try:
            self.watermark_thumbnail, self.watermark_filepath, self.watermark = logic.open_watermark(self.watermark_filepath)
        except:
            messagebox.showinfo("Error", "Load image file first")
            return
        self.watermark_display.configure(anchor=CENTER, image=self.watermark_thumbnail)
        self.watermark_path.configure(text=self.watermark_filepath)
        self.watermark_options_frame.grid(row=5, column=0)

    def watermark_image(self):
        locations = list(self.watermark_location_listbox.curselection())
        size = self.watermark_size.get()
        self.image = logic.watermark_image(locations, size)
        self.thumbnail, self.image_filepath = logic.display_image()
        self.display_image()

    def watermark_from_text(self):
        text = self.watermark_text_entry.get()
        if not text:
            messagebox.showinfo("Error", "Cannot Be blank")
            return
        try:
            self.image, self.image_filepath, self.watermark_filepath = logic.create_text_watermark(text)
            self.thumbnail, self.image_filepath = logic.display_image()
            self.open_watermark()
            self.display_image()
        except TypeError as e:
            messagebox.showerror("Error", "Error.\nPlease 'Open File' first")


    def display_image(self):
        # display image. This is called by a number of other methods to update image.
        # make sure that self.thumbnail and self.image_filepath are correctly updated before calling
        self.img_display.configure(anchor=NW, image=self.thumbnail)
        self.img_filepath.configure(text=self.image_filepath)

    def save_file(self):
        try:
            logic.save_file()
            messagebox.showinfo("Save Success", "Saved to '/processed' directory")
        except Exception as e:
            messagebox.showinfo("Save failed", f"Save Failed. \n\nError code: \n {e.args}")

    def batch_process(self):
        try:
            logic.batch_process()
            messagebox.showinfo("Batch Process", "Batch saved to '/processed' directory")
        except Exception as e:
            messagebox.showinfo("Batch Process", f"Failed: \n\n {e.args}")

    def disable_toggle(self, element):
        if element['state'] == "disabled":
            element['state'] =="!disabled"
        elif element['state'] == "!disabled":
            element['state'] == "disabled"


gui = GUI()
gui.root.mainloop()
