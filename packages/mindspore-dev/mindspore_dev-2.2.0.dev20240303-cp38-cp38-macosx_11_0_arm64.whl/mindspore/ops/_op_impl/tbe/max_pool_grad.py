# Copyright 2020 Huawei Technologies Co., Ltd
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
# ============================================================================

"""MaxPoolGrad op"""
from mindspore.ops.op_info_register import op_info_register, TBERegOp, DataType

max_pool_grad_op_info = TBERegOp("MaxPoolGrad") \
    .fusion_type("OPAQUE") \
    .async_flag(False) \
    .binfile_name("max_pool_grad.so") \
    .compute_cost(10) \
    .kernel_name("max_pool_grad") \
    .partial_flag(True) \
    .attr("kernel_size", "required", "listInt", "all") \
    .attr("strides", "required", "listInt", "all") \
    .attr("pad_mode", "required", "str", "all") \
    .attr("format", "optional", "str", "all", "NHWC") \
    .input(0, "x1", False, "required", "all") \
    .input(1, "x2", False, "required", "all") \
    .input(2, "grad", False, "required", "all") \
    .output(0, "y", False, "required", "all") \
    .dtype_format(DataType.None_None, DataType.None_None, DataType.None_None, DataType.None_None) \
    .dynamic_shape(True) \
    .is_dynamic_format(True) \
    .get_op_info()


@op_info_register(max_pool_grad_op_info)
def _max_pool_grad_tbe():
    """MaxPoolGrad TBE register"""
    return
