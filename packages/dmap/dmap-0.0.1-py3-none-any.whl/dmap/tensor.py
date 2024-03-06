from __future__ import annotations
import functools
import operator
from copy import deepcopy
from dmap.memory import Memory
from dmap.ops import BinaryOp, MemoryOp, MovementOp, ReduceOp, UnaryOp

class Tensor:
    def __init__(
            self, 
            shape: list[int], 
            stride: list[int] | None = None, 
            parents: list[Tensor] = [],
            op: BinaryOp | MemoryOp | MovementOp | ReduceOp | UnaryOp | None = None
        ) -> Tensor:
        # Control flow for setting both the operation and memory fields.
        if not op:
            self._op: MemoryOp = MemoryOp()
            self._memory: Memory = Memory(shape = shape, safe_op = True, stride = None)
        elif op.op != "UNSAFE_RESHAPE":
            self._op: BinaryOp | MovementOp | ReduceOp | UnaryOp = op
            self._memory: Memory = Memory(shape = shape, safe_op = True, stride = None)
        else:
            self._op: MovementOp = op
            self._memory: Memory = Memory(shape = shape, safe_op = False, stride = stride)
        self._parents: list[Tensor] = parents
        self._children: list[Tensor] = []

    # Memory Operations
    def safe_reshape(self, new_shape: list[int]) -> Tensor:
        new_size = functools.reduce(operator.mul, new_shape)
        assert new_size > 0, "The specified reshape cannot be performed as it has atleast one dimension of size zero."
        assert new_size == functools.reduce(operator.mul, self._memory.view), "The specified reshape cannot be performed as it results in a different sized region of memory than the original allocation."
        operation = MovementOp(op = "SAFE_RESHAPE", view = new_shape)
        child = Tensor(shape = new_shape, parents = [self], op = operation)
        self._children.append(child)
        return child

    # Permute and expand are unsafe reshapes.
    def _unsafe_reshape(self, new_shape: list[int], new_stride: list[int]) -> Tensor:
        assert functools.reduce(operator.mul, new_shape) > 0, "The specified reshape cannot be performed as it has atleast one dimension of size zero."
        assert len(new_shape) == len(new_stride), "The specified reshape cannot be performed because the number of dimensions provided for the shape and stride do not match."
        operation = MovementOp(op = "UNSAFE_RESHAPE", view = new_shape, stride = new_stride)
        child = Tensor(shape = new_shape, stride = new_stride, parents = [self], op = operation)
        self._children.append(child)
        return child

    # Binary Operations
    def _binary_operation(self, tensor_2: Tensor, op_type: str) -> Tensor:
        assert self._memory.view == tensor_2._memory.view, "The operation cannot be performed because the two tensors do not have identical shapes."
        operation = BinaryOp(op = op_type)
        child = Tensor(shape = self._memory.view, parents = [self, tensor_2], op = operation)
        self._children.append(child)
        tensor_2._children.append(child)
        return child
    
    def add(self, tensor_2: Tensor) -> Tensor:
        return self._binary_operation(tensor_2 = tensor_2, op_type = "ADD")
    
    def div(self, tensor_2: Tensor) -> Tensor:
        return self._binary_operation(tensor_2 = tensor_2, op_type = "DIV")
    
    def mul(self, tensor_2: Tensor) -> Tensor:
        return self._binary_operation(tensor_2 = tensor_2, op_type = "MUL")
    
    def sub(self, tensor_2: Tensor) -> Tensor:
        return self._binary_operation(tensor_2 = tensor_2, op_type = "SUB")
    
    # Reduction Operations
    def _reduction(self, axis: int, op_type: str) -> Tensor:
        assert axis >= 0, "The reduction operation cannot be perfomed along a negative axis."
        assert axis <= len(self._memory.view) - 1, "The reduction operation cannot be performed because the axis provided is greater than the number of dimensions in the tensor."
        operation = ReduceOp(op = op_type, axis = axis)
        new_shape = deepcopy(self._memory.view)
        new_shape.pop(axis)
        child = Tensor(shape = new_shape, parents = [self], op = operation)
        self._children.append(child)
        return child
    
    def max(self, axis: int) -> Tensor:
        return self._reduction(axis = axis, op_type = "MAX")
    
    def min(self, axis: int) -> Tensor:
        return self._reduction(axis = axis, op_type = "MIN")

    def sum(self, axis: int) -> Tensor:
        return self._reduction(axis = axis, op_type = "SUM")
    
    # Topological Sort
    def _topological_sort(self) -> list[Tensor]:
        def top_sort_util(tensor, visited, stack) -> list[Tensor]:
            visited.add(tensor)
            for parent in tensor._parents:
                if parent not in visited:
                    top_sort_util(parent, visited, stack)
            stack.append(tensor)
            return stack
        return top_sort_util(self, set(), [])