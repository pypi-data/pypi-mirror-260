# Copyright (c) 2024 Yansheng Zhu
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations
from ._cuda_loader import CudaLoader
from .cuda_error import CudaError
from ._core import CUdevice_attribute

__all__ = [
    "getCudaDeviceCount",
    "isCudaInitSuccess",
    "cudaDriverVersion",
    "CudaDeviceInfo",
    "CudaError",
    "CUdevice_attribute",
    "setCudaDylibName",
]
__version__ = "0.3.1"

cuda = CudaLoader()


def setCudaDylibName(name: str):
    """Set CUDA Driver dynamic library name

    Implementation details: The default name in Windows is `nvcuda` which will load `nvcuda.dll`
    the default name in Linux is `cuda` which will load `libcuda.so (or libcuda.so.X)`
    """
    cuda = CudaLoader(name)


def cudaDriverVersion() -> str:
    """CUDA driver version"""
    return cuda.cudaDriverVersion()


def isCudaInitSuccess() -> bool:
    """Check if CUDA was successfully initialized"""
    return cuda.isCuInitSuccess()


def getCudaDeviceCount() -> int:
    """Get CUDA device count

    Implementation details: If CUDA init failed or CUDA driver is not installed, this method also return 0,
    you can use isCudaInitSuccess to check it.
    """
    return cuda.cuDeviceGetCount()


class CudaDeviceInfo:
    """Get device information of cuda device with given device index"""

    def __init__(self, index: int):
        # get device handle
        self.handle = cuda.cuDeviceGet(index)
        # init name
        self._name = cuda.cuDeviceGetName(self.handle)
        # init uuid
        self._uuid = cuda.cuDeviceGetUuid(self.handle)
        # init compute capability
        cc_major = cuda.cuDeviceGetAttr(
            CUdevice_attribute.CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR, self.handle
        )
        cc_minor = cuda.cuDeviceGetAttr(
            CUdevice_attribute.CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR, self.handle
        )
        self._compute_capability = (cc_major, cc_minor)
        # init total vmem
        self._total_vmem = cuda.cuDeviceTotalMem(self.handle)
        # init pci id
        pci_bus = cuda.cuDeviceGetAttr(
            CUdevice_attribute.CU_DEVICE_ATTRIBUTE_PCI_BUS_ID, self.handle
        )
        pci_dev = cuda.cuDeviceGetAttr(
            CUdevice_attribute.CU_DEVICE_ATTRIBUTE_PCI_DEVICE_ID, self.handle
        )
        pci_domain = cuda.cuDeviceGetAttr(
            CUdevice_attribute.CU_DEVICE_ATTRIBUTE_PCI_DOMAIN_ID, self.handle
        )
        self._pci_id = (pci_bus, pci_dev, pci_domain)
        # init is tcc
        self._is_tcc = cuda.cuDeviceGetAttr(
            CUdevice_attribute.CU_DEVICE_ATTRIBUTE_TCC_DRIVER, self.handle
        )
        self._is_tcc = bool(self._is_tcc)

    @property
    def name(self) -> str:
        """Device name"""
        return self._name

    @property
    def uuid(self) -> str:
        """Device uuid

        Implementation details: If cuda version is 11.4+, using cuDeviceGetUuid_v2 instead of cuDeviceGetUuid
        """
        return self._uuid

    @property
    def computeCapability(self) -> (int, int):
        """Device cuda compute capability"""
        return self._compute_capability

    @property
    def totalGlobalVmem(self) -> int:
        """Device total available memory in bytes

        Implementation details: If cuDeviceTotalMem_v2 is not available, fall back to cuDeviceTotalMem (only support vmem less than 4GB)
        """
        return self._total_vmem

    @property
    def pciId(self) -> (int, int, int):
        """Device pci slot id in (bus, device, domain) form"""
        return self._pci_id

    @property
    def isTccDriver(self) -> bool:
        """true if device is a Tesla device using TCC driver, false otherwise"""
        return self._is_tcc

    def getAttr(self, attr: CUdevice_attribute) -> int:
        """Get cuda device attribute e"""
        return cuda.cuDeviceGetAttr(attr, self.handle)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        x, y = self.computeCapability
        a, b, c = self.pciId
        mem_in_mb = self.totalGlobalVmem / 1024 / 1024
        sentences = [
            f"Device Name: {self.name}",
            f"Device UUID: {self.uuid}",
            f"Compute Capability: {x}.{y}",
            f"Total Memoty: {mem_in_mb}MBytes",
            f"PCI ID: {a}:{b}:{c}",
            f"Is Using Tcc Driver: {self.isTccDriver}",
        ]
        mlen = max(map(lambda x: len(x), sentences))
        sentences.insert(0, "=" * mlen)
        sentences.append("=" * mlen)
        return "\n".join(sentences)
