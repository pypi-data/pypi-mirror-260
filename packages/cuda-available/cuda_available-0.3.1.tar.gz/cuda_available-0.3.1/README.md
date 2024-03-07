## cuda_available

A package for checking available CUDA device information

![GitHub License](https://img.shields.io/github/license/AlexZhu2001/cuda_available)
![PyPI - Version](https://img.shields.io/pypi/v/cuda-available)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/alexzhu2001/cuda_available/build.yml)

### Usage
#### Basic usage
```Python
from cuda_available import *

cnt = getCudaDeviceCount()
print(f"Cuda device count: {cnt}")
for idx in range(cnt):
    print(CudaDeviceInfo(idx))
```

#### Get count of cuda device
```Python
from cuda_available import *

cnt = getCudaDeviceCount()
print(f"Cuda device count: {cnt}")
```

#### Check if cuda init successful
```Python
from cuda_available import *

state = "Succeed" if isCudaInitSuccess() else "Failed"
print(f"Cuda init state: {state}")
```

#### Get CUDA driver version
```Python
from cuda_available import *

version = cudaDriverVersion()
print(f"Cuda driver version: {version}")
```

#### Get infomation of cuda device
```Python
from cuda_available import *

cnt = getCudaDeviceCount()
for idx in range(cnt):
    info = CudaDeviceInfo(idx)
    print(f"UUID: {info.uuid}")
    print(f"Name: {info.name}")
    print(f"ComputeCapability: {info.computeCapability}")
    print(f"TotalGlobalVmem: {info.totalGlobalVmem}")
    print(f"PciId: {info.pciId}")
    print(f"UsingTccDriver: {info.isTccDriver}")
    print("===================================")
```

### Advanced usage
#### Get more cuda attribute
```Python
from cuda_available import *

cnt = getCudaDeviceCount()
for idx in range(cnt):
    info = CudaDeviceInfo(idx)
    mem_clock_rate = info.getAttr(CUdevice_attribute.CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE)
    print(f"The memory clock rate is {mem_clock_rate / 1000 / 1000} GHz")
```

#### Using custom cuda lib name
**Warning: This situation is very rare, please do so when making sure you know what you are doing**
```Python
from cuda_available import *

# if you are using windows, it will search for <cuda_lib_name>.dll
# if you are using linux, it will search for [lib]<cuda_lib_name>.so[.X]
setCudaDylibName("cuda_lib_name")

cnt = getCudaDeviceCount()
for idx in range(cnt):
    info = CudaDeviceInfo(idx)
    print(f"UUID: {info.uuid}")
    print(f"Name: {info.name}")
    print(f"ComputeCapability: {info.computeCapability}")
    print(f"TotalGlobalVmem: {info.totalGlobalVmem}")
    print(f"PciId: {info.pciId}")
    print(f"UsingTccDriver: {info.isTccDriver}")
    print("===================================")
```
