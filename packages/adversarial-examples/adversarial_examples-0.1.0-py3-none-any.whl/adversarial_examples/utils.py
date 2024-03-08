import json
from typing import List, Tuple

import torch
from PIL import Image
from torch import Tensor
from torch.nn import Module
from torchvision import models, transforms

IMAGENET_LABELS_PATH = "imagenet-labels.json"
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def load_resnet_and_labels() -> Tuple[Module, List[str]]:
    """
    Load a pretrained ResNet and its corresponding labels.

    Returns:
        Tuple[Module, List[str]]: The loaded model and its labels.
    """
    model = models.resnet18(weights=models.resnet.ResNet18_Weights.IMAGENET1K_V1)
    with open(IMAGENET_LABELS_PATH) as f:
        labels = json.load(f)
    model.eval()
    return model, labels


def load_image(
    image_path: str,
    resize_size: int = 256,
    crop_size: int = 224,
    target_mean: List[float] = IMAGENET_MEAN,
    target_std: List[float] = IMAGENET_STD,
) -> Tensor:
    """
    Load an image as a Tensor and preprocess it.

    Args:
        image_path (str): The path to the image.
        resize_size (int, optional): The size to resize the image to. Defaults to 256.
        crop_size (int, optional): The size to crop the image to. Defaults to 224.
        target_mean (List[float], optional): The target mean for normalization. Defaults to [0.485, 0.456, 0.406].
        target_std (List[float], optional): The target standard deviation for normalization. Defaults to [0.229, 0.224, 0.225].

    Returns:
        Tensor: The preprocessed image.
    """
    image = Image.open(image_path)
    return preprocess_image(image)


def preprocess_image(
    image: Image.Image,
    resize_size: int = 256,
    crop_size: int = 224,
    target_mean: List[float] = [0.485, 0.456, 0.406],
    target_std: List[float] = [0.229, 0.224, 0.225],
) -> Tensor:
    preprocess = transforms.Compose(
        [
            transforms.Resize(resize_size),
            transforms.CenterCrop(crop_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=target_mean, std=target_std),
        ]
    )
    return preprocess(image)


def predict(model: Module, image: Tensor) -> Tensor:
    """
    Make a prediction using a model and an image.

    Args:
        model (Module): The model to use for prediction.
        image_tensor (Tensor): The image to predict.

    Returns:
        Tensor: The predicted class label.
    """
    with torch.no_grad():
        output = model(image.unsqueeze(0))
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    _, indices = torch.topk(probabilities, 1)
    return indices


def unnormalize(tensor, mean=IMAGENET_MEAN, std=IMAGENET_STD):
    tensor = tensor.clone()  # to avoid changes to the original tensor
    for t, m, s in zip(tensor, mean, std):
        t.mul_(s).add_(m)  # multiply by std and add the mean
    return tensor


def to_image(tensor: torch.Tensor) -> Image.Image:
    """
    Convert tensor to a PIL Image.

    Args:
        tensor (Tensor): The tensor to convert.

    Returns:
        Tensor: The predicted class label.
    """
    tensor = unnormalize(tensor)
    tensor = tensor.clamp(0, 1)
    return transforms.ToPILImage()(tensor)
