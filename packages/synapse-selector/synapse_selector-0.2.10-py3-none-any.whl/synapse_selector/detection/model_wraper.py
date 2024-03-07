import torch
import numpy as np


class torch_model:
    def __init__(
        self,
    ) -> None:
        self.model = None
        self.weights_loaded = False

    def load_weights(self, model_path: str) -> None:
        print(model_path)
        self.model = torch.jit.load(model_path)
        self.model.eval()
        self.weights_loaded = True

    def predict(
        self,
        arr: np.ndarray,
        threshold: float = 0.5,
    ) -> list[int]:
        # reshape input to (1, 1, length)
        input_tensor = torch.reshape(
            torch.tensor(arr, dtype=torch.float), (1, 1, arr.shape[0])
        )
        self.preds = np.array(self.model(input_tensor).detach().flatten())
        infered_peaks = list(np.argwhere(self.preds > threshold).flatten())
        return infered_peaks

    def update_predictions(self, threshold: float) -> list[int]:
        infered_peaks = list(np.argwhere(np.array(self.preds) > threshold).flatten())
        return infered_peaks
