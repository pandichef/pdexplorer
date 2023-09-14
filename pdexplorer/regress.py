import matplotlib.pyplot as plt
from pprint import pprint
import statsmodels.api as sm
import numpy as np
import pandas as pd
from pandas import CategoricalDtype
from .search import search_iterable
from .dataset import current
from ._get_custom_attributes import _get_custom_attributes
from ._patsify import _patsify
import statsmodels.formula.api as smf
from ._print import _print

# from statsmodels.regression.linear_model import RegressionResultsWrapper

# smf.logit


def regress(varlist: str, library="statsmodels", epochs=100):
    if library == "statsmodels":
        df = current.df
        patsy_formula = _patsify(varlist)
        # print(patsy_formula)
        model = smf.ols(patsy_formula, data=df, missing="drop")
        results = model.fit()
        _print(results.summary())
        current.methods, current.properties = _get_custom_attributes(results)
        # print(results)
        return results
    elif library == "sklearn":
        # import numpy as np
        from sklearn.linear_model import LinearRegression

        varlist_as_list = varlist.split()
        yvar = varlist_as_list[0]
        xvars = varlist_as_list[1:]
        xvars = search_iterable(current.df.columns, " ".join(xvars))
        X = current.df.dropna()[xvars].values
        y = current.df.dropna()[yvar].values
        reg = LinearRegression().fit(X, y)
        return reg
    elif library == "pytorch":
        # Source: https://towardsdatascience.com/linear-regression-with-pytorch-eb6dedead817
        # This didn't work with SDG, so I used Rprop instead
        import torch
        from torch.autograd import Variable

        if varlist == "":
            # create dummy data for training
            x_values = [i for i in range(11)]
            x_train = np.array(x_values, dtype=np.float32)
            x_train = x_train.reshape(-1, 1)

            y_values = [2 * i + 1 for i in x_values]
            y_train = np.array(y_values, dtype=np.float32)
            y_train = y_train.reshape(-1, 1)
            X = torch.tensor(x_train)
            y = torch.tensor(y_train)
        else:
            varlist_as_list = varlist.split()
            yvar = varlist_as_list[0]
            xvars = varlist_as_list[1:]
            xvars = search_iterable(current.df.columns, " ".join(xvars))
            x_train = current.df.dropna()[xvars].values
            y_train = current.df.dropna()[[yvar]].values
            X = torch.tensor(x_train).to(torch.float32)
            y = torch.tensor(y_train).to(torch.float32)

        # print(X.dtype)
        # print(y.dtype)
        print(X.shape)
        print(y.shape)
        # print(X.shape[1])
        # print(X)
        # print(y)

        class linearRegression(torch.nn.Module):
            def __init__(self, inputSize, outputSize):
                super(linearRegression, self).__init__()
                self.linear = torch.nn.Linear(inputSize, outputSize)

            def forward(self, x):
                out = self.linear(x)
                return out

        inputDim = X.shape[1]  # takes variable 'x'
        outputDim = 1  # takes variable 'y'
        learningRate = 0.01
        epochs = epochs

        model = linearRegression(inputDim, outputDim)
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

            # print("epoch {}, loss {}".format(epoch, loss.item()))

        """
        with torch.no_grad():  # we don't need gradients in the testing phase
            if torch.cuda.is_available():
                predicted = model(X.cuda()).cpu().data.numpy()
            else:
                predicted = model(X).data.numpy()
            # print(predicted)

        plt.clf()
        plt.plot(x_train, y_train, "go", label="True data", alpha=0.5)
        plt.plot(x_train, predicted, "--", label="Predictions", alpha=0.5)
        plt.legend(loc="best")
        plt.show()
        """

        return model


"""
def regress2(varlist: str):
    # https://www.stata.com/manuals/rregress.pdf
    # page 6
    # regress mpg weight foreign
    df = singleton.df

    varlist_as_list = varlist.split()
    yvar = varlist_as_list[0]
    xvars = varlist_as_list[1:]

    xvars = search_iterable(df.columns, " ".join(xvars))

    for col in df.columns:
        if isinstance(df[col].dtype, CategoricalDtype):
            df[col] = df[col].cat.codes

    X = df[xvars]
    y = df[yvar]

    X = sm.add_constant(X)
    results = sm.OLS(y, X).fit()
    print(results.summary())
    # print(type(results))
    # print(results.params)
    # return get_custom_attributes(results)
    singleton.methods, singleton.properties = get_custom_attributes(results)
    # pprint(custom_methods)
    # pprint(custom_properties)
    return results
"""

