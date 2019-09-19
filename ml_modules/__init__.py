from .bicubic_upsample.inference import inference as bicubic
from .bilinear_upsample.inference import inference as bilinear
from .nn_upsample.inference import inference as nearest_neighbor

__all__ = ['bicubic', 'bilinear', 'nearest_neighbor']