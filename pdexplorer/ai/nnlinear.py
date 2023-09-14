from ..search import search_iterable
from ..dataset import current


def nnlinear(varlist: str):
    # https://pytorch.org/tutorials/beginner/pytorch_with_examples.html#pytorch-nn
    import torch
    import math

    # Create Tensors to hold input and outputs.
    x = torch.linspace(-math.pi, math.pi, 2000)
    y = torch.sin(x)

    # For this example, the output y is a linear function of (x, x^2, x^3), so
    # we can consider it as a linear layer neural network. Let's prepare the
    # tensor (x, x^2, x^3).
    p = torch.tensor([1, 2, 3])
    xx = x.unsqueeze(-1).pow(p)

    varlist_as_list = varlist.split()
    yvar = varlist_as_list[0]
    xvars = varlist_as_list[1:]
    xvars = search_iterable(current.df.columns, " ".join(xvars))

    X_numpy = current.df.dropna()[xvars].values
    y_numpy = current.df.dropna()[[yvar]].values

    xx = torch.tensor(X_numpy)
    y = torch.tensor(y_numpy)

    print(y.shape)
    print(xx.shape)
    print(y)
    print(xx)

    # In the above code, x.unsqueeze(-1) has shape (2000, 1), and p has shape
    # (3,), for this case, broadcasting semantics will apply to obtain a tensor
    # of shape (2000, 3)

    # Use the nn package to define our model as a sequence of layers. nn.Sequential
    # is a Module which contains other Modules, and applies them in sequence to
    # produce its output. The Linear Module computes output from input using a
    # linear function, and holds internal Tensors for its weight and bias.
    # The Flatten layer flatens the output of the linear layer to a 1D tensor,
    # to match the shape of `y`.
    model = torch.nn.Sequential(torch.nn.Linear(3, 1), torch.nn.Flatten(0, 1))

    # The nn package also contains definitions of popular loss functions; in this
    # case we will use Mean Squared Error (MSE) as our loss function.
    loss_fn = torch.nn.MSELoss(reduction="sum")

    learning_rate = 1e-6
    for t in range(2000):

        # Forward pass: compute predicted y by passing x to the model. Module objects
        # override the __call__ operator so you can call them like functions. When
        # doing so you pass a Tensor of input data to the Module and it produces
        # a Tensor of output data.
        y_pred = model(xx)

        # Compute and print loss. We pass Tensors containing the predicted and true
        # values of y, and the loss function returns a Tensor containing the
        # loss.
        loss = loss_fn(y_pred, y)
        if t % 100 == 99:
            print(t, loss.item())

        # Zero the gradients before running the backward pass.
        model.zero_grad()

        # Backward pass: compute gradient of the loss with respect to all the learnable
        # parameters of the model. Internally, the parameters of each Module are stored
        # in Tensors with requires_grad=True, so this call will compute gradients for
        # all learnable parameters in the model.
        loss.backward()

        # Update the weights using gradient descent. Each parameter is a Tensor, so
        # we can access its gradients like we did before.
        with torch.no_grad():
            for param in model.parameters():
                param -= learning_rate * param.grad

    # You can access the first layer of `model` like accessing the first item of a list
    linear_layer = model[0]

    # For linear layer, its parameters are stored as `weight` and `bias`.
    print(
        f"Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} x + {linear_layer.weight[:, 1].item()} x^2 + {linear_layer.weight[:, 2].item()} x^3"
    )

    # import torch
    # import torch.nn as nn
    # import numpy as np
    # from sklearn import datasets
    # import matplotlib.pyplot as plt

    # varlist_as_list = varlist.split()
    # yvar = varlist_as_list[0]
    # xvars = varlist_as_list[1:]
    # xvars = search_iterable(current.df.columns, " ".join(xvars))

    # X_numpy = current.df.dropna()[xvars].values
    # y_numpy = current.df.dropna()[yvar].astype(float).values

    # # 0) Prepare data
    # # X_numpy, y_numpy = datasets.make_regression(
    # #     n_samples=100, n_features=2, noise=20, random_state=4
    # # )
    # print(X_numpy)
    # print(y_numpy)

    # # cast to float Tensor
    # X = torch.from_numpy(X_numpy.astype(np.float32))
    # y = torch.from_numpy(y_numpy.astype(np.float32))
    # y = y.view(y.shape[0], 1)

    # n_samples, n_features = X.shape

    # # 1) Model
    # # Linear model f = wx + b
    # input_size = n_features
    # output_size = 1
    # model = nn.Linear(input_size, output_size)

    # # 2) Loss and optimizer
    # learning_rate = 0.01

    # criterion = nn.MSELoss()
    # optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    # # 3) Training loop
    # num_epochs = 100
    # for epoch in range(num_epochs):
    #     # Forward pass and loss
    #     y_predicted = model(X)
    #     loss = criterion(y_predicted, y)

    #     # Backward pass and update
    #     loss.backward()
    #     optimizer.step()

    #     # zero grad before new step
    #     optimizer.zero_grad()

    #     if (epoch + 1) % 10 == 0:
    #         print(f"epoch: {epoch+1}, loss = {loss.item():.4f}")

    # # Plot
    # # predicted = model(X).detach().numpy()

    # # plt.plot(X_numpy, y_numpy, "ro")
    # # plt.plot(X_numpy, predicted, "b")
    # # plt.show()
