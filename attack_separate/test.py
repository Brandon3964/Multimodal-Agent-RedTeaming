from PIL import Image
from attack.bim import bim
from attack.llava_model import LLaVa
import os 

path = "liuhaotian/llava-v1.5-7b"
model = LLaVa(path)

image = Image.open("input.png").convert("RGB")

outputs = ["a blue motorcycle with cat"]

attack_out_dict = bim(model, image, outputs, size=1536)
adv_image = attack_out_dict["adv_image"]
adv_caption = attack_out_dict["adv_outputs"][0]  # Keep as in your original code
acc = attack_out_dict["acc"]

print("Adv caption:", adv_caption)
print("Target caption:", outputs)
print("Accuracy:", acc)

adv_image.save("adv_image.jpg", format="JPEG")
print("Adversarial image saved as adv_image.jpg")