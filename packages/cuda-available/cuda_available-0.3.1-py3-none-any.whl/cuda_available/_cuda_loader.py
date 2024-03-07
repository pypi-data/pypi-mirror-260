# Copyright (c) 2024 Yansheng Zhu
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import os
import sys
import ctypes
from ctypes.util import find_library
from ._core import CUdevice_attribute, CUuuid, uuid_repr
from .cuda_error import CudaError

if sys.platform == "win32":
    DEFAULT_DYLIB_NAME = "nvcuda"
elif sys.platform == "linux":
    DEFAULT_DYLIB_NAME = "cuda"
else:
    raise CudaError("This platform is not supported!")


class CudaLoader:
    def __init__(self, lib_name: str = DEFAULT_DYLIB_NAME):
        nv_cuda_path = find_library(lib_name)
        if nv_cuda_path is not None:
            nv_cuda_basename = os.path.basename(nv_cuda_path)
            self.nv_cuda = ctypes.CDLL(nv_cuda_basename)
            cuInit = getattr(self.nv_cuda, "cuInit", None)
            if cuInit is None:
                self.nv_cuda = None
            else:
                errcode = cuInit(0)
                if errcode != 0:
                    self.nv_cuda = None
        else:
            self.nv_cuda = None

    def cuDeviceGetCount(self) -> int:
        if self.nv_cuda is None:
            return 0
        cnt = ctypes.c_int()
        cuDeviceGetCount = getattr(self.nv_cuda, "cuDeviceGetCount", None)
        if cuDeviceGetCount is None:
            return 0
        errcode = cuDeviceGetCount(ctypes.byref(cnt))
        if errcode != 0:
            return 0
        return cnt.value

    def cuDeviceGet(self, idx: int) -> int:
        if self.nv_cuda is None:
            raise CudaError(f"Cannot get #{idx} cuda device, the cuda init failed!")
        handle = ctypes.c_int()
        cuDeviceGet = getattr(self.nv_cuda, "cuDeviceGet", None)
        if cuDeviceGet is None:
            raise CudaError(
                f"Cannot get #{idx} cuda device, cuDeviceGet was not found!"
            )
        errcode = cuDeviceGet(ctypes.byref(handle), ctypes.c_int(idx))
        if errcode != 0:
            raise CudaError(f"Cannot get #{idx} cuda device, error code is {errcode}!")
        return handle.value

    def cuDeviceGetAttr(self, attr: CUdevice_attribute, dev_handle: int) -> int:
        if self.nv_cuda is None:
            raise CudaError(
                f"Cannot get {attr.name} for this cuda device, the cuda init failed!"
            )
        pi = ctypes.c_int()
        cuDeviceGetAttribute = getattr(self.nv_cuda, "cuDeviceGetAttribute", None)
        if cuDeviceGetAttribute is None:
            raise CudaError(
                f"Cannot get {attr.name} for this cuda device, cuDeviceGetAttribute was not found!"
            )
        errcode = cuDeviceGetAttribute(
            ctypes.byref(pi), ctypes.c_int(attr.value), ctypes.c_int(dev_handle)
        )
        if errcode != 0:
            raise CudaError(
                f"Cannot get {attr.name} for this cuda device, error code is {errcode}!"
            )
        return pi.value

    def isCuInitSuccess(self) -> bool:
        return self.nv_cuda is not None

    def _cu_driver_version(self) -> (int, int):
        if self.nv_cuda is None:
            raise CudaError(f"Cannot get cuda driver version, the cuda init failed!")
        version = ctypes.c_int()
        cuDriverGetVersion = getattr(self.nv_cuda, "cuDriverGetVersion", None)
        if cuDriverGetVersion is None:
            raise CudaError(
                f"Cannot get cuda driver version, cuDriverGetVersion was not found!"
            )
        errcode = cuDriverGetVersion(ctypes.byref(version))
        if errcode != 0:
            raise CudaError(f"Cannot get cuda driver version, error code is {errcode}!")
        version = version.value
        major = version // 1000
        minor = version % 1000 // 10
        return major, minor

    def cudaDriverVersion(self) -> str:
        major, minor = self._cu_driver_version()
        return f"{major}.{minor}"

    def cuDeviceGetName(self, dev_handle: int) -> str:
        if self.nv_cuda is None:
            raise CudaError(f"Cannot get device name, the cuda init failed!")
        name = ctypes.create_string_buffer(256)
        cuDeviceGetName = getattr(self.nv_cuda, "cuDeviceGetName", None)
        if cuDeviceGetName is None:
            raise CudaError(
                f"Cannot get cuda device name, cuDeviceGetName was not found!"
            )
        errcode = cuDeviceGetName(name, 256, dev_handle)
        if errcode != 0:
            raise CudaError(f"Cannot get cuda device name, error code is {errcode}!")
        return str(name.value, encoding="ascii")

    def cuDeviceTotalMem(self, dev_handle: int) -> int:
        if self.nv_cuda is None:
            raise CudaError(f"Cannot get total memory, the cuda init failed!")
        size = ctypes.c_size_t()
        cuDeviceTotalMem = getattr(self.nv_cuda, "cuDeviceTotalMem_v2", None)
        if cuDeviceTotalMem is None:  # Fall back to v1
            cuDeviceTotalMem = getattr(self.nv_cuda, "cuDeviceTotalMem", None)
        if cuDeviceTotalMem is None:
            raise CudaError(f"Cannot get total memory, cuDeviceTotalMem was not found!")
        errcode = cuDeviceTotalMem(ctypes.byref(size), dev_handle)
        if errcode != 0:
            raise CudaError(f"Cannot get total memory, error code is {errcode}!")
        return size.value

    def cuDeviceGetUuid(self, dev_handle: int) -> int:
        if self.nv_cuda is None:
            raise CudaError(f"Cannot get uuid, the cuda init failed!")
        major, minor = self._cu_driver_version()
        uuid = CUuuid()
        if major < 11 or minor < 4:
            cuDeviceGetUuid = getattr(self.nv_cuda, "cuDeviceGetUuid", None)
        else:
            cuDeviceGetUuid = getattr(self.nv_cuda, "cuDeviceGetUuid_v2", None)
        if cuDeviceGetUuid is None:
            raise CudaError(
                f"Cannot get uuid, cuDeviceGetUuid or cuDeviceGetUuid_v2 was not found!"
            )
        errcode = cuDeviceGetUuid(ctypes.byref(uuid), dev_handle)
        if errcode != 0:
            raise CudaError(f"Cannot get uuid, error code is {errcode}!")
        return uuid_repr(uuid)
