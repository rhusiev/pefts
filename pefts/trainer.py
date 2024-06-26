from typing import Iterable

import torch
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

from .model import Transformer


class Trainer:
    """A simple trainer for the transformer model."""

    def __init__(self, model: Transformer, optimizer: torch.optim.Optimizer) -> None:
        """Initialize the trainer.

        Args:
            model: The model to train.
            optimizer: The optimizer to use.
        """
        self.model = model
        self.optimizer = optimizer
        self.device = next(model.parameters()).device

    def train(
        self, dataset: Iterable[tuple[torch.Tensor, torch.Tensor]], epochs: int = 1
    ) -> None:
        """Train the model on the given dataset.

        Args:
            dataset: The dataset to train on.
            epochs: The number of epochs to train for.
        """
        for _ in range(epochs):
            for batch, attention_mask in dataset:
                self.optimizer.zero_grad()
                result, loss = self.model(
                    batch[:, :-1].to(self.device),
                    batch[:, 1:].to(self.device),
                    attention_mask.to(self.device),
                )
                print(tokenizer.decode(result[0, -3, :].argmax()), end="")
                print(tokenizer.decode(result[0, -2, :].argmax()), end="")
                print(tokenizer.decode(result[0, -1, :].argmax()))
                print(loss.item())
                loss.backward()
                self.optimizer.step()
