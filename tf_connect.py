import requests
import numpy as np
from PIL import Image
from io import BytesIO


def create_request(array):
    return '{"instances": %s}' % array


def image_downloader(image_url):
    response = requests.get(image_url)
    pil_image = Image.open(BytesIO(response.content))
    return pil_image


def image_to_array(pil_image, shape=None):
    img_array = np.array(pil_image)
    if shape:
        img_array = img_array.reshape(shape)
    return img_array


def tf_request(server_url, image_url, image_resolution: tuple = (320, 640)):

    # Download the image using the given url and resize it to the specified resolution
    input_image = image_downloader(image_url).resize(image_resolution)

    # Convert the image to a pixel np array and then create a list
    image_array = [image_to_array(input_image).tolist()]

    # Create a string request from the array to send it to the tensorflow model
    new_request = create_request(str(image_array))

    # Post the request to the tensorflow serving api
    response = requests.post(server_url, new_request)
    response.raise_for_status()

    # Prediction response from the api
    prediction_list = response.json()["predictions"][0]

    # return the list of predictions
    return prediction_list

def process_output(prediction_list: list):
    """
    prediction_list = [is_fedora, is_not_fedora]
    so index 0 is true and index 1 is false
    """
    # find the index with the highest value of likelihood
    max_index = (prediction_list.index(max(prediction_list)))

    is_fedora = not bool(max_index)

    if is_fedora:
        return "I found a Red Hat Fedora!"
    return "No Red Hat Fedora found :("
