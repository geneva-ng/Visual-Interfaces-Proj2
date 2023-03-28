import cv2
import os
import numpy as np
from functools import cmp_to_key
import base64
from io import BytesIO
from PIL import Image

#COLOR PREP --------------------

# Function to compute color difference
def compute_color_difference(hist1, hist2):
    diff = 0
    for i in range(len(hist1)):
        diff += abs(hist1[i] - hist2[i])
    return diff / (2 * 89 * 60)


#TEXTURE PREP -------------------

# Function to compute texture difference
def compute_texture_difference(hist1, hist2):
    diff = 0
    for i in range(len(hist1)):
        diff += abs(hist1[i] - hist2[i])
    return diff / (2 * 89 * 60)


#SHAPE PREP ---------------------

def binarize_image(img, threshold=100):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return bin_img

def shape_difference(image1, image2):
    mismatch = np.sum(image1 != image2)
    return mismatch / (2 * 89 * 60)


#SHARED BY ALL (SFA) ------------

# Function to compare two images values  
def compare_images(a, b):
    return a[1] - b[1]


#NEW: CREATE OUTPUT -------------

def create_thumbnail(image, size=(50, 50)):
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img.thumbnail(size)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f'<img src="data:image/jpeg;base64,{img_base64}" alt="Thumbnail" />'


def main():

    # Read images from the directory (SFA)                                              #IMGS FOLDER READIN
    directory = "images"
    image_files = [f"i{str(i).zfill(2)}.jpg" for i in range(1, 41)]

    # Read Crowd.txt file (SOURCED FROM COLOR/SHAPE)                                    #CROWD.TXT READIN 
    with open("Crowd.txt", "r") as f:
        crowd_data = [list(map(int, line.split())) for line in f.readlines()]

    image_data = {}  # Dictionary to store feature data

    for i, filename in enumerate(image_files):

        #read image                                                                      
        img = cv2.imread(os.path.join(directory, filename))      
        thumbnail = create_thumbnail(img)

        #color profile
        histColor = cv2.calcHist([img], [0, 1, 2], None, [2, 6, 8], [0, 256, 0, 256, 0, 256])
        histColor = histColor.flatten()

        #texture profile
        height, width, channels = img.shape
        gray = np.zeros((height, width), dtype=np.uint8)                    
        for y in range(height):
            for x in range(width):
                pixel = img[y, x]
                avg = int(np.mean(pixel))
                gray[y, x] = avg
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)                         
        laplacian_abs = cv2.convertScaleAbs(laplacian)
        histTex = cv2.calcHist([laplacian_abs], [0], None, [4], [0, 256])   
        histTex = histTex.flatten()

        #shape profile 
        bin_img = binarize_image(img)   
        
        # Store the features in the dictionary
        image_data[filename] = {
            'thumbnail': thumbnail,
            'histColor': histColor,
            'histTex': histTex,
            'bin_img': bin_img,
        }

    g_values = []

    for i, filename in enumerate(image_files):

        img_data = image_data[filename]
        thumbnail = img_data['thumbnail']
        histColor = img_data['histColor']
        histTex = img_data['histTex']
        bin_img = img_data['bin_img']

        row_data = []

        for j, otherFile in enumerate(image_files):

            img_op_data = image_data[otherFile]
            histColor_op = img_op_data['histColor']
            histTex_op = img_op_data['histTex']
            bin_img_op = img_op_data['bin_img']

            # Compute G
            I = compute_color_difference(histColor, histColor_op)
            T = compute_texture_difference(histTex, histTex_op)
            S = shape_difference(bin_img, bin_img_op)

            # #gestalt = grand_total_score = 11852
            # i_weight = 0.33     #color
            # s_weight = 0.22     #shape
            # t_weight = 0.11     #texture

            #gestalt1 = grand_total_score = 11205
            i_weight = 0.33     #color
            t_weight = 0.22     #texture
            s_weight = 0.11     #shape

            # #custom_gestalt3 = grand_total_score = 11205
            # i_weight = 0.50     #color
            # t_weight = 0.25     #texture
            # s_weight = 0.25     #shape

            G = i_weight * I + s_weight * S + t_weight * T

            if i != j:
                row_data.append((otherFile, G))

        row_data.sort(key=cmp_to_key(compare_images))
        g_values.append((filename, thumbnail, row_data[:3]))


    # Create HTML output
    html = '<table border="1" cellspacing="0" cellpadding="5">\n'
    html += '<tr><th>q</th><th>t1</th><th>t2</th><th>t3</th><th>score</th></tr>\n'

    # grand_total_score = 0

    # for row in g_values:
    #     filename, thumbnail, top3 = row
    #     html += f'<tr><td>{thumbnail}<br>{filename}</td>'

    #     row_score = 0

    #     for otherFile, _ in top3:
    #         img_op = cv2.imread(os.path.join(directory, otherFile))
    #         thumbnail_op = create_thumbnail(img_op)
    #         file_index = int(otherFile[1:3]) - 1
    #         current_q = crowd_data[image_files.index(filename)][file_index]
    #         row_score += current_q
    #         html += f'<td>{thumbnail_op}<br>{otherFile}<br>q: {current_q}</td>'

    #     grand_total_score += row_score
    #     html += f'<td>{row_score}</td></tr>\n'

    grand_total_score = 0

    for row in g_values:
        filename, thumbnail, top3 = row
        html += f'<tr><td>{thumbnail}<br>{filename}</td>'

        row_score = 0

        for otherFile, _ in top3:
            img_op = cv2.imread(os.path.join(directory, otherFile))
            thumbnail_op = create_thumbnail(img_op)
            file_index = int(otherFile[1:3]) - 1
            current_q = crowd_data[image_files.index(filename)][file_index]

            # Cap current_q at 3 if it's greater than 3
            if current_q > 3:
                current_q = 3

            row_score += current_q
            html += f'<td>{thumbnail_op}<br>{otherFile}<br>q: {current_q}</td>'

        grand_total_score += row_score
        html += f'<td>{row_score}</td></tr>\n'

    

    html += '</table>'

    # html += f'<p>GRAND TOTAL SCORE: {grand_total_score}</p>'
    html += f'<p>PERSONAL HAPPINESS SCORE: {grand_total_score}</p>'

    with open("custom_gestalt3.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()

