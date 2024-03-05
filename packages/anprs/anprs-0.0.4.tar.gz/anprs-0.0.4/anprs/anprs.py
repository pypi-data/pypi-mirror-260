# from os.path import splitext
# from turtle import mode
import os

import cv2
from keras.models import model_from_json, Sequential, load_model
import numpy as np
from .local_utils import detect_lp


# helper functions
def preprocess_image(image_path, resize=False):
    print(f"pre_process_image with path {image_path}")
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Normalize pixel values
    img = img.astype(np.float32) / 255.0
    # img = img / 255
    if resize:
        img = cv2.resize(img, (224, 224))
    return img

def check_image_file_exists(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            try:
                # Try to load the image using cv2
                img = cv2.imread(file_path)
                if img is not None:
                    return True, "Image file exists and is valid."
                else:
                    return False, "File exists but is not a valid image."
            except Exception:
                return False, "Failed to load image. File may not be a valid image format."
        else:
            return False, "Path exists but is not a file."
    else:
        return False, "File does not exist."


# class for license plate recognition
class LPR:
    def __init__(self):
        # Define the paths for the media and results folders
        self.media_folder = "../media"
        self.results_folder = "../results"

        # Create the media folder if it doesn't exist
        if not os.path.exists(self.media_folder):
            os.makedirs(self.media_folder)

        # Create the results folder if it doesn't exist
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)

        # Print a message to indicate the folders are created
        print("Folders 'media' and 'results' created successfully.")

    wpod_net_path = "../models/wpod-net.json"

    def load_lpr_model(self):
        try:
            # path = splitext(self.wpod_net_path)[0]
            # with open("%s.json" % path, "r") as json_file:
            #     model_json = json_file.read()
            # model = model_from_json(model_json, custom_objects={})
            # model.load_weights('%s.h5' % path)
            model = load_model(filepath="../models/wpod_net_all_in_one.h5")
            print("LPR Model Loaded successfully...")
            print("Detecting License Plate ... ")
            return model
        except Exception as e:
            print(f"wpod_net loading exception\n {e}")

    # wpod_net_model = load_lpr_model()

    # detect license plate
    def get_plate(self, image_path, Dmax=608, Dmin=608):
        print(f"get_plate with {image_path}")
        vehicle_img = preprocess_image(image_path)
        ratio = float(max(vehicle_img.shape[:2])) / min(vehicle_img.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        wpod_net_model = self.load_lpr_model()
        _, LpImg, _, cor = detect_lp(
            wpod_net_model, vehicle_img, bound_dim, lp_threshold=0.5
        )
        return vehicle_img, LpImg, cor

    # save image
    def save_predicted_img(self, img_path):
        try:
            vehicle, LpImg, cor = self.get_plate(img_path)
            img = cv2.convertScaleAbs(LpImg[0], alpha=255.0)
            is_saved = cv2.imwrite("../results/res.jpg", img)
            if(not is_saved):
                raise Exception('File Error: Could not write cropped image')
            return is_saved
        except Exception as e:
            print(f"Exception in plate detection:\n{e}")
            return False

    # wrapper for performing lpr
    def perform_lpr(self, original_img_path: str):
        """
        The function `perform_lpr` performs license plate recognition on an image and saves the
        predicted results.
        
        :param original_img_path: The `original_img_path` parameter in the `perform_lpr` method is a
        string that represents the file path to the original image on which you want to perform license
        plate recognition (LPR). This path should point to the location of the image file on your system
        :type original_img_path: str
        :return: The `perform_lpr` method returns `true` if License plate is successfully detected save cropped image is saved,
        else returns `false`
        """
        print("performing lpr...")
        file_check, reason = check_image_file_exists(original_img_path)
        if not file_check:
            print(reason)
            return False
        res = self.save_predicted_img(original_img_path)
        print(f"LPR results saved = {res}")
        return res


# class for optical character recognition
class OCR:
    ocr_model_path = "../models/ocr_model.h5"

    # lp_image_path = 'results/res.jpg'

    def find_contours(self, dimensions, img):
        cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        lower_width = dimensions[0]
        upper_width = dimensions[1]
        lower_height = dimensions[2]
        upper_height = dimensions[3]

        img_ht, img_wt = np.shape(img)

        cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:15]

        ii = cv2.imread("../results/contour.jpg")

        x_cntr_list = []
        target_contours = []
        img_res = []
        for cntr in cntrs:
            intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)

            # if lower_width < intWidth < upper_width and lower_height < intHeight < upper_height:
            if (
                0.40 * img_wt > intWidth > 0.01 * img_wt
                and 0.75 * img_ht > intHeight > 0.40 * img_ht
            ):
                x_cntr_list.append(intX)

                char_copy = np.zeros((44, 24))
                char = img[intY : intY + intHeight, intX : intX + intWidth]
                char = cv2.resize(char, (20, 40))

                cv2.rectangle(
                    ii,
                    (intX, intY),
                    (intWidth + intX, intY + intHeight),
                    (50, 21, 200),
                    2,
                )

                # char = cv2.subtract(255, char)
                char = 255 - char

                char_copy[2:42, 2:22] = char
                char_copy[0:2, :] = 0
                char_copy[:, 0:2] = 0
                char_copy[42:44, :] = 0
                char_copy[:, 22:24] = 0

                img_res.append(char_copy)
                # plt.show()

        indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
        img_res_copy = []
        for idx in indices:
            img_res_copy.append(img_res[idx])
        img_res = np.array(img_res_copy)

        return img_res

    def segment_characters(self, image):
        img_lp = cv2.resize(image, (333, 75))
        img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
        _, img_binary_lp = cv2.threshold(
            img_gray_lp, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img_binary_lp = cv2.erode(img_binary_lp, kernel)
        img_binary_lp = cv2.dilate(img_binary_lp, kernel)

        # img_binary_lp = cv2.erode(img_binary_lp, (3, 3))
        # img_binary_lp = cv2.dilate(img_binary_lp, (3, 3))

        LP_WIDTH = img_binary_lp.shape[0]
        LP_HEIGHT = img_binary_lp.shape[1]

        img_binary_lp[0:3, :] = 255
        img_binary_lp[:, 0:3] = 255
        img_binary_lp[72:75, :] = 255
        img_binary_lp[:, 330:333] = 255

        dimensions = [LP_WIDTH / 6, LP_WIDTH / 2, LP_HEIGHT / 10, 2 * LP_HEIGHT / 3]

        if not cv2.imwrite("../results/contour.jpg", img_binary_lp):
            raise Exception("Could not write contours image")

        print("image segmented...")

        char_list = self.find_contours(dimensions, img_binary_lp)

        print("contours found...")

        return char_list

    # lp_image = cv2.imread(lp_image_path)

    # model: Sequential = load_model(filepath='models/ocr_model.h5')
    model: Sequential = load_model(filepath="../models/ocr_model.h5")

    def fix_dimension(self, img):
        new_img = np.zeros((28, 28, 3))
        for i in range(3):
            new_img[:, :, i] = img
        return new_img

    def get_results(self):
        """
        The function `get_results` performs optical character recognition (OCR) on a license plate image
        to extract and return the plate number.
        :return: The `get_results` method returns the recognized plate number after performing OCR on
        the segmented characters of the input image.
        """
        print("started ocr...")

        lp_image_path = "../results/res.jpg"
        lp_image = cv2.imread(lp_image_path)
        # lp_canny_image = cv2.Canny(lp_image)
        # lp_canny_image = cv2.resize(lp_canny_image, (32,32))

        dic = {}
        characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, c in enumerate(characters):
            dic[i] = c

        output = []
        segmented_chars = self.segment_characters(lp_image)
        for i, ch in enumerate(segmented_chars):
            print(type(ch), ch.shape)
            # img_canny = cv2.Canny(np.uint8(ch), 32, 32)
            img_ = cv2.resize(ch, (28, 28), interpolation=cv2.INTER_AREA)
            img = self.fix_dimension(img_)
            img = img.reshape((1, 28, 28, 3))
            print(img.shape)
            # img = img.reshape((1, 28, 28, 3))

            # im = np.array(img)
            # im = img/255.0
            y_ = self.model.predict(img)

            idx = np.argmax(y_)

            character = dic[idx]
            output.append(character)

        plate_number = "".join(output)

        print("ocr done.")

        return plate_number


# wrapper for whole process
class Recognizer:
    name = ""
    lpr_model_path = ""



def main(run=False):

    if not run:
        return

    lpr = LPR()
    ocr = OCR()

    image_path = '../media/photo.jpg'

    lpr_res = lpr.perform_lpr(image_path)

    license_plate_number = ""

    if lpr_res:
        license_plate_number = ocr.get_results()
    else:
        print('License plate not detected')

    print(lpr_res, license_plate_number)

if __name__ == '__main__':
    main()
