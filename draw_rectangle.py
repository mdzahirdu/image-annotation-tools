import cv2
import os
import glob

# === PARAMETERS ===
input_folder = r"J:\IJCB_paper_face1st_data_May_25\YOLOv_final\draw_annotation_manually\images"
output_folder = r"J:\IJCB_paper_face1st_data_May_25\YOLOv_final\draw_annotation_manually\label"

os.makedirs(output_folder, exist_ok=True)

class_id = 0
scale = 0.2

# === IMAGE LIST ===
image_list = glob.glob(os.path.join(input_folder, "*.JPG"))

# === MAIN LOOP ===
for image_path in image_list:
    boxes = []
    drawing = False
    ix, iy = -1, -1

    image = cv2.imread(image_path)
    image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
    h_img, w_img = image.shape[:2]
    image_copy = image.copy()

    def draw_boxes(img, boxes, current_box=None):
        for (start, end) in boxes:
            cv2.rectangle(img, start, end, (0, 255, 0), 2)
        if current_box is not None:
            cv2.rectangle(img, current_box[0], current_box[1], (0, 0, 255), 2)

    def mouse_handler(event, x, y, flags, param):
        global drawing, ix, iy, image_copy, boxes
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                temp = image.copy()
                draw_boxes(temp, boxes, ((ix, iy), (x, y)))
                cv2.imshow("image", temp)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            boxes.append( ((ix, iy), (x, y)) )
            temp = image.copy()
            draw_boxes(temp, boxes)
            image_copy = temp.copy()
            cv2.imshow("image", image_copy)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_handler)
    cv2.imshow("image", image_copy)

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("Exiting early.")
            cv2.destroyAllWindows()
            exit(0)

        elif key == ord("c"):
            # save YOLO annotation
            base_name = os.path.basename(image_path)
            output_txt = os.path.join(output_folder, os.path.splitext(base_name)[0] + ".txt")
            with open(output_txt, "w") as f:
                for (start, end) in boxes:
                    x1,y1 = start
                    x2,y2 = end
                    xmin, ymin = min(x1,x2), min(y1,y2)
                    xmax, ymax = max(x1,x2), max(y1,y2)
                    x_center = ((xmin + xmax)/2) / w_img
                    y_center = ((ymin + ymax)/2) / h_img
                    w = (xmax - xmin) / w_img
                    h = (ymax - ymin) / h_img
                    line = f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"
                    f.write(line + "\n")
                    print(f"Saved: {line}")

            # show cropped regions for 0.5 sec
            for (start, end) in boxes:
                xmin, ymin = min(start[0],end[0]), min(start[1],end[1])
                xmax, ymax = max(start[0],end[0]), max(start[1],end[1])
                crop = image[ymin:ymax, xmin:xmax]
                cv2.imshow("crop", crop)
                cv2.waitKey(1000)  # 1 sec
                cv2.destroyWindow("crop")

            break

        elif key == ord("r"):
            boxes = []
            image_copy = image.copy()
            cv2.imshow("image", image_copy)

    cv2.destroyAllWindows()

print("All images processed.")
