import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import logging

logging.basicConfig(filename=".cache/classification.log", level=logging.INFO, filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def predict(data):
    df = data.to_frame()
    
    df['returns'] = np.log(df / df.shift(1))
    df.dropna(inplace=True)
    df['direction'] = np.sign(df['returns']).astype(int)
    plot_daily_returns(df)

    lag_cols = add_lags(df)
    cols_bin = add_bins(df, lag_cols)
    models = {
        'MLP' : MLPClassifier(max_iter=500),
        'gauss_nb': GaussianNB(),
        'svm': SVC(),
        'random_forest': RandomForestClassifier(max_depth=10, n_estimators=100),
        'log_reg': linear_model.LogisticRegression(),
    }
    fit_models(df, models, cols_bin)
    predict_positions(df, models, cols_bin)
    strategies = evaluate_strats(df, models)

    logger.info('\nTotal Returns:')
    logger.info(df[strategies].sum().apply(np.exp))
    logger.info('\nAnnual Volatility:')
    logger.info(df[strategies].std() * 252 ** 0.5)
    plot_return_comparison(df, strategies)
    df.to_csv('.cache/classification.csv', sep='\t')

    predictions = df['strategy_svm']
    predictions = pd.DataFrame(predictions)
    predictions.rename(columns = {'strategy_svm': 'predicted'}, inplace=True)
    return predictions

def evaluate_strats(df, models):
    strategies = []
    for model in models.keys():
        col = 'strategy_' + model
        df[col] = df['pos_' + model] * df['returns']
        strategies.append(col)
    strategies.insert(0,'returns')
    return strategies


def predict_positions(df, models, cols_bin):
    for model in models.keys():
        df['pos_' + model] = models[model].predict(df[cols_bin])
    
def fit_models(df, models, cols_bin):
    return { model: models[model].fit(df[cols_bin], df['direction']) for model in models.keys() }


def add_lags(df):
    lags = [1, 2, 3, 4, 5]
    cols = []
    for lag in lags:
        col = f'rtn_lag{lag}'
        df[col] = df['returns'].shift(lag)
        cols.append(col)
    
    df.dropna(inplace=True)
    return cols

def add_bins(df, lag_cols, bins=[0]):
    cols_bin = []
    for col in lag_cols:
        col_bin = col + '_bin'
        df[col_bin] = np.digitize(df[col], bins)
        cols_bin.append(col_bin)
    return cols_bin



def plot_daily_returns(df, save=True):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize = (12,6))
    
    ax[0].plot(df['close'], label = 'close price')
    ax[0].set(title = 'Closing Price', ylabel = 'Price')
    ax[0].grid(True)
    ax[0].legend()

    ax[1].plot(df['returns'], label = 'Daily Returns')
    ax[1].set(title = 'Daily Returns', ylabel = 'Returns')
    ax[1].grid(True)
    plt.legend()
    plt.tight_layout()
    if save == True:
        plt.savefig('.cache/daily_returns', dpi=300)
        plt.clf()
    else:
        plt.show()

def plot_return_comparison(df, strategies, save=True):
    logger.info(strategies)
    ax = df[strategies].cumsum().apply(np.exp).plot(figsize=(12, 6), title='Classifiers Return Comparison')
    ax.set_ylabel("Cumulative Returns")
    ax.grid(True)
    plt.tight_layout()
    if save == True:
        plt.savefig('.cache/classifiers_return', dpi=300)
        plt.clf()
    else:
        plt.show()
