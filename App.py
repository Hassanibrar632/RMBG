import streamlit as st
import rembg
import numpy as np
from PIL import Image
import io

# Function to remove the background from an image
def remove_background(input_image):
    try:
        input_array = np.array(input_image)
        output_array = rembg.remove(input_array)
        output_image = Image.fromarray(output_array)
        return output_image
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Convert the processed image to bytes for downloading
def convert_image_to_bytes(image):
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')  # Save the image in PNG format
    img_bytes.seek(0)
    return img_bytes

# Streamlit App layout
st.title("Batch Background Removal")

# Initialize session state for storing processed images if it doesn't exist
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = {}

# Upload multiple images
uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'tiff'])

# Process the images if any are uploaded
if uploaded_files:
    st.write("Processing images...")
    
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.processed_images:
            try:
                # Open the uploaded image using PIL
                image = Image.open(uploaded_file)
                # Remove the background
                result_image = remove_background(image)
                
                # Store the processed image in session state to persist it
                if result_image:
                    st.session_state.processed_images[uploaded_file.name] = {
                        'original': image,
                        'processed': result_image
                    }
            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {e}")

# Display and download the images stored in session state
if st.session_state.processed_images:
    for file_name, images in st.session_state.processed_images.items():
        original_image = images['original']
        processed_image = images['processed']
        
        # Display original and processed images
        st.image([original_image, processed_image], caption=["Original Image", "Processed Image"], width=300)

        # Convert the processed image to bytes for download
        image_bytes = convert_image_to_bytes(processed_image)

        # Add download button
        st.download_button(
            label=f"Download Processed Image: {file_name}",
            data=image_bytes,
            file_name=f"processed_{file_name}",
            mime="image/png"
        )
