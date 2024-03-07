import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import ast

BENCHMARKING_SCORES_PKL = "./bm_scores.pkl"
PARAMETR_SERACH_SCORES = "./ps_scores_without_pred_lbl.pkl"


def xfloat(content: str):
    try:
        return float(content)
    except Exception:
        return -999.999


def filter_first_group(df, group_column):
    return df[df[group_column].eq(df[group_column].iloc[0])]


def parse_benchmarking_scores() -> pd.DataFrame:
    df = pd.read_pickle(BENCHMARKING_SCORES_PKL)
    df['epoch'] = df['epoch'].astype(int)
    return df


def parse_parameter_search_scores() -> pd.DataFrame:
    df = pd.read_pickle(PARAMETR_SERACH_SCORES)
    df['epoch'] = df['epoch'].astype(int)
    return df


def visualize_losses(benchmarking_scores):
    """
    Visualizes the losses for each model grouped by datasets.

    Parameters:
    - benchmarking_scores (DataFrame): the data contained in bm_scores.pkl

    This method creates subplots to display the loss trends for each model across different datasets.
    """
    datasets = np.unique(benchmarking_scores['dataset'])
    models = np.unique(benchmarking_scores['model'])
    _, axes = plt.subplots(len(datasets), 1, figsize=(8, 4 * len(datasets)))
    for dataset_index, dataset in enumerate(datasets):
        for model in models:
            benchmarking_scores_filtered_by_model_and_dataset = benchmarking_scores[(benchmarking_scores['model'] == model) & (benchmarking_scores['dataset'] == dataset)]
            benchmarking_scores_filtered_by_model_and_dataset = filter_first_group(benchmarking_scores_filtered_by_model_and_dataset, "params")
            if benchmarking_scores_filtered_by_model_and_dataset.empty:
                continue
            trainLoss = []
            for _, row in benchmarking_scores_filtered_by_model_and_dataset.sort_values(by='epoch').iterrows():
                if row['trainLoss']:
                    trainLoss.extend(row['trainLoss'])
            if len(trainLoss) > 0:
                axes[dataset_index].plot(trainLoss, label=model)
                axes[dataset_index].set_title(f'Dataset {dataset}')
        axes[dataset_index].legend()
        axes[dataset_index].set_yscale('log')
        axes[dataset_index].set_ylabel('train loss')
        axes[dataset_index].set_xlabel('epoch')
    plt.tight_layout()
    plt.savefig("./plots/losses.png")


def visualize_f1_scores(benchmarking_scores):
    """
    Visualizes the f1 scores for each model grouped by datasets.

    Parameters:
    - benchmarking_scores (DataFrame): the data contained in bm_scores.pkl

    This method creates subplots to display the f1 score trends for each model across different datasets.
    """
    datasets = np.unique(benchmarking_scores['dataset'])
    models = np.unique(benchmarking_scores['model'])
    _, axes = plt.subplots(len(datasets), 1, figsize=(8, 4 * len(datasets)))
    for dataset_index, dataset in enumerate(datasets):
        for model in models:
            benchmarking_scores_filtered_by_model_and_dataset = benchmarking_scores[(benchmarking_scores['model'] == model) & (benchmarking_scores['dataset'] == dataset)]
            benchmarking_scores_filtered_by_model_and_dataset = filter_first_group(benchmarking_scores_filtered_by_model_and_dataset, "params")
            if benchmarking_scores_filtered_by_model_and_dataset.empty:
                continue
            f1_scores = []
            epochs = []
            for _, row in benchmarking_scores_filtered_by_model_and_dataset.sort_values(by='epoch').iterrows():
                f1_scores.append(row['f1'])
                epochs.append(row['epoch'])
            if len(f1_scores) > 1: # keep AllTrue and IsolutionForest but remove AllFalse and Random
                axes[dataset_index].plot(epochs, f1_scores, label=model)
                axes[dataset_index].set_title(f'Dataset {dataset}')
            elif model not in ["AllFalse", "Random"]:
                n = 2000
                axes[dataset_index].plot(list(range(n)), f1_scores * n, label=model)
                axes[dataset_index].set_title(f'Dataset {dataset}')
        axes[dataset_index].legend()
        axes[dataset_index].set_ylabel('f1 score')
        axes[dataset_index].set_xlabel('epoch')
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig("./plots/f1_scores.png")


