from base64 import b64decode
import webbrowser
import openai


def generateImage_AndSave(promt, image_count):
    images=[]
    response = openai.Image.create(
        prompt = promt,
        n = image_count,
        size = '512x512',
        response_format = 'b64_json'
    )

    for image in response['data']:
        images.append(image.b64_json)

    prefix = 'Img'
    for index,image in enumerate(images):
        with open(f'{prefix}_{index}.jpg','wb') as file:
            file.write(b64decode(image))

openai.api_key = "OPEN AI API"
generateImage_AndSave('muscle men', image_count=1)

