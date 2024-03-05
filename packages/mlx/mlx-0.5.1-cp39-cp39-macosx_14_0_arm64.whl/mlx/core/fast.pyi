"""
mlx.core.fast: fast operations
"""
from __future__ import annotations
__all__ = ['rope']
def rope(*args, **kwargs):
    """
    
            rope(a: array, dims: int, *, traditinoal: bool, base: float, scale: float, offset: int, stream: Union[None, Stream, Device] = None) -> array
    
            Apply rotary positional encoding to the input.
    
            Args:
                a (array): Input array.
                dims (int): The feature dimensions to be rotated. If the input feature
                    is larger than dims then the rest is left unchanged.
                traditional (bool): If set to ``True`` choose the traditional
                    implementation which rotates consecutive dimensions.
                base (float): The base used to compute angular frequency for
                    each dimension in the positional encodings.
                scale (float): The scale used to scale the positions.
                offset (int): The position offset to start at.
    
            Returns:
                array: The output array.
          
    """
