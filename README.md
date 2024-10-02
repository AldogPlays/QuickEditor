# ✂️ QuickEditor v1.0

**QuickEditor** is a fast, lightweight image cropper designed for batch-editing multiple images using predefined cropping presets. With an intuitive interface, it allows you to zoom, manually adjust crop boxes, and save images with ease.

## 🌟 Features

- **📂 Batch Image Editing**: Edit entire folders of images in just a few clicks.
- **📐 Cropping Presets**: Choose from six aspect ratio presets:
  - 16:9 (Horizontal)
  - 9:16 (Vertical)
  - 4:3 (Horizontal)
  - 3:4 (Vertical)
  - 1:1 (Square)
  - 21:9 (Cinematic)
- **🔧 Manual Adjustments**:
  - ➡️ Move the crop area using arrow keys.
  - 🔍 Resize the crop box with `+` and `-` keys or the mouse scroll wheel.
  - 🔬 Fine-tune zoom and cropping with precise controls.
- **📏 Guidelines**: Rule-of-thirds and center guidelines for better composition.
- **💾 Smart Save**:
  - Press `Enter` to save the current crop and move to the next image.
  - Press `S` to save without moving to the next image.
  - Each saved image has an automatic version number starting at `_v1`.
- **📂 Auto Folder Management**: Edited images are automatically saved in a subfolder with `_edited` appended to the original folder.
- **📂 Auto Folder Opening**: After closing the app, the source folder of the images opens automatically.

## 📸 Cropping Examples

Here are two examples showcasing how images are cropped using QuickEditor:

### Example 1: Cropping to 16:9 Aspect Ratio

![16:9 Crop Example](images/screenshot1.png)  
*This image is cropped using the 16:9 horizontal preset with rule-of-thirds guidelines.*

### Example 2: Cropping to 4:3 Aspect Ratio

![4:3 Crop Example](images/screenshot2.png)  
*This image is cropped using the 4:3 horizontal preset with composition guidelines.*

## 🚀 Latest Release: QuickEditor v1.0

The first official release of **QuickEditor v1.0** is now live! It includes all the essential features for fast, efficient image cropping. You can download it directly from the **[Releases](https://github.com/AldogPlays/QuickEditor/releases)** page.

### How to Use the v1.0 Release:
1. **Download** the `QuickEditor.exe` from the release page.
2. **Run** the `QuickEditor.exe`—no installation required!
3. Start cropping your images right away.

## ⚙️ Installation (For Source Code Users)

### 📋 Prerequisites

- 🐍 Python 3.x
- 🖼️ `Pillow` (PIL) for image handling
- 🖥️ `Tkinter` (comes pre-installed with Python)

### 🛠️ Install Dependencies

You can install dependencies with `pip` by running the following command in your terminal:

```bash
pip install pillow
```

### 🚀 Running the App from Source

1. Clone or download the QuickEditor repository to your machine.
2. Navigate to the project directory.
3. Run the application using Python:

```bash
python main.py
```

## 🖼️ Usage Guide

1. **🗂️ Select Folder**: Click "Select Folder" and choose the folder containing your images.
2. **✂️ Crop Presets**: Use keys `1` through `6` to select a crop preset:
   - `1`: 16:9 (Horizontal)
   - `2`: 9:16 (Vertical)
   - `3`: 4:3 (Horizontal)
   - `4`: 3:4 (Vertical)
   - `5`: 1:1 (Square)
   - `6`: 21:9 (Cinematic)
3. **📏 Adjust Crop Box**: Move the crop box with arrow keys and resize it with `+` or `-`. Mouse scroll for zooming in/out.
4. **📐 Guidelines**: Use rule-of-thirds and center guidelines for perfect alignment.
5. **💾 Save**: Press `Enter` to save and move to the next image, or `S` to save without moving to the next.
6. **❌ Exit Fullscreen**: Press `Esc` at any time to exit fullscreen mode.

### ⌨️ Key Bindings

| Key | Action |
| --- | ------ |
| `1` to `6` | Select crop preset |
| ⬅️ ➡️ 🔼 🔽 | Move crop box (left, right, up, down) |
| `+` / `-` | Resize crop box (zoom in / zoom out) |
| 🖱️ `Mouse Scroll` | Resize crop box (zoom in / zoom out) |
| 🔑 `Enter` | Save and move to the next image |
| `S` | Save without moving to the next image |
| `N` | Skip to the next image without saving |
| ❌ `Esc` | Exit fullscreen mode |

## 📂 Folder Structure

When you select a folder, edited images are saved in a subfolder with `_edited` appended to the folder name.

Example:
- Original folder: `VacationPhotos`
- Edited folder: `VacationPhotos_edited`

Each image will have a version suffix (`_v1`, `_v2`, etc.):

- `image_v1.png`
- `image_v2.png`

## 🛠️ Troubleshooting

### ⚠️ Issue: The app closes but doesn’t open the folder

Make sure you’ve selected the correct folder. On non-Windows systems, `os.startfile()` may not be supported, so you may need to manually navigate to the folder.

---

Check out the **[Releases](https://github.com/AldogPlays/QuickEditor/releases)** page for the latest version and future updates!