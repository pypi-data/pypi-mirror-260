import torch
from torch.utils.data import DataLoader, TensorDataset
from .gd_utils import GD_output

def GD(J, init_parameters, lr, num_steps, decay_rate=0):

    single_parameter = False
    if isinstance(init_parameters, torch.Tensor):
        init_parameters = {'theta': init_parameters}
        single_parameter = True
        
    parameters = {key: tensor.clone().requires_grad_() for key, tensor in init_parameters.items()}
    input_parameters = list(parameters.values())[0] if single_parameter else parameters
    objective = J(input_parameters)
    per_step_objectives = [objective.detach()]
    running_parameters = {key: [tensor.clone()] for key, tensor in init_parameters.items()}

    for t in range(num_steps):

        objective.backward()
        with torch.no_grad():
            for parameter in parameters.values():
                parameter -= lr * (1 - decay_rate) ** (1 + t) * parameter.grad
        for parameter in parameters.values():
            parameter.grad.zero_()
        for param_name in running_parameters.keys():
            running_parameters[param_name].append(parameters[param_name].detach().clone())

        input_parameters = list(parameters.values())[0] if single_parameter else parameters
        objective = J(input_parameters)
        per_step_objectives.append(objective.detach())
        
    for param_name in running_parameters.keys():
        running_parameters[param_name] = torch.stack(running_parameters[param_name], dim=0)
    output = GD_output(parameters=running_parameters,
                       per_step_objectives=torch.stack(per_step_objectives),
                       lr=lr,
                       num_steps=num_steps,
                       grad_steps=range(len(per_step_objectives)),
                       decay_rate=decay_rate,
                       type_flag='gd')
    return output


def SGD(L, init_parameters, X, lr, batch_size, num_epochs, y=None, decay_rate=0, max_steps=-1, shuffle=True, random_state=None):

    if random_state != None:
        torch.manual_seed(random_state)
    dataset = TensorDataset(X, y) if y != None else X
    data_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=shuffle)
    num_mini_batches = len(data_loader)
    
    single_parameter = False
    if isinstance(init_parameters, torch.Tensor):
        init_parameters = {'theta': init_parameters}
        single_parameter = True
    
    parameters = {param_name: param.clone().requires_grad_() for param_name, param in init_parameters.items()}
    per_step_objectives = []
    per_epoch_objectives = []
    running_parameters = {param_name: [param.clone()] for param_name, param in init_parameters.items()}
    first_step = True
    s = 0
    epoch_step_nums = [0]

    for t in range(num_epochs):
        for i, mini_batch in enumerate(data_loader):
            
            input_parameters = list(parameters.values())[0] if single_parameter else parameters
            if first_step:
                objective = L(input_parameters, *mini_batch).mean() if y != None else L(input_parameters, mini_batch).mean()
                per_step_objectives.append(objective.detach())
                per_epoch_objectives.append(objective.detach())
                first_step = False

            objective.backward()
            with torch.no_grad():
                for parameter in parameters.values():
                    parameter -= lr * (1 - decay_rate) ** (1 + s) * parameter.grad
            for param_name in running_parameters.keys():
                running_parameters[param_name].append(parameters[param_name].detach().clone())
            for parameter in parameters.values():
                parameter.grad.zero_()
            
            objective = L(input_parameters, *mini_batch).mean() if y != None else L(input_parameters, mini_batch).mean()
            per_step_objectives.append(objective.detach())
            
            complete_epoch = True if i + 1 == num_mini_batches else False
            s += 1
            if s == max_steps:
                break
        
        if complete_epoch:
            epoch_step_nums.append(s)
        
        epoch_objective = torch.tensor(per_step_objectives[num_mini_batches * t + 1:])
        per_epoch_objectives.append(epoch_objective.mean())

        if s == max_steps:
            break

    for param_name in running_parameters.keys():
        running_parameters[param_name] = torch.stack(running_parameters[param_name], dim=0)
    output = GD_output(parameters=running_parameters,
                       per_step_objectives=torch.stack(per_step_objectives),
                       per_epoch_objectives=torch.stack(per_epoch_objectives),
                       epoch_step_nums=torch.tensor(epoch_step_nums),
                       grad_steps=range(len(per_step_objectives)),
                       lr=lr,
                       num_epochs=num_epochs,
                       decay_rate=decay_rate,
                       batch_size=batch_size,
                       max_steps=max_steps)
    return output