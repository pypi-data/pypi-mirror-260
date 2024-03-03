# Copyright 2021 Huawei Technologies Co., Ltd
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

"""LogicalNot op"""
from mindspore.ops.op_info_register import op_info_register, TBERegOp, DataType

logical_not_op_info = TBERegOp("LogicalNot") \
    .fusion_type("ELEMWISE") \
    .async_flag(False) \
    .binfile_name("logical_not.so") \
    .compute_cost(10) \
    .kernel_name("logical_not") \
    .dynamic_shape(True) \
    .partial_flag(True) \
    .input(0, "x", False, "required", "all") \
    .output(0, "y", True, "required", "all") \
    .op_pattern("formatAgnostic") \
    .dtype_format(DataType.BOOL_None, DataType.BOOL_None) \
    .get_op_info()


@op_info_register(logical_not_op_info)
def _logical_not_ds_tbe():
    """LogicalNot TBE register"""
    return
