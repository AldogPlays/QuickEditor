import os
import atexit
from tkinter import Tk, filedialog, Canvas, Button, Label, Frame
from tkinter import StringVar
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
        self.source_folder = None  # Store the source folder path
        self.edits_folder = None  # Store the folder for edited images

        # Initialize UI variables
        self.crop_info = StringVar()
        self.image_info = StringVar()

        # Get the screen resolution
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Load UI elements
        self.canvas = Canvas(self.root, width=self.screen_width, height=self.screen_height, bg="#2D2D2D")
        self.canvas.pack()

        # Create a header frame
        self.header_frame = Frame(self.root, bg="#3B3B3B", bd=2, relief="flat", padx=10, pady=10)
        self.header_frame.place(relx=0.5, rely=0.05, anchor='center')

        # Add title to header
        self.title_label = Label(self.header_frame, text="Image Cropper", font=("Roboto", 18, "bold"), fg="white", bg="#3B3B3B")
        self.title_label.pack()

        # Create a GUI overlay frame for controls
        self.overlay_frame = Frame(self.root, bg="#3B3B3B", bd=2, relief="flat", padx=10, pady=10)
        self.overlay_frame.place(relx=0.5, rely=0.9, anchor='center')

        # Style buttons with modern design
        button_style = {"bg": "#3A85FF", "fg": "white", "font": ("Roboto", 12), "relief": "flat", "bd": 0, "width": 12, "height": 2}

        # Add buttons to the overlay frame
        self.next_button = Button(self.overlay_frame, text="Next", command=self.save_and_next_image, **button_style)
        self.next_button.pack(side="left", padx=10)

        self.exit_button = Button(self.overlay_frame, text="Exit Fullscreen", command=self.exit_fullscreen, **button_style)
        self.exit_button.pack(side="left", padx=10)

        self.load_button = Button(self.overlay_frame, text="Select Folder", command=self.load_folder, **button_style)
        self.load_button.pack(side="left", padx=10)

        # Add dynamic labels for crop info and image info
        self.crop_info_label = Label(self.overlay_frame, textvariable=self.crop_info, bg="#3B3B3B", fg="white", font=("Roboto", 12))
        self.crop_info_label.pack(side="left", padx=20)

        self.image_info_label = Label(self.overlay_frame, textvariable=self.image_info, bg="#3B3B3B", fg="white", font=("Roboto", 12))
        self.image_info_label.pack(side="left", padx=20)

        # Bind arrow keys, Enter, plus/minus keys for crop resizing
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.save_and_next_image)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("+", self.increase_crop_size)
        self.root.bind("-", self.decrease_crop_size)

        # Bind mouse scroll to resize crop box
        self.canvas.bind("<MouseWheel>", self.handle_scroll)

        # Bind number keys 1-6 for different crop presets
        for i in range(1, 7):
            self.root.bind(str(i), self.set_crop_preset)

        # Bind exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Register the exit handler with atexit (pass source_folder from the instance)
        atexit.register(self.on_atexit)

    def load_folder(self):
        # Let user select a folder and load all image paths from it
        folder = filedialog.askdirectory()
        if folder:
            self.images = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.source_folder = folder  # Store the selected folder

            # Get the parent folder name and append '_edited'
            parent_folder_name = os.path.basename(self.source_folder)
            self.edits_folder = os.path.join(self.source_folder, f"{parent_folder_name}_edited")

            # Create the folder for edited images if it doesn't exist
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

        # Draw guidelines centered in the crop area
        self.draw_guidelines()

        # Update crop information dynamically
        self.update_crop_info()

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

    def draw_guidelines(self):
        # Draw guidelines centered in the crop box
        x1, y1, x2, y2 = self.crop_box
        width = x2 - x1
        height = y2 - y1

        # Calculate thirds
        third_width = width / 3
        third_height = height / 3

        # Vertical guidelines (thirds and center)
        self.canvas.create_line(x1 + third_width, y1, x1 + third_width, y2, fill='white', dash=(4, 2))  # Left third
        self.canvas.create_line(x1 + 2 * third_width, y1, x1 + 2 * third_width, y2, fill='white', dash=(4, 2))  # Right third
        self.canvas.create_line((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, fill='white', dash=(4, 2))  # Center line

        # Horizontal guidelines (thirds and center)
        self.canvas.create_line(x1, y1 + third_height, x2, y1 + third_height, fill='white', dash=(4, 2))  # Top third
        self.canvas.create_line(x1, y1 + 2 * third_height, x2, y1 + 2 * third_height, fill='white', dash=(4, 2))  # Bottom third
        self.canvas.create_line(x1, (y1 + y2) / 2, x2, (y1 + y2) / 2, fill='white', dash=(4, 2))  # Center line

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
        # Increase the size of the crop box (granular zoom)
        self.resize_crop_box(1.05)  # Adjusted for smaller zoom increments

    def decrease_crop_size(self, event):
        # Decrease the size of the crop box (granular zoom)
        self.resize_crop_box(0.95)  # Adjusted for smaller zoom increments

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
        # Handle mouse scroll to resize crop box (inverted scroll behavior)
        if event.delta > 0:
            self.decrease_crop_size(None)  # Scroll up decreases size
        else:
            self.increase_crop_size(None)  # Scroll down increases size

    def save_and_next_image(self, event=None):
        # Save the cropped image to the edited folder and proceed to the next image
        if self.current_image_index < len(self.images):
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
                # If no more images, update the label and stop
                self.status_label.config(text="All images processed!")
        else:
            # If the index is already out of range, stop processing
            self.status_label.config(text="No more images to process!")

    def update_status(self):
        # Update the status label with current image index, crop preset, and total images
        preset_name = f"Preset {self.current_preset}: {self.crop_presets[self.current_preset][0]}:{self.crop_presets[self.current_preset][1]}"
        self.image_info.set(f"Image {self.current_image_index + 1} of {len(self.images)} | {preset_name}")

    def update_crop_info(self):
        # Display crop dimensions and aspect ratio
        x1, y1, x2, y2 = self.crop_box
        width = x2 - x1
        height = y2 - y1
        aspect_ratio = width / height if height != 0 else 0
        self.crop_info.set(f"Crop: {width}x{height} | Aspect Ratio: {aspect_ratio:.2f}")

    def set_crop_preset(self, event):
        # Set the crop preset based on the number key pressed
        self.current_preset = int(event.char)
        self.set_initial_crop_box()
        self.display_image()
        self.update_status()  # Ensure the status is updated when preset changes

    def exit_fullscreen(self, event=None):
        # Exit fullscreen mode when the Escape key or button is pressed
        self.root.attributes('-fullscreen', False)

    def on_close(self):
        # Open the parent folder on close
        if self.source_folder:
            os.startfile(self.source_folder)
        self.root.destroy()

    def on_atexit(self):
        # Called during atexit to open the source folder if available
        if self.source_folder:
            os.startfile(self.source_folder)

if __name__ == "__main__":
    root = Tk()
    app = CropperApp(root)
    root.mainloop()