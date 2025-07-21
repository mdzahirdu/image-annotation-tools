
# 🖼️ Image Annotation Tools (Manual Drawing)

This repository provides **manual image annotation tools** written in Python using OpenCV. These tools allow users to annotate images by **drawing rectangular boxes or free-form polygons**, and save the annotations in YOLO or LabelMe-compatible formats.

---

## 📁 Project Structure

- `draw_rectangle.py`  
  Annotate using rectangular bounding boxes (saved as `.txt` in YOLO format)

- `draw_polygon.py`  
  Annotate using free-form polygons (saved as `.json` in LabelMe format)

---

## 🧰 Requirements

Install required packages:

```
pip install -r requirements.txt
```

---

## 🖱️ Rectangle Tool Instructions

```bash
python draw_rectangle.py
```

- Left-click + drag = Draw box  
- Press `c` = Confirm and save  
- Press `r` = Reset current image  
- Press `q` = Quit without saving  

---

## 🧭 Polygon Tool Instructions

```bash
python draw_polygon.py
```

- Click = Add a point  
- Press `n` = Finish polygon and input label  
- Press `s` or `Enter` = Save all shapes  
- Press `r` = Reset all  
- Press `q` = Quit  

---

## 📂 Input/Output

- Input: `images/` folder  
- Output:  
  - `label/` for YOLO  
  - `polygon_label/` for polygons

---

## 📜 License

MIT License

---

## 🙋‍♂️ Author

[mdzahirdu](https://github.com/mdzahirdu)
