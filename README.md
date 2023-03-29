# Visual-Interfaces-Proj2

The aim of this project was to identify the top three most similar images for each of the 40 photos in the set included in this repository. I created an output chart in HTML format that displays the target photo in the leftmost column, with the next three columns showing the most similar, second most similar, and third most similar images, respectively.

To determine the rankings of the images, I utilized three metrics: color similarity, textural similarity, and shape similarity. I developed individual scripts to compute each of these metrics, and then combined them into a single simplex vector. This vector was used to rank the images based on their overall similarity to the target photo.

To provide a comprehensive overview of the project, I have included both the individual scripts for each metric as well as the combined script that generates the rankings. Additionally, I have included the output HTML file in PDF format for your convenience. 

As an additional component of this project, the professor collected data from his students regarding how they would personally rank the "top three" photos for each image. This information was then compiled into a file named "Crowd.txt". The file contains 40 lines, with each line consisting of 41 evenly-spaced integer values. These values correspond to the scores assigned to each photo based on the number of times the photo was ranked in a particular spot by the students for each of the 40 images.

To evaluate the accuracy of the system's top three photo selection for each image, the student rankings for each of the selected photos were aggregated per row. A higher score in a row indicated that more students selected those particular photos to fill those rankings, and a lower score indicated that the algorithm's decisions had lesser overlap with students' decisions. This metric was used to adjust the parameters within each algorithm to improve their accuracy in replicating human perception.
