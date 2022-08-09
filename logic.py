from PIL import ImageTk, Image, ImageDraw, ImageFont
import os


class Logic:
    def __init__(self):
        self.image = None
        self.image_filepath = None
        self.thumbnail = None
        self.watermark = None
        self.watermark_thumbnail = None
        self.watermark_filepath = None
        self.watermark_locations = None
        self.watermark_size_selected = None
        self.image_mode = None
        self.directory = None




    def open_file(self, filepath=None):

        self.image_filepath = filepath
        self.directory = os.path.dirname(self.image_filepath)
        self.image = Image.open(self.image_filepath)
        self.image_mode = self.image.mode

        return self.display_image()


    def open_watermark(self, filepath):
        # Open image and create thumbnail to display

        self.watermark_filepath = filepath

        self.watermark = Image.open(self.watermark_filepath)
        self.watermark_thumbnail = self.watermark.copy()
        self.watermark_thumbnail.thumbnail((300, 300))

        # GUI UPDATES
        self.watermark_thumbnail = ImageTk.PhotoImage(self.watermark_thumbnail)
        return self.watermark_thumbnail, self.watermark_filepath, self.watermark

    def create_text_watermark(self, text):

        font = ImageFont.truetype("Arial", 50)
        text_length = int(font.getlength(text) + 10)
        txt = Image.new("RGBA", (text_length, 65), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        draw.text((10,10), text=text, font=font, fill=(255, 255, 255, 128))

        if not os.path.exists(os.path.join(self.directory, 'watermarks')):
            os.mkdir(os.path.join(self.directory, 'watermarks'))
        self.watermark_filepath = os.path.join(self.directory, 'watermarks/text_watermark.png')
        txt.save(self.watermark_filepath, "PNG")

        return self.image, self.image_filepath

    def watermark_image(self, locations, size_selected):
        if locations:
            self.watermark_locations = locations
            self.watermark_size_selected = size_selected
            # Create an image using image and thumbnail
            width, height = self.image.size
            wm_width, wm_height = self.watermark.size
            ratio = (width // 4) // wm_width

            watermark_size_dict = {
                "Large": (wm_width * (ratio*2), wm_height * (ratio*2)),
                "Medium": (wm_width * ratio, wm_height * ratio),
                "Small": (wm_width * (ratio//2), wm_height * (ratio//2))
            }


            watermark = self.watermark.resize(watermark_size_dict[self.watermark_size_selected])
            watermark_width, watermark_height = watermark.size
            draw = ImageDraw.Draw(self.image)


            location_dict = {
                "Center": ((width//2)-(watermark_width//2), (height//2)-(watermark_height//2)),
                "Top-Left": (0, 0),
                "Top-Right": (width - watermark_width, 0),
                "Bottom-Left": (0, height - watermark_height),
                "Bottom-Right": (width - watermark_width, height - watermark_height)
            }

            location_keys = list(location_dict.keys())

            for x in self.watermark_locations:
                draw.bitmap(xy=location_dict[location_keys[x]], bitmap=watermark)

            return self.image, self.image_filepath

    def display_image(self):
        thumbnail = self.image.copy()
        thumbnail.thumbnail((800, 800))
        thumbnail = ImageTk.PhotoImage(image=thumbnail)

        return thumbnail, self.image_filepath

    def batch_process(self):
        try:
            files = os.listdir(self.directory)
            for x in files:
                full_path = os.path.join(self.directory, x)
                if x[0] == '.':
                    continue
                if os.path.isdir(full_path):
                    continue
                if Image.open(full_path).format:
                    self.open_file(filepath=full_path)
                    self.watermark_image(locations=self.watermark_locations, size_selected=self.watermark_size_selected)
                    self.save_file()
            return True
        except Exception as e:
            return False, e


    def save_file(self):
        current_dir = "/".join(self.image_filepath.split("/")[:-1])
        filename = self.image_filepath.split('/')[-1]
        save_path = os.path.join(current_dir, 'processed')
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        self.image.save(os.path.join(save_path, filename), format='JPEG')