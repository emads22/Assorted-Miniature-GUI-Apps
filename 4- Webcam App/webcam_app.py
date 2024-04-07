# Note: This script runs only on a local IDE with "streamlit run main.py"

import streamlit as st
from PIL import Image


# Function to convert image to grayscale
def convert_to_grayscale(image):
    """
    Convert the provided image to grayscale.

    Parameters:
    - image: An image object returned either from camera capturing or file uploading.

    Returns:
    - grayscale_image: PIL.Image.Image object
    """
    # Open the image and render it with Image.open() from PIL
    this_image = Image.open(image)
    # Convert the image to grayscale
    grayscale_image = this_image.convert('L')
    # Return the resulting grayscale image
    return grayscale_image


# Function to display original and grayscale images
def display_images(original_img, grayscale_img):
    """
    Display the original and grayscale images side by side.

    Parameters:
    - original_img: PIL.Image.Image object
    - grayscale_img: PIL.Image.Image object
    """
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original:")
        st.image(original_img, use_column_width=True)

    with col2:
        st.subheader("Grayscale:")
        st.image(grayscale_img, use_column_width=True)


# Function to capture image from webcam
def capture_image():
    """
    Logic for capturing image from webcam and converting it to grayscale.
    """
    st.header("Capture a picture")
    # Create a collapsible section titled "Start camera"
    with st.expander("Start camera"):
        # Prompt the user to provide camera input
        original_image = st.camera_input("Camera")
        if original_image is not None:
            grayscale_image = convert_to_grayscale(original_image)
            # Display the original and grayscale images
            display_images(original_image, grayscale_image)


# Function to upload image
def upload_image():
    """
    Logic for browsing image, converting it to grayscale, and displaying.
    """
    st.header("Browse a picture")
    # Prompt the user to upload an image file
    original_image = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if original_image is not None:
        grayscale_image = convert_to_grayscale(original_image)
        # Display the original and grayscale images
        display_images(original_image, grayscale_image)


# Main function
def main():
    # Set the title of the app and format it to be in the center
    st.markdown("<h1 style='text-align: center;'>Grayscale Image Converter</h1>",
                unsafe_allow_html=True)

    # Create buttons for capturing and browsing images
    _, col1, col2, _ = st.columns(4)
    with col1:
        capture_button = st.button("Capture Image")
    with col2:
        browse_button = st.button("Browse Image")

    # If the capture button is clicked, call the capture_image function
    if capture_button:
        capture_image()

    # If the browse button is clicked, call the upload_image function
    if browse_button:
        upload_image()


if __name__ == '__main__':
    main()
