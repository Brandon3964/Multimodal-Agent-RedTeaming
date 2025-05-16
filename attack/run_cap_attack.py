import argparse
import os
from PIL import Image

from beartype import beartype
from datasets import load_dataset

from agent_attack.attacks import get_attack_fn
from agent_attack.data.attack_data import get_examples
from agent_attack.models import get_model


def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run adversarial attack for captions")

    parser.add_argument(
        "--attack",
        type=str,
        default="bim",
        choices=["pgd", "bim"],
        help="Adversarial attack method",
    )
    parser.add_argument(
        "--captioning_model",
        type=str,
        default="liuhaotian/llava-v1.5-7b",
        choices=["liuhaotian/llava-v1.5-7b", "Salesforce/instructblip-vicuna-7b"],
        help="Captioning backbone.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=14,
        help="Batch size for the attack",
    )
    parser.add_argument("--result_dir", type=str, default="")

    # New arguments for generalization
    parser.add_argument("--image_path", type=str, default="input.png", help="Path to the input image")
    parser.add_argument("--target_caption", type=str, default="A cat", help="Target caption for the attack")
    parser.add_argument("--size", type=int, default=1536, help="Size parameter for the attack")

    args = parser.parse_args()
    return args


@beartype
def run(args: argparse.Namespace) -> dict:
    attack_fn = get_attack_fn(args.attack)
    captioning_model = get_model(args.captioning_model)

    # Load the image
    victim_image = Image.open(args.image_path).convert("RGB")
    prompt_fn = captioning_model.get_captioning_prompt_fn()
    inputs = [prompt_fn()]
    outputs = [args.target_caption]

    attack_out_dict = attack_fn(captioning_model, victim_image, inputs, outputs, size=args.size)
    adv_image = attack_out_dict["adv_image"]
    adv_caption = attack_out_dict["adv_outputs"][0]
    acc = attack_out_dict["acc"]
    print("Adv caption:", adv_caption)
    print("Target caption:", args.target_caption)
    print("Accuracy:", acc)

    return {
        "adv_image": adv_image,
        "adv_caption": adv_caption,
        "acc": acc,
    }


if __name__ == "__main__":
    import sys
    args = config()
    print(f"Start testing on image {args.image_path}...")
    result = run(args)
    print("done!")