def visualize_predict_duration(benchmarking_scores):
    """
    Visualizes the duration of the prediction for each model grouped by datasets

    Parameters:
    - benchmarking_scores (DataFrame): the data contained in bm_scores.pkl    
    """
    datasets = np.unique(benchmarking_scores['dataset'])
    models = np.unique(benchmarking_scores['model'])
    models = np.setdiff1d(models, ["AllTrue", "AllFalse", "Random", "NPRandom"])
    _, axes = plt.subplots(len(datasets), 1, figsize=(8, 4 * len(datasets)))
    for dataset_index, dataset in enumerate(datasets):
        model_bars = []
        model_prediction_times = []
        for model in models:
            benchmarking_scores_filtered_by_model_and_dataset = benchmarking_scores[(benchmarking_scores['model'] == model) & (benchmarking_scores['dataset'] == dataset)]
            benchmarking_scores_filtered_by_model_and_dataset = filter_first_group(benchmarking_scores_filtered_by_model_and_dataset, "params")
            if benchmarking_scores_filtered_by_model_and_dataset.empty:
                continue
            predict_duration = benchmarking_scores_filtered_by_model_and_dataset['predictDuration']
            model_bars.append(model)
            model_prediction_times.append(float(sum(td.total_seconds() for td in predict_duration))) # TODO: do we want to sum over all epoch predictions?
        axes[dataset_index].set_title(f'Dataset {dataset}')
        axes[dataset_index].bar(model_bars, model_prediction_times)
        axes[dataset_index].legend()
        axes[dataset_index].set_ylabel('total predict duration over all epochs [s]')
        axes[dataset_index].set_yscale('log')
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig("./plots/predict_durations.png")


def visualize_training_times(benchmarking_scores):
    """
    Visualizes the duration of the training times for each model grouped by datasets

    Parameters:
    - benchmarking_scores (DataFrame): the data contained in bm_scores.pkl    
    """
    datasets = np.unique(benchmarking_scores['dataset'])
    models = np.unique(benchmarking_scores['model'])
    models = [model for model in models if model in ["MTAD_GAT", "TranVAE", "MLSTM", "AnoFormer"]]
    _, axes = plt.subplots(len(models), 1, figsize=(8, 4 * len(models)))
    for dataset_index, dataset in enumerate(datasets):
        for model_index, model in enumerate(models):
            benchmarking_scores_filtered_by_model_and_dataset = benchmarking_scores[(benchmarking_scores['model'] == model) & (benchmarking_scores['dataset'] == dataset)]
            benchmarking_scores_filtered_by_model_and_dataset = filter_first_group(benchmarking_scores_filtered_by_model_and_dataset, "params")
            if benchmarking_scores_filtered_by_model_and_dataset.empty:
                continue
            epochs = []
            total_durations = []
            for _, row in benchmarking_scores_filtered_by_model_and_dataset.sort_values(by='epoch').iterrows():
                total_durations.append(row['totalDuration'].total_seconds())
                epochs.append(row['epoch'])
            if len(total_durations) > 1:
                axes[model_index].plot(epochs, total_durations, label=dataset)
            axes[model_index].set_title(f'Model {model}')
            axes[model_index].legend()
            axes[model_index].set_ylabel('cumulative training time [s]')
            axes[model_index].set_xlabel('epoch')
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig("./plots/training_times.png")


