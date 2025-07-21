import cv2
import os
import glob
import numpy as np
import json

# === PARAMETERS ===
input_folder = r"J:\IJCB_paper_face1st_data_May_25\YOLOv_final\draw_annotation_manually\images"
output_folder = r"J:\IJCB_paper_face1st_data_May_25\YOLOv_final\draw_annotation_manually\polygon_label"
os.makedirs(output_folder, exist_ok=True)

scale = 0.2
zoom_step = 0.1
min_zoom = 0.1
max_zoom = 5.0
line_thickness = 2

# === IMAGE LIST (deduplicated) ===
image_list_raw = glob.glob(os.path.join(input_folder, "*.jpg")) + \
                 glob.glob(os.path.join(input_folder, "*.JPG"))
image_dict = {}
for path in image_list_raw:
    key = os.path.basename(path).lower()
    if key not in image_dict:
        image_dict[key] = path
image_list = list(image_dict.values())
print(f"🔍 Found {len(image_list)} unique images to annotate.")

def annotate_image(image_path):
    zoom = scale
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return

    orig_h, orig_w = image.shape[:2]
    base_name = os.path.basename(image_path)

    shapes = []          # Store all polygons for this image
    current_polygon = [] # Current polygon being drawn

    def get_scaled_image():
        return cv2.resize(image, (0, 0), fx=zoom, fy=zoom)

    def redraw():
        temp = get_scaled_image().copy()
        # Draw existing polygons
        for shape in shapes:
            pts = np.array(shape['points'], np.int32)
            cv2.polylines(temp, [pts], isClosed=True, color=(0, 0, 255), thickness=line_thickness)
        # Draw current polygon
        for i, (x, y) in enumerate(current_polygon):
            cv2.circle(temp, (int(x), int(y)), 3, (0, 255, 0), -1)
            if i > 0:
                cv2.line(temp, (int(current_polygon[i - 1][0]), int(current_polygon[i - 1][1])),
                         (int(x), int(y)), (255, 0, 0), line_thickness)
        cv2.imshow("Polygon Annotation", temp)

    def mouse_handler(event, x, y, flags, param):
        nonlocal zoom
        if event == cv2.EVENT_LBUTTONDOWN:
            current_polygon.append((x, y))
            redraw()
        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                zoom_by_key("in")
            else:
                zoom_by_key("out")

    def zoom_by_key(in_or_out):
        nonlocal zoom, current_zoom, current_polygon
        old_zoom = zoom
        zoom = min(max(zoom + zoom_step if in_or_out == "in" else zoom - zoom_step, min_zoom), max_zoom)
        print(f"🔎 Zoom level: {zoom:.2f}")
        scale_ratio = zoom / old_zoom
        current_polygon = [(px * scale_ratio, py * scale_ratio) for (px, py) in current_polygon]
        redraw()

    current_zoom = zoom
    cv2.namedWindow("Polygon Annotation", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Polygon Annotation", 1000, 800)
    cv2.setMouseCallback("Polygon Annotation", mouse_handler)
    redraw()

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("❌ Exiting early.")
            cv2.destroyAllWindows()
            exit(0)

        elif key == ord('+') or key == ord('='):
            zoom_by_key("in")
        elif key == ord('-') or key == ord('_'):
            zoom_by_key("out")

        elif key == ord("u"):  # Undo last point
            if current_polygon:
                current_polygon.pop()
                redraw()
                print("↩️  Removed last point.")

        elif key == ord("r"):  # Reset all
            shapes.clear()
            current_polygon.clear()
            redraw()
            print("🔁 Reset all annotations.")

        elif key == ord("n"):  # Finish current polygon and add it
            if len(current_polygon) >= 3:
                label = input("Enter label for this polygon (e.g., Face, Mask, Glasses): ").strip()
                shapes.append({
                    "label": label,
                    "points": [(float(x), float(y)) for (x, y) in current_polygon],
                    "group_id": None,
                    "description": "",
                    "shape_type": "polygon",
                    "flags": {}
                })
                current_polygon.clear()
                redraw()
                print(f"✅ Polygon with label '{label}' added.")
            else:
                print("⚠️ At least 3 points required to complete a polygon.")

        elif key in [ord("s"), 13]:  # Save all and move to next image
            if len(shapes) > 0:
                json_data = {
                    "version": "5.8.2",
                    "flags": {},
                    "shapes": shapes,
                    "imagePath": base_name,
                    "imageData": None,
                    "imageHeight": orig_h,
                    "imageWidth": orig_w
                }
                json_filename = os.path.join(output_folder, os.path.splitext(base_name)[0] + ".json")
                with open(json_filename, "w") as jf:
                    json.dump(json_data, jf, indent=2)
                print(f"💾 Saved {len(shapes)} polygon(s) to {json_filename}")
            else:
                print("⚠️ No shapes drawn. Nothing saved.")
            break

    cv2.destroyAllWindows()

# === MAIN LOOP ===
for idx, image_path in enumerate(image_list):
    print(f"\n🖼️ Annotating image {idx + 1}/{len(image_list)}: {os.path.basename(image_path)}")
    annotate_image(image_path)

cv2.destroyAllWindows()
print("\n✅ All unique images processed. Program finished.")
