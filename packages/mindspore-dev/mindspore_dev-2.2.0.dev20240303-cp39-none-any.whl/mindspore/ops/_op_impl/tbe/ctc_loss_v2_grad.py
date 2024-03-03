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

"""CTC_LossV2Grad op"""
from mindspore.ops.op_info_register import op_info_register, TBERegOp, DataType

ctc_loss_v2_grad_info = TBERegOp("CTCLossV2Grad") \
    .fusion_type("OPAQUE") \
    .async_flag(False) \
    .binfile_name("ctc_loss_v2_grad.so") \
    .compute_cost(10) \
    .kernel_name("ctc_loss_v2_grad") \
    .partial_flag(True) \
    .attr("blank", "optional", "int", "all", "0") \
    .attr("reduction", "optional", "str", "all", "none") \
    .attr("zero_infinity", "optional", "bool", "all", "false") \
    .input(0, "grad_out", False, "required", "all") \
    .input(1, "log_probs", False, "required", "all") \
    .input(2, "targets", False, "required", "all") \
    .input(3, "input_lengths", False, "required", "all") \
    .input(4, "target_lengths", False, "required", "all") \
    .input(5, "neg_log_likelihood", False, "required", "all") \
    .input(6, "log_alpha", False, "required", "all") \
    .output(0, "grad", False, "required", "all") \
    .dtype_format(DataType.F32_Default, DataType.F32_Default, DataType.I32_Default, DataType.I32_Default,
                  DataType.I32_Default, DataType.F32_Default, DataType.F32_Default, DataType.F32_Default) \
    .get_op_info()

@op_info_register(ctc_loss_v2_grad_info)
def _ctc_loss_v2_grad_tbe():
    """CTCLossV2Grad TBE register"""
    return
