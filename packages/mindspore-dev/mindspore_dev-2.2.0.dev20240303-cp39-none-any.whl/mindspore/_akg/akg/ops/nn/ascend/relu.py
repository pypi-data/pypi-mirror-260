#!/usr/bin/env python3
# coding: utf-8
# Copyright 2019-2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""operator dsl function: relu"""

import akg.tvm
import akg.utils as utils


@utils.check_input_type(akg.tvm.tensor.Tensor)
def Relu(inputs, target=utils.CCE):
    """
    Compute rectified linear of input tensor.

    Return max(inputs, 0) element-wise.

    Args:
        inputs (tvm.tensor.Tensor): Input tensor.

    Returns:
        tvm.tensor.Tensor with the same type and shape as data.
    
    Supported Platforms:
        'Ascend'
    """
    utils.check_shape(inputs.shape)
    utils.ops_dtype_check(inputs.dtype, utils.DtypeForDavinci.ALL_FLOAT)
    output = akg.tvm.compute(inputs.shape, lambda *i: akg.tvm.max(inputs(*i),
                                                                  akg.tvm.const(0, inputs.dtype)), name="output")
    return output
