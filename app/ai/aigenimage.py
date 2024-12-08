from gradio_client import Client
from loguru import logger
import os
from app.utils.translate_prompt import translate_prompt
from datetime import datetime
from PIL import Image
import asyncio


async def generate_image(text):
    try:
        txt = await translate_prompt(text)
        client = Client("stabilityai/stable-diffusion-3.5-large-turbo")
        result = client.predict(
	        	prompt=txt,
		        negative_prompt="",
        		seed=0,
	        	randomize_seed=True,
		        width=1024,
    		    height=1024,
    	    	guidance_scale=0,
	    	    num_inference_steps=4,
    	    	api_name="/infer"
        )
        dd = str(datetime.now()).split(' ')
        dttime = dd[0] + '_' + dd[1]
        webp_image = Image.open(str(result[0]))
        png_image = webp_image.convert("RGBA")
        nam = str(result[0]).rstrip('/image.webp') + f'/{dttime}{text[0:4]}.png'
        png_image.save(nam)
        os.remove(str(result[0]))
        if result is not None:
            return nam
    except Exception as ex:
        return logger.error(f'Ошибка при генерации изображения:\n{ex}')
    


#print(asyncio.run(generate_image('')))