import os
from tkinter import Tk, filedialog, Canvas, Button, Label, Frame
from PIL import Image, ImageTk

class CropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        # Set the window to fullscreen mode
        self.root.attributes('-fullscreen', True)

        # Initialize state variables
        self.images = []
        self.current_image_index = 0
        self.crop_box = None
        self.crop_presets = {
            1: (16, 9),  # Horizontal 16:9
            2: (9, 16),  # Vertical 9:16
            3: (4, 3),   # Horizontal 4:3
            4: (3, 4),   # Vertical 3:4
            5: (1, 1),   # Square 1:1
            6: (21, 9)   # Horizontal cinematic 21:9
        }
        self.current_preset = 1  # Start with preset 1 (16:9)
        self.shift_amount = 10  # Amount of shift per arrow key press

        # Get the screen resolution
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Load UI elements
        self.canvas = Canvas(self.root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()

        # Create a GUI overlay frame
        self.overlay_frame = Frame(self.root, bg="black", bd=2)
        self.overlay_frame.place(relx=0.5, rely=0.9, anchor='center')

        # Add buttons and labels to the overlay frame
        self.next_button = Button(self.overlay_frame, text="Next", command=self.save_and_next_image)
        self.next_button.pack(side="left")

        self.exit_button = Button(self.overlay_frame, text="Exit Fullscreen", command=self.exit_fullscreen)
        self.exit_button.pack(side="left")

        self.status_label = Label(self.overlay_frame, text="", bg="black", fg="white")
        self.status_label.pack(side="left")

        self.load_button = Button(self.overlay_frame, text="Select Folder", command=self.load_folder)
        self.load_button.pack(side="left")

        # Bind arrow keys, Enter, plus/minus keys for crop resizing
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.save_and_next_image)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("+", self.increase_crop_size)
        self.root.bind("-", self.decrease_crop_size)

        # Bind mouse scroll to resize crop box (inverted scroll behavior)
        self.canvas.bind("<MouseWheel>", self.handle_scroll)

        # Bind number keys 1-6 for different crop presets
        for i in range(1, 7):
            self.root.bind(str(i), self.set_crop_preset)

    def load_folder(self):
        # Let user select a folder and load all image paths from it
        folder = filedialog.askdirectory()
        if folder:
            self.images = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.source_folder = folder
            self.edits_folder = os.path.join(self.source_folder, "edits")
            if not os.path.exists(self.edits_folder):
                os.makedirs(self.edits_folder)
            if self.images:
                self.load_image()

    def load_image(self):
        # Load the current image and set the crop box based on its size
        img_path = self.images[self.current_image_index]
        self.original_image = Image.open(img_path)
        self.set_initial_crop_box()  # Set the initial crop box based on the preset
        self.display_image()
        self.update_status()

    def set_initial_crop_box(self):
        # Set the crop box based on the current preset's aspect ratio
        width, height = self.original_image.size
        aspect_ratio = self.crop_presets[self.current_preset]
        new_width = width
        new_height = int(width * aspect_ratio[1] / aspect_ratio[0])

        # Adjust the crop box if it exceeds the image boundaries
        if new_height > height:
            new_height = height
            new_width = int(height * aspect_ratio[0] / aspect_ratio[1])

        # Center the crop box on the image
        x1 = (width - new_width) // 2
        y1 = (height - new_height) // 2
        self.crop_box = (x1, y1, x1 + new_width, y1 + new_height)

    def display_image(self):
        # Display the current image and draw the shaded cropping boxes
        cropped_image = self.original_image

        # Resize image to fit fullscreen while maintaining aspect ratio
        cropped_image.thumbnail((self.screen_width, self.screen_height), Image.LANCZOS)

        # Convert the image to Tkinter format and display it
        self.tk_image = ImageTk.PhotoImage(cropped_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Draw the shaded areas outside the crop box
        self.draw_shaded_areas()

    def draw_shaded_areas(self):
        # Draw shaded areas to represent the crop box
        x1, y1, x2, y2 = self.crop_box
        img_width, img_height = self.original_image.size

        # Scale the crop box to match the resized display image
        display_scale_x = self.screen_width / img_width
        display_scale_y = self.screen_height / img_height
        scaled_crop_box = (x1 * display_scale_x, y1 * display_scale_y, x2 * display_scale_x, y2 * display_scale_y)

        # Clear the canvas before drawing
        self.canvas.delete("all")

        # Draw the image again
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Draw shaded rectangles outside the crop box
        self.canvas.create_rectangle(0, 0, scaled_crop_box[0], self.screen_height, fill='black', stipple='gray50')
        self.canvas.create_rectangle(scaled_crop_box[2], 0, self.screen_width, self.screen_height, fill='black', stipple='gray50')
        self.canvas.create_rectangle(scaled_crop_box[0], 0, scaled_crop_box[2], scaled_crop_box[1], fill='black', stipple='gray50')
        self.canvas.create_rectangle(scaled_crop_box[0], scaled_crop_box[3], scaled_crop_box[2], self.screen_height, fill='black', stipple='gray50')

    def move_left(self, event):
        # Move the crop box left by shift_amount pixels
        self.crop_box = (self.crop_box[0] - self.shift_amount, self.crop_box[1],
                         self.crop_box[2] - self.shift_amount, self.crop_box[3])
        self.display_image()

    def move_right(self, event):
        # Move the crop box right by shift_amount pixels
        self.crop_box = (self.crop_box[0] + self.shift_amount, self.crop_box[1],
                         self.crop_box[2] + self.shift_amount, self.crop_box[3])
        self.display_image()

    def move_up(self, event):
        # Move the crop box up by shift_amount pixels
        self.crop_box = (self.crop_box[0], self.crop_box[1] - self.shift_amount,
                         self.crop_box[2], self.crop_box[3] - self.shift_amount)
        self.display_image()

    def move_down(self, event):
        # Move the crop box down by shift_amount pixels
        self.crop_box = (self.crop_box[0], self.crop_box[1] + self.shift_amount,
                         self.crop_box[2], self.crop_box[3] + self.shift_amount)
        self.display_image()

    def increase_crop_size(self, event):
        # Increase the size of the crop box
        self.resize_crop_box(1.1)

    def decrease_crop_size(self, event):
        # Decrease the size of the crop box
        self.resize_crop_box(0.9)

    def resize_crop_box(self, factor):
        # Resize the crop box by a factor (greater than 1 increases, less than 1 decreases)
        x1, y1, x2, y2 = self.crop_box
        width = x2 - x1
        height = y2 - y1

        new_width = int(width * factor)
        new_height = int(height * factor)

        img_width, img_height = self.original_image.size

        # Ensure the crop box does not exceed the image boundaries
        new_x1 = max(0, x1 - (new_width - width) // 2)
        new_y1 = max(0, y1 - (new_height - height) // 2)
        new_x2 = min(img_width, x2 + (new_width - width) // 2)
        new_y2 = min(img_height, y2 + (new_height - height) // 2)

        self.crop_box = (new_x1, new_y1, new_x2, new_y2)
        self.display_image()

    def handle_scroll(self, event):
        # Inverted mouse scroll: scroll up decreases size, scroll down increases size
        if event.delta > 0:
            self.decrease_crop_size(None)  # Scroll up decreases size
        else:
            self.increase_crop_size(None)  # Scroll down increases size

    def save_and_next_image(self, event=None):
        # Save the cropped image to the edits folder and proceed to the next image
        cropped_image = self.original_image.crop(self.crop_box)
        img_path = self.images[self.current_image_index]
        img_name = os.path.basename(img_path)
        save_path = os.path.join(self.edits_folder, img_name)
        cropped_image.save(save_path)

        # Move to the next image
        self.current_image_index += 1
        if self.current_image_index < len(self.images):
            self.load_image()
        else:
            self.status_label.config(text="All images processed!")

    def update_status(self):
        # Update the status label with current image index, crop preset, and total images
        preset_name = f"Preset {self.current_preset}: {self.crop_presets[self.current_preset][0]}:{self.crop_presets[self.current_preset][1]}"
        self.status_label.config(text=f"Image {self.current_image_index + 1} of {len(self.images)} | {preset_name}")

    def set_crop_preset(self, event):
        # Set the crop preset based on the number key pressed
        self.current_preset = int(event.char)
        self.set_initial_crop_box()
        self.display_image()
        self.update_status()  # Ensure the status is updated when preset changes

    def exit_fullscreen(self, event=None):
        # Exit fullscreen mode when the Escape key or button is pressed
        self.root.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = Tk()
    app = CropperApp(root)
    root.mainloop()