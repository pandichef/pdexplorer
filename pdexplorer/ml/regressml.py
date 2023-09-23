from .._search import search_iterable
from .._dataset import current
from .._get_custom_attributes import _get_custom_attributes
from .._patsify import _patsify
from .._print import _print

# from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing import Union


def regressml(varlist: str):
    # ) -> Union[RegressionResultsWrapper, LinearRegression, None]:
    """
    Stata docs: https://www.stata.com/manuals/rregress.pdf
    Returns: https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html
    """
    # if library == "statsmodels":
    #     import statsmodels.formula.api as smf

    #     df = current.df
    #     patsy_formula = _patsify(varlist)
    #     # print(patsy_formula)
    #     model = smf.ols(patsy_formula, data=df, missing="drop")
    #     results = model.fit()
    #     _print(results.summary())
    #     current.methods, current.properties = _get_custom_attributes(results)
    #     # print(results)
    #     # print(current.properties)
    #     current.stored_results["e"] = {}
    #     current.stored_results["e"] = {
    #         "scalars": {
    #             "N": int(results.nobs),
    #             "df_m": int(results.df_model),
    #             "df_r": int(results.df_resid),
    #             "F": results.fvalue,
    #             "r2": results.rsquared,
    #             "mss": results.mse_model,
    #             "r2_a": results.rsquared_adj,
    #             "ll": results.llf,
    #         }
    #     }
    #     return results
    # elif library == "sklearn" or library == "scikit-learn":
    from sklearn.linear_model import LinearRegression

    # import numpy as np

    varlist_as_list = varlist.split()
    yvar = varlist_as_list[0]
    xvars = varlist_as_list[1:]
    xvars = search_iterable(current.df.columns, " ".join(xvars))
    X = current.df.dropna()[xvars].values
    y = current.df.dropna()[yvar].values
    reg = LinearRegression().fit(X, y)
    return reg


#     elif library == "pytorch":
#         # Source: https://towardsdatascience.com/linear-regression-with-pytorch-eb6dedead817
#         # This didn't work with SDG, so I used Rprop instead
#         import numpy as np
#         import torch
#         from torch.autograd import Variable

#         # class linearRegression(torch.nn.Module):
#         #     def __init__(self, inputSize, outputSize):
#         #         super(linearRegression, self).__init__()
#         #         self.linear = torch.nn.Linear(inputSize, outputSize)

#         #     def forward(self, x):
#         #         out = self.linear(x)
#         #         return out

#         if varlist == "":
#             # create dummy data for training
#             x_values = [i for i in range(11)]
#             x_train = np.array(x_values, dtype=np.float32)
#             x_train = x_train.reshape(-1, 1)

#             y_values = [2 * i + 1 for i in x_values]
#             y_train = np.array(y_values, dtype=np.float32)
#             y_train = y_train.reshape(-1, 1)
#             X = torch.tensor(x_train)
#             y = torch.tensor(y_train)
#         else:
#             varlist_as_list = varlist.split()
#             yvar = varlist_as_list[0]
#             xvars = varlist_as_list[1:]
#             xvars = search_iterable(current.df.columns, " ".join(xvars))
#             x_train = current.df.dropna()[xvars].values
#             y_train = current.df.dropna()[[yvar]].values
#             X = torch.tensor(x_train).to(torch.float32)
#             y = torch.tensor(y_train).to(torch.float32)

#         # print(X.dtype)
#         # print(y.dtype)
#         print(X.shape)
#         print(y.shape)
#         # print(X.shape[1])
#         # print(X)
#         # print(y)

#         inputDim = X.shape[1]  # takes variable 'x'
#         outputDim = 1  # takes variable 'y'
#         learningRate = 0.01
#         epochs = epochs

#         # model = linearRegression(inputDim, outputDim)
#         model = torch.nn.Linear(inputDim, outputDim)
#         ##### For GPU #######
#         if torch.cuda.is_available():
#             model.cuda()
#         criterion = torch.nn.MSELoss()
#         optimizer = torch.optim.Rprop(model.parameters(), lr=learningRate)

#         for epoch in range(epochs):
#             # Converting inputs and labels to Variable
#             if torch.cuda.is_available():
#                 inputs = X.cuda()
#                 labels = y.cuda()
#             else:
#                 inputs = X
#                 labels = y

#             # print(inputs)
#             # print(labels)

#             # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
#             optimizer.zero_grad()

#             # get output from the model, given the inputs
#             outputs = model(inputs)

#             # get loss for the predicted output
#             loss = criterion(outputs, labels)
#             # print(loss)
#             # get gradients w.r.t to parameters
#             loss.backward()

#             # update parameters
#             optimizer.step()

#             # print("epoch {}, loss {}".format(epoch, loss.item()))

#         """
#         with torch.no_grad():  # we don't need gradients in the testing phase
#             if torch.cuda.is_available():
#                 predicted = model(X.cuda()).cpu().data.numpy()
#             else:
#                 predicted = model(X).data.numpy()
#             # print(predicted)

#         plt.clf()
#         plt.plot(x_train, y_train, "go", label="True data", alpha=0.5)
#         plt.plot(x_train, predicted, "--", label="Predictions", alpha=0.5)
#         plt.legend(loc="best")
#         plt.show()
#         """

#         return model  # type: ignore
#     elif library == "pytorch_dataloader":
#         # same as above, but using the dataloader
#         import torch
#         from torch.autograd import Variable

#         ds = current.get_pytorch_dataset(varlist)
#         dl = current.get_pytorch_dataloader(varlist)

#         print(ds.x_train.shape)
#         print(ds.y_train.shape)
#         # print(y.shape)

#         inputDim = ds.x_train.shape[1]  # takes variable 'x'
#         outputDim = 1  # takes variable 'y'
#         learningRate = 0.01
#         epochs = epochs

#         model = torch.nn.Linear(inputDim, outputDim)
#         ##### For GPU #######
#         if torch.cuda.is_available():
#             model.cuda()
#         criterion = torch.nn.MSELoss()
#         optimizer = torch.optim.Rprop(model.parameters(), lr=learningRate)

#         for epoch in range(epochs):
#             for batch, (X, y) in enumerate(dl):
#                 # Converting inputs and labels to Variable
#                 if torch.cuda.is_available():
#                     inputs = X.cuda()
#                     labels = y.cuda()
#                 else:
#                     inputs = X
#                     labels = y

#                 # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
#                 optimizer.zero_grad()

#                 # get output from the model, given the inputs
#                 outputs = model(inputs)

#                 # get loss for the predicted output
#                 loss = criterion(outputs, labels)
#                 # print(loss)
#                 # get gradients w.r.t to parameters
#                 loss.backward()

#                 # update parameters
#                 optimizer.step()

#                 # print("epoch {}, loss {}".format(epoch, loss.item()))

#         return model  # type: ignore
#     else:
#         raise Exception("Invalid library name.")


# """
# def regress2(varlist: str):
#     # https://www.stata.com/manuals/rregress.pdf
#     # page 6
#     # regress mpg weight foreign
#     df = singleton.df

#     varlist_as_list = varlist.split()
#     yvar = varlist_as_list[0]
#     xvars = varlist_as_list[1:]

#     xvars = search_iterable(df.columns, " ".join(xvars))

#     for col in df.columns:
#         if isinstance(df[col].dtype, CategoricalDtype):
#             df[col] = df[col].cat.codes

#     X = df[xvars]
#     y = df[yvar]

#     X = sm.add_constant(X)
#     results = sm.OLS(y, X).fit()
#     print(results.summary())
#     # print(type(results))
#     # print(results.params)
#     # return get_custom_attributes(results)
#     singleton.methods, singleton.properties = get_custom_attributes(results)
#     # pprint(custom_methods)
#     # pprint(custom_properties)
#     return results
# """

