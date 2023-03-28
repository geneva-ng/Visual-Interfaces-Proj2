import cv2
import os
import numpy as np
from functools import cmp_to_key

# Function to compute texture difference
def compute_texture_difference(hist1, hist2):
    diff = 0
    for i in range(len(hist1)):
        diff += abs(hist1[i] - hist2[i])
    return diff / (2 * 89 * 60)

# Function to compare two images based on their T values
def compare_images(a, b):                                  
    return a[1] - b[1]

def main():
    # Read images from dir
    directory = "images"
    image_files = [f"i{str(i).zfill(2)}.jpg" for i in range(1, 41)]
   
    # Load crowd data from the text file
    with open("Crowd.txt", "r") as f:
        lines = f.readlines()
        crowd_data = [[float(value) for value in line.strip().split()] for line in lines]

    # Calculate grayscale intensity for all images 
    histograms = []
    for filename in image_files:
        img = cv2.imread(os.path.join(directory, filename))
        height, width, channels = img.shape
        gray = np.zeros((height, width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixel = img[y, x]
                avg = int(np.mean(pixel))
                gray[y, x] = avg

        #Calculate Laplacian for all images
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)    #hybrid
        laplacian_abs = cv2.convertScaleAbs(laplacian)
        histTex = cv2.calcHist([laplacian_abs], [0], None, [4], [0, 256])
        histograms.append(histTex.flatten())

    # Compute T values for each pair of images
    T_values = []
    for i, hist1 in enumerate(histograms):
        image_diffs = []
        for j, hist2 in enumerate(histograms):
            if i != j:
                T = compute_texture_difference(hist1, hist2)
                image_diffs.append((image_files[j], T))

        # Sort the images by their T values
        sorted_diffs = sorted(image_diffs, key=cmp_to_key(compare_images))
        T_values.append((image_files[i], sorted_diffs[:3]))

    # Create HTML output
    html_output = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            text-align: center;
            vertical-align: middle;
            border: 1px solid black;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
    </head>
    <body>
        <table>
            <tr>
                <th>q</th>
                <th>t1</th>
                <th>t2</th>
                <th>t3</th>
                <th>score</th>
            </tr>'''

    #Calculate q_scores for all images, rows, and for the entire table
    grand_total_score = 0
    for row_index, row in enumerate(T_values):
        row_total_score = 0
        html_output += "<tr><td><img src='images/{}' width='50px' height='50px'/><br>{}</td>".format(row[0], row[0])
        for col in row[1]:
            col_index = int(col[0][1:3]) - 1
            q_value = crowd_data[row_index][col_index]
            row_total_score += q_value
            html_output += "<td><img src='images/{}' width='50px' height='50px'/><br>{}<br>{}</td>".format(col[0], col[0], q_value)
        html_output += "<td>{}</td></tr>".format(row_total_score)
        grand_total_score += row_total_score

    html_output += '''
        </table>
        <p>PERSONAL HAPPINESS SCORE: {}</p>
    </body>
    </html>'''.format(grand_total_score)

    # Save HTML output to a file
    with open("output_texture_crowd.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    main()

