import asyncio
from dataclasses import dataclass
from logging import getLogger
from typing import List, Literal, Optional, Union

import numpy as np

from .docker_inference_server import DockerInferenceServer, DockerInferenceServerConfig
from .utils import is_nvidia_system

LOGGER = getLogger("TEI")


Pooling_Literal = Literal["cls", "mean"]
DType_Literal = Literal["float32", "float16"]


@dataclass(order=False)
class TEIConfig(DockerInferenceServerConfig):
    # Docker options
    image: str = "ghcr.io/huggingface/text-embeddings-inference:cpu-latest"
    # Launcher options
    model_id: str = "bert-base-uncased"
    revision: str = "main"
    dtype: Optional[DType_Literal] = None
    pooling: Optional[Pooling_Literal] = None
    tokenization_workers: Optional[int] = None

    def __post_init__(self) -> None:
        super().__post_init__()

        if is_nvidia_system() and "cpu" in self.image:
            LOGGER.warning(
                "Your system has NVIDIA GPU, but you are using a CPU image."
                "Consider using a GPU image for better performance."
            )


class TEI(DockerInferenceServer):
    NAME: str = "Text-Embedding-Inference"
    SUCCESS_SENTINEL: str = "Ready"
    FAILURE_SENTINEL: str = "Error"

    def __init__(self, config: TEIConfig) -> None:
        super().__init__(config)

    async def single_client_call(self, text: str, **kwargs) -> np.ndarray:
        output = await self.client.feature_extraction(text=text, **kwargs)
        return output

    async def batch_client_call(self, text: List[str], **kwargs) -> List[np.ndarray]:
        output = await asyncio.gather(*[self.single_client_call(t, **kwargs) for t in text])
        return output

    def encode(self, text: Union[str, List[str]], **kwargs) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(text, str):
            output = asyncio.run(self.single_client_call(text, **kwargs))
            return output
        elif isinstance(text, list):
            output = asyncio.run(self.batch_client_call(text, **kwargs))
            return output
        else:
            raise ValueError(f"Unsupported input type: {type(text)}")