def visualize_lstm_wafer_f1_scores(parameter_search_scores):
    """
    Visualizes the f1 scores for each parameter configurtion for LSTM on dataset WAFER
    and encodes if 2 or 3 hidden layers were used by the color of the bars

    Parameters:
    - parameter_search_scores (DataFrame): the data contained in pm_scores.pkl  
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 7))
    model = "MLSTM"
    dataset = "WAFER"
    parameter_search_scores_filtered_by_model_and_dataset = parameter_search_scores[(parameter_search_scores['model'] == model) & (parameter_search_scores['dataset'] == dataset)]
    current_param_index = 1
    param_labels = {}
    integer_parameter_combinations = []
    parameter_combinations = []
    values_f1 = []
    three_instead_of_two_hidden_layers = []
    only_highest_epoch = parameter_search_scores_filtered_by_model_and_dataset.loc[parameter_search_scores_filtered_by_model_and_dataset.groupby('params')['epoch'].idxmax()]
    fifty_random = only_highest_epoch.sample(n=80)
    fifty_random = fifty_random.sort_values('f1')
    for _, row in fifty_random.iterrows():
        parameter_combinations.append(row['params'])
        values_f1.append(row['f1'])
        three_instead_of_two_hidden_layers.append(ast.literal_eval(row['params'])["number_layers"] == 3)
    for parameter_combination in parameter_combinations:
        integer_parameter_combinations.append(current_param_index)
        param_labels[current_param_index] = parameter_combination
        current_param_index += 1
    for _, (label, value, color_bool) in enumerate(zip(integer_parameter_combinations, values_f1, three_instead_of_two_hidden_layers)):
        color = 'orange' if color_bool else 'blue'
        axes[0].bar(label, value, color=color)
    axes[0].set_title(f'Model {model} on dataset {dataset}')
    axes[0].legend()
    axes[0].set_ylabel('f1_score')
    plt.suptitle("f1 scores for 80 random params")
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    text_str = '\n'.join([f'{key}: {value}' for key, value in list(param_labels.items())])
    axes[1].text(-0.1, 0.1, text_str, fontsize=4.5)
    axes[1].axis('off')
    plt.savefig("./plots/lstm_wafer_f1_scores.png")


def visualize_parameter_combinations(parameter_search_scores):
    """
    Visualizes the adjusted/not adjusted f1 scores for each parameter combination grouped by datasets and algorithms.
    The parameter combinations are given as numbers and are displayed in a legend beneath.
    Each parameter combination from the param parameter_search_scores is displayed in the plot.

    Parameters:
    - parameter_search_scores (DataFrame): the data contained in pm_scores.pkl   
    """
    datasets = np.unique(parameter_search_scores['dataset'])
    models = np.unique(parameter_search_scores['model'])
    models = [model for model in models if model in ["MTAD_GAT", "TranVAE", "MLSTM", "AnoFormer"]]
    nrows = len(datasets)
    ncols = len(models)
    figsize = (ncols * 6, nrows * 6)
    param_labels = {}
    current_param_index = 1
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    for dataset_index, dataset in enumerate(datasets):
        for model_index, model in enumerate(models):
            parameter_search_scores_filtered_by_model_and_dataset = parameter_search_scores[(parameter_search_scores['model'] == model) & (parameter_search_scores['dataset'] == dataset)]
            parameter_combinations = []
            values_f1 = []
            values_paf1 = []
            for _, row in parameter_search_scores_filtered_by_model_and_dataset.loc[parameter_search_scores_filtered_by_model_and_dataset.groupby('params')['epoch'].idxmax()].iterrows():
                parameter_combinations.append(row['params'])
                values_f1.append(row['f1'])
                values_paf1.append(row['paf1'])
            if len(parameter_combinations) > 0:
                integer_parameter_combinations = []
                for parameter_combination in parameter_combinations:
                    integer_parameter_combinations.append(current_param_index)
                    param_labels[current_param_index] = parameter_combination
                    current_param_index += 1
                axes[dataset_index][model_index].bar(integer_parameter_combinations, values_f1)
                axes[dataset_index][model_index].bar(integer_parameter_combinations, values_paf1, bottom=values_f1)
            axes[dataset_index][model_index].set_xlabel(f'Model {model}')
            axes[dataset_index][model_index].set_ylabel(f'Dataset {dataset}')

    plt.suptitle("f1/paf1 scores for different parameter combinations")
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    text_str = '\n'.join([f'{key}: {value}' for key, value in list(param_labels.items())[:60]]) # TODO: not just the first 60
    plt.subplots_adjust(bottom=0.3)
    plt.gcf().text(0.5, 0.01, text_str, ha='center')
    plt.savefig("./plots/f1_paf1_scores_parameter_combinations.png")


def visualize_labels(true_labels, predicted_labels, title="Comparison between predicted labels vs true labels"):
    _, ax = plt.subplots()
    true_labels = list(map(lambda x: 1 if x else 0, true_labels))
    predicted_labels = list(map(lambda x: 1 if x else 0, predicted_labels))
    x = range(1, len(true_labels) + 1)
    ax.step(x, true_labels, label="true label", alpha=0.75)
    ax.step(x, predicted_labels, label="predicted label", alpha=0.75)
    # add color highlighting
    for i in range(len(true_labels)):
        if predicted_labels[i] == true_labels[i]:
            ax.axvspan(i - 0.5, i + 0.5, facecolor='green', alpha=0.3)
        else:
            ax.axvspan(i - 0.5, i + 0.5, facecolor='red', alpha=0.3)
    ax.set_xlabel('timestep')
    ax.set_ylabel('label')
    ax.set_title(title)
    plt.yticks([0, 1])
    ax.legend()
    plt.savefig("./plots/label_comparison.png")


def main():
    benchmarking_scores = parse_benchmarking_scores()
    parameter_search_scores = parse_parameter_search_scores()
    visualize_losses(benchmarking_scores)
    visualize_f1_scores(benchmarking_scores)
    
    # get one random timeseries for labels from dataset
    random_score = benchmarking_scores.iloc[100]
    true_labels = random_score['labels']
    predicted_labels = random_score['prediction']

    visualize_labels(true_labels, predicted_labels)
    visualize_predict_duration(benchmarking_scores)
    visualize_training_times(benchmarking_scores)

    visualize_parameter_combinations(parameter_search_scores)

    visualize_lstm_wafer_f1_scores(parameter_search_scores)

if __name__ == "__main__":
    main()