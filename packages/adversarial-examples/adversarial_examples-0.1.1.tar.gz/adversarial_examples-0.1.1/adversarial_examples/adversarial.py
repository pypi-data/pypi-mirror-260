from typing import Union

import torch
import torch.optim as optim
from torch import Tensor
from torch.nn import Module


def create_adversarial_example(
    model: Module,
    source_image: Tensor,
    target_label: Union[str, int],
    epsilon: float = 0.1,
    num_steps: int = 100,
    alpha: float = 0.01,
) -> Tensor:
    """
    This function creates an adversarial example using the given model, image tensor,
    and target label. The target label can be either the label name or label index
    as defined in the imagenet-labels.json file.

    Args:
        model (Module): The model to be used for creating the adversarial example.
        image_tensor (Tensor): The image tensor to be used for creating the adversarial example.
        target_label (Union[str, int]): The target label for the adversarial example.
            Can be either the label name or label index.
        epsilon (float, optional): The maximum allowed size of the adversarial perturbation.
            Default is 0.1.
        num_steps (int, optional): The number of steps for the gradient descent. Default is 100.
        alpha (float, optional): The step size for the gradient descent. Default is 0.01.

    Returns:
        Tensor: The adversarial example as a tensor.
    """
    model.eval()

    # Create a copy of the image and make it requires gradient
    adversarial_image = source_image.clone().detach().unsqueeze(0).requires_grad_(True)
    optimizer = optim.Adam([adversarial_image], lr=0.01)

    for i in range(num_steps):
        outputs = model(adversarial_image)
        loss = torch.nn.CrossEntropyLoss()(outputs, target_label)
        loss += epsilon * torch.norm(adversarial_image - source_image)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return adversarial_image.requires_grad_(False).squeeze()
