import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from .utils import *
from .llava_model import LLaVa

def bim(model, image, outputs, epsilon=16 / 255, alpha=1 / 255, iters=4000, size=1536):
    device = model.distributed_state.device
    prompt_fn = model.get_captioning_prompt_fn()
    inputs = [prompt_fn()]
    # Freeze the model
    model.freeze()

    if size:
        image = resize_image(image, size)
    image = torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0).permute(0, 3, 1, 2).to(device)
    delta = torch.zeros_like(image, requires_grad=True)

    evaluate_from_tensor(model, image + delta, inputs, outputs)

    losses = []
    best_delta = None
    best_acc = 0
    for idx in tqdm(range(iters)):
        pixel_values = model.image_processor_from_tensor(image + delta)

        loss = model.forward(pixel_values, questions=inputs, answers=outputs, image_sizes=None)
        # print(loss.item())
        losses.append(loss.item())
        loss.backward()

        # loss the lower the better
        with torch.no_grad():
            delta.grad.sign_()
            delta.data = delta.data - alpha * delta.grad
            delta.data.clamp_(-epsilon, epsilon)
            delta.data = torch.clamp(image + delta, 0, 1) - image
            delta.grad.zero_()

        if (idx + 1) % 200 == 0:
            with torch.no_grad():
                pixel_values = model.image_processor_from_tensor(image + delta)
                loss = model.forward(pixel_values, questions=inputs, answers=outputs, image_sizes=None)
                print("Loss:", loss.item())
            acc = evaluate_from_tensor(model, image + delta, inputs, outputs)
            # Save the image
            # image_np = (image + delta).squeeze(0).detach().cpu().numpy()
            # image_np = (image_np * 255).astype("uint8").transpose(1, 2, 0)
            # Image.fromarray(image_np).save(f"attack/attacks/bim_image_{idx + 1}.png")
            # Plot the loss
            # sns.lineplot(x=range(len(losses)), y=losses)
            # plt.savefig(f"attack/attacks/bim_loss.png")
            # plt.close()

            if acc > best_acc:
                best_acc = acc
                best_delta = delta.clone()

            # Early stopping
            if acc == 1:
                break

    if best_acc != 1:
        delta = best_delta
    image_np = (image + delta).squeeze(0).detach().cpu().numpy()
    adv_image = Image.fromarray((image_np * 255).astype("uint8").transpose(1, 2, 0))

    acc, gen_texts = evaluate_from_pil(model, adv_image, inputs, outputs)

    return {
        "adv_image": adv_image,
        "adv_outputs": gen_texts,
        "acc": acc,
    }

