# Copyright (c) 2024 Yansheng Zhu
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


class CudaError(Exception):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self) -> str:
        return self.reason

    def __repr__(self) -> str:
        return self.reason
