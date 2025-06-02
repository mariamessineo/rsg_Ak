##First version 30-May-2025 Maria Messineo (tested on mw-plot)
##Direct Milky Way image download  2-June-2025 Maria Messineo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import requests
from PIL import Image
from io import BytesIO



def rgb2gray(rgb_image):
    """Convert RGB image to grayscale using perceptual weights."""
    return np.dot(rgb_image[..., :3], [0.2125, 0.7154, 0.0721])


def load_and_crop_image(image_path, lon_extent=14.5, offset=0.0, scale_x=0.01666, scale_y=0.01666):
    """
    Load and crop the Milky Way image to focus on the Galactic center.
    Returns the cropped image and coordinate transformation parameters.
    """
    
    
    # Check if the path is a URL or local file
    if image_path.startswith('http'):
        response = requests.get(image_path)
        if response.status_code == 200:
            im_pil = Image.open(BytesIO(response.content))
            im = np.array(im_pil)
        else:
            raise ValueError("Failed to retrieve image from URL.")
    else:
        im = plt.imread(image_path)
    
    im2 = np.rot90(im, 2)  # Rotate 180 degrees, because made for a rotated version
    im=im2                 # called main_milkyway-full_nasa_jpl-caltech.jpg
                           # sun position Y=+8 kpc 
    center_x = im.shape[0] / 2 - 94 + 60
    center_y = im.shape[1] / 2 + 60 - 60

    delta=0          #to add extra lengths to the axis
    lo = lon_extent + delta
    x1 = int((-lo) / scale_x + center_x)
    y1 = int((-lo - offset) / scale_y + center_y)
    x2 = int((lo + offset) / scale_x + center_x)
    y2 = int((lo) / scale_y + center_y)
    im = im[x1:x2, y1:y2, :3]
    center_x -= x1
    center_y -= y1
    return im, scale_x, scale_y, center_x, center_y


def plot_galactic_distribution(im, scale_x, scale_y, center_x, center_y, rsun, xr, yr, output_file, title_text):
    """Plot grayscale Milky Way with overlaid Galactic star distribution."""
    fig, ax = plt.subplots(figsize=(10, 10))
    gray = -1 * rgb2gray(im)
    ax.imshow(gray, cmap='gray')

    sun_x = (0.0 - 0.0) / scale_x + center_x
    sun_y = (rsun - 0.0) / -scale_y + center_y
    ax.scatter(sun_x, sun_y, color='blue', s=10, label="Sun")
    ax.scatter(center_x, center_y, color='cyan', s=5, label="Galactic Center (0,0)")

    star_x = (xr - 0.0) / scale_x + center_x
    star_y = (yr - 0.0) / -scale_y + center_y
    ax.scatter(star_x, star_y, color='red', s=2, label="cRSG stars")

    # Axis ticks in Galactic coordinates
    ticks = [-15, -10, -5, 0, 5, 10, 15]
    tick_x = [x / scale_x + center_x for x in ticks]
    tick_y = [y / -scale_y + center_y for y in ticks]
    ax.xaxis.set_major_locator(ticker.FixedLocator(tick_x))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticks))
    ax.yaxis.set_major_locator(ticker.FixedLocator(tick_y))
    ax.yaxis.set_major_formatter(ticker.FixedFormatter(ticks))

    ax.set_xlabel("X [kpc]")
    ax.set_ylabel("Y [kpc]")
    ax.legend(loc="lower left")

    ax.text(0.70, 0.05, "Image Credit: NASA/JPL-Caltech", transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.text(0.70, 0.90, title_text, transform=ax.transAxes, fontsize=9, color='red',
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.savefig(output_file)
    plt.close()


def main():
    """    
    location:
    https://commons.wikimedia.org/wiki/File:Milky_Way_galaxy1.jpg
    download this image in your directory
    """

    # Parameters
    rsun = 8.125
    image_path = "https://upload.wikimedia.org/wikipedia/commons/8/83/Milky_Way_galaxy1.jpg" #2,400 × 2,589 
    catalog_path = "./tab_xyv.dat"
    output_file = "./galaxyRSG.jpeg"
    title = "Galactic plane view of cRSGs"

    # Load data
    data = pd.read_csv(catalog_path,sep="\s+",names = ['source_id','ll','bb','X_8.125','Y_8.125','X_8.50','Y_8.50','Vlsr'])
    xr, yr = data['X_8.125'], data['Y_8.125']

    # Load and crop background
    im, scale_x, scale_y, center_x, center_y = load_and_crop_image(image_path)

    # Plot
    plot_galactic_distribution(im, scale_x, scale_y, center_x, center_y,
                               rsun, xr, yr, output_file, title)


if __name__ == "__main__":
    main()
    
#MM had first used the mw-plot package, but she wanted a different image orientation.
#MM aknowledge Dr. Henry Leung from
#the Department of Astronomy & Astrophysics, University of Toronto
#for his mw-plot, which she used to check the result    