# JUST A DEMO OF HOW LINEAR REGRESSION WORKS WITH NN #
from ..._search import search_iterable
from ..._dataset import current
from ..._get_custom_attributes import _get_custom_attributes
from ..._patsify import _patsify
from ..._print import _print
from typing import Union


def regressnn(varlist: str, use_dataloader=False, epochs: int = 100):
    if not use_dataloader:
        import numpy as np
        import torch
        from torch.autograd import Variable

        varlist_as_list = varlist.split()
        yvar = varlist_as_list[0]
        xvars = varlist_as_list[1:]
        xvars = search_iterable(current.df.columns, " ".join(xvars))
        x_train = current.df.dropna()[xvars].values
        y_train = current.df.dropna()[[yvar]].values
        X = torch.tensor(x_train).to(torch.float32)
        y = torch.tensor(y_train).to(torch.float32)
        inputDim = X.shape[1]  # takes variable 'x'
        outputDim = 1  # takes variable 'y'
        learningRate = 0.01
        epochs = epochs
        model = torch.nn.Linear(inputDim, outputDim)
        ##### For GPU #######
        if torch.cuda.is_available():
            model.cuda()
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.Rprop(model.parameters(), lr=learningRate)

        for epoch in range(epochs):
            # Converting inputs and labels to Variable
            if torch.cuda.is_available():
                inputs = X.cuda()
                labels = y.cuda()
            else:
                inputs = X
                labels = y

            # https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html#optimizer
            # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
            optimizer.zero_grad()

            # get output from the model, given the inputs
            outputs = model(inputs)

            # get loss for the predicted output
            loss = criterion(outputs, labels)
            # print(loss)
            # get gradients w.r.t to parameters
            loss.backward()

            # update parameters
            optimizer.step()
        return model  # type: ignore
    else:
        # same as above, but using the dataloader
        import torch
        from torch.autograd import Variable

        ds = current.get_pytorch_dataset(varlist)
        dl = current.get_pytorch_dataloader(varlist)
        inputDim = ds.x_train.shape[1]  # takes variable 'x'
        outputDim = 1  # takes variable 'y'
        learningRate = 0.01
        epochs = epochs

        model = torch.nn.Linear(inputDim, outputDim)
        ##### For GPU #######
        if torch.cuda.is_available():
            model.cuda()
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.Rprop(model.parameters(), lr=learningRate)
        for epoch in range(epochs):
            for X, y in dl:
                # print(X.shape)
                # Converting inputs and labels to Variable
                if torch.cuda.is_available():
                    inputs = X.cuda()
                    labels = y.cuda()
                else:
                    inputs = X
                    labels = y

                # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
                optimizer.zero_grad()

                # get output from the model, given the inputs
                outputs = model(inputs)

                # get loss for the predicted output
                loss = criterion(outputs, labels)
                # print(loss)
                # get gradients w.r.t to parameters
                loss.backward()

                # update parameters
                optimizer.step()
        return model  # type: ignore
