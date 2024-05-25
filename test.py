import torch
import torch.nn as nn
import torch.nn.functional as F

# A = nn.Linear(2, 3, bias=False)
# A.weight.requires_grad = False
# A.weight = torch.nn.Parameter(torch.tensor([[1, 4], [2, 5], [3, 6]], dtype=torch.float32))
# print(f'A: {A.weight}')

# x = torch.tensor([[1, 1]], dtype=torch.float32)
# print(f'{x = }')

# y = A(x)
# print(f'{y = }')

# z = y @ A.weight
# print(f'{z = }')

# print available torch devices and current device
print(f'{torch.cuda.is_available() = }')
print(f'{torch.cuda.current_device() = }')
print(f'{torch.cuda.device_count() = }')
print(f'{torch.cuda.get_device_name() = }')
print(f'{torch.cuda.memory_allocated() = }')
print(f'{torch.cuda.memory_reserved() = }')
