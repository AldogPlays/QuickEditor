# ✂️ Quick Editor

Quick Editor is a simple image cropper designed to allow you to quickly edit and crop multiple images using predefined cropping presets. The app provides a fast and intuitive interface for batch-editing images, with dynamic zoom and manual crop box adjustments.

## 🌟 Features

- **📂 Batch Image Editing**: Select a folder containing images and quickly edit all images in the folder.
- **📐 Cropping Presets**: Choose from multiple cropping presets:
  - 16:9 (Horizontal)
  - 9:16 (Vertical)
  - 4:3 (Horizontal)
  - 3:4 (Vertical)
  - 1:1 (Square)
  - 21:9 (Cinematic)
- **🔧 Manual Adjustments**:
  - ➡️ Move the crop area with arrow keys.
  - 🔍 Resize the crop box using the `+` and `-` keys or the mouse scroll wheel.
  - 🔬 Choose zoom granularity for finer control over cropping.
- **📏 Guidelines**: Display rule-of-thirds and center guidelines within the crop box to help you adjust your crops perfectly.
- **💾 Save Edits**: Save all edited images to a new folder named after the original folder with `_edited` appended.
- **📂 Auto Folder Opening**: After the app closes, it automatically opens the folder where the original images are located.

## ⚙️ Installation

### 📋 Prerequisites

- 🐍 Python 3.x
- 🖼️ `Pillow` for image handling (`PIL`)
- 🖥️ `Tkinter` (should come pre-installed with Python)

### 🛠️ Install Dependencies

You can install dependencies using `pip`. Open your terminal or command prompt and run the following command:

```bash
pip install pillow
```

### 🚀 Running the App

1. Clone or download the Quick Editor repository to your local machine.
2. Navigate to the project directory.
3. Run the application with Python:

```bash
python main.py
```

## 🖼️ Usage

1. **🗂️ Select Folder**: After launching Quick Editor, click the "Select Folder" button to choose a folder containing the images you want to edit.
2. **✂️ Crop Presets**: Use number keys `1` through `6` to select a cropping preset:
   - `1`: 16:9 (Horizontal)
   - `2`: 9:16 (Vertical)
   - `3`: 4:3 (Horizontal)
   - `4`: 3:4 (Vertical)
   - `5`: 1:1 (Square)
   - `6`: 21:9 (Cinematic)
3. **📏 Adjust Crop Box**: Use arrow keys to move the crop box and `+` or `-` to resize the box. The mouse scroll wheel can also be used to zoom the crop box in or out.
4. **📐 Guidelines**: Guidelines will appear within the crop box for better composition alignment (rule of thirds and center lines).
5. **💾 Save and Proceed**: Press `Enter` to save the cropped image and move to the next image in the folder.
6. **❌ Exit Fullscreen**: Press `Esc` to exit fullscreen mode at any time.

### ⌨️ Key Bindings

| Key | Action |
| --- | ------ |
| `1` to `6` | Select crop preset |
| ⬅️ ➡️ 🔼 🔽 | Move crop box (left, right, up, down) |
| `+` / `-` | Resize crop box (zoom in / zoom out) |
| 🖱️ `Mouse Scroll` | Resize crop box (zoom in / zoom out) |
| 🔑 `Enter` | Save cropped image and move to next image |
| ❌ `Esc` | Exit fullscreen mode |

## 📂 Folder Structure

When you select a folder containing images, the edited images will be saved to a subfolder of the same name with `_edited` appended.

For example:
- Original folder: `VacationPhotos`
- Edited folder: `VacationPhotos_edited`

## 🛠️ Troubleshooting

### ⚠️ Issue: The app closes but doesn’t open the folder

Ensure that you have correctly selected a folder, and make sure you have Python’s `os.startfile()` functionality supported on your operating system (primarily works on Windows).
