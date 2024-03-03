"""Evaluation utils for unsupervised graph learning tasks.
"""

# pylint: disable=invalid-name,too-many-locals
import os
import random
from typing import Dict
from typing import List
from typing import Tuple

import numpy as np
import torch
from munkres import Munkres
from six.moves import cPickle as pickle
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score as ACC
from sklearn.metrics import adjusted_mutual_info_score as AMI
from sklearn.metrics import adjusted_rand_score as ARI
from sklearn.metrics import f1_score as F1
from sklearn.metrics import normalized_mutual_info_score as NMI
from sklearn.svm import LinearSVC

from ..common import tab_printer


def load_dict(filename_):
    with open(filename_, "rb") as f:
        ret_di = pickle.load(f)
    return ret_di


def save_dict(di_, filename_):
    # Get the directory path from the filename
    dir_path = os.path.dirname(filename_)

    # Create the directory if it does not exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(filename_, "wb") as f:
        pickle.dump(di_, f)


def split_train_test_nodes(
    num_nodes,
    train_ratio,
    valid_ratio,
    data_name,
    split_id=0,
    fixed_split=True,
):
    if fixed_split:
        file_path = f"../input/fixed_splits/{data_name}-{train_ratio}-{valid_ratio}-splits.npy"
        if not os.path.exists(file_path):
            print("There is no generated fixed splits")
            print("Generating fixed splits...")
            splits = {}
            for idx in range(10):
                # set up train val and test
                shuffle = list(range(num_nodes))
                random.shuffle(shuffle)
                train_nodes = shuffle[:int(num_nodes * train_ratio / 100)]
                val_nodes = shuffle[int(num_nodes * train_ratio /
                                        100):int(num_nodes * (train_ratio + valid_ratio) / 100)]
                test_nodes = shuffle[int(num_nodes * (train_ratio + valid_ratio) / 100):]
                splits[idx] = {"train": train_nodes, "valid": val_nodes, "test": test_nodes}
            save_dict(di_=splits, filename_=file_path)
        else:
            splits = load_dict(filename_=file_path)
        split = splits[split_id]
        train_nodes, val_nodes, test_nodes = split["train"], split["valid"], split["test"]
    else:
        # set up train val and test
        shuffle = list(range(num_nodes))
        random.shuffle(shuffle)
        train_nodes = shuffle[:int(num_nodes * train_ratio / 100)]
        val_nodes = shuffle[int(num_nodes * train_ratio /
                                100):int(num_nodes * (train_ratio + valid_ratio) / 100)]
        test_nodes = shuffle[int(num_nodes * (train_ratio + valid_ratio) / 100):]

    return np.array(train_nodes), np.array(val_nodes), np.array(test_nodes)


def cluster_eval(y_true, y_pred):
    """code source: https://github.com/bdy9527/SDCN"""
    y_true = y_true.detach().cpu().numpy() if isinstance(y_true, torch.Tensor) else y_true
    y_pred = y_pred.detach().cpu().numpy() if isinstance(y_pred, torch.Tensor) else y_pred

    l1 = list(set(y_true))
    numclass1 = len(l1)
    l2 = list(set(y_pred))
    numclass2 = len(l2)

    # NOTE: force to assign a random node into a missing class
    # fill out missing classes
    ind = 0
    if numclass1 != numclass2:
        for i in l1:
            if i in l2:
                pass
            else:
                y_pred[ind] = i
                ind += 1

    l2 = list(set(y_pred))
    numclass2 = len(l2)

    cost = np.zeros((numclass1, numclass2), dtype=int)
    for i, c1 in enumerate(l1):
        mps = [i1 for i1, e1 in enumerate(y_true) if e1 == c1]
        for j, c2 in enumerate(l2):
            mps_d = [i1 for i1 in mps if y_pred[i1] == c2]
            cost[i][j] = len(mps_d)

    # match two clustering results by Munkres algorithm
    m = Munkres()
    cost = (-cost).tolist()
    indexes = m.compute(cost)

    # get the match results
    new_predict = np.zeros(len(y_pred))
    for i, c in enumerate(l1):
        # correponding label in l2:
        c2 = l2[indexes[i][1]]

        # ai is the index with label==c2 in the pred_label list
        ai = [ind for ind, elm in enumerate(y_pred) if elm == c2]
        new_predict[ai] = c

    return (
        ACC(y_true, new_predict),
        NMI(y_true, new_predict, average_method="arithmetic"),
        AMI(y_true, new_predict, average_method="arithmetic"),
        ARI(y_true, new_predict),
        F1(y_true, new_predict, average="macro"),
    )


def kmeans_test(X, y, n_clusters, repeat=10):
    y = y.detach().cpu().numpy() if isinstance(y, torch.Tensor) else y
    X = X.detach().cpu().numpy() if isinstance(X, torch.Tensor) else X

    acc_list = []
    nmi_list = []
    ami_list = []
    ari_list = []
    f1_list = []
    for _ in range(repeat):
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
        y_pred = kmeans.fit_predict(X)
        (
            acc_score,
            nmi_score,
            ami_score,
            ari_score,
            macro_f1,
        ) = cluster_eval(
            y_true=y,
            y_pred=y_pred,
        )
        acc_list.append(acc_score)
        nmi_list.append(nmi_score)
        ami_list.append(ami_score)
        ari_list.append(ari_score)
        f1_list.append(macro_f1)
    return (
        np.mean(acc_list),
        np.std(acc_list),
        np.mean(nmi_list),
        np.std(nmi_list),
        np.mean(ami_list),
        np.std(ami_list),
        np.mean(ari_list),
        np.std(ari_list),
        np.mean(f1_list),
        np.std(f1_list),
    )


def svm_test(num_nodes, data_name, embeddings, labels, train_ratios=(10, 20, 30, 40), repeat=10):
    result_macro_f1_list = []
    result_micro_f1_list = []
    for train_ratio in train_ratios:
        macro_f1_list = []
        micro_f1_list = []
        for i in range(repeat):
            train_idx, val_idx, test_idx = split_train_test_nodes(
                num_nodes=num_nodes,
                train_ratio=train_ratio,
                valid_ratio=train_ratio,
                data_name=data_name,
                split_id=i,
            )
            X_train, X_test = embeddings[np.concatenate([train_idx, val_idx])], embeddings[test_idx]
            y_train, y_test = labels[np.concatenate([train_idx, val_idx])], labels[test_idx]
            svm = LinearSVC(dual=False)
            svm.fit(X_train, y_train)
            y_pred = svm.predict(X_test)
            macro_f1 = F1(y_test, y_pred, average="macro")
            micro_f1 = F1(y_test, y_pred, average="micro")
            macro_f1_list.append(macro_f1)
            micro_f1_list.append(micro_f1)
        result_macro_f1_list.append((np.mean(macro_f1_list), np.std(macro_f1_list)))
        result_micro_f1_list.append((np.mean(micro_f1_list), np.std(micro_f1_list)))
    return result_macro_f1_list, result_micro_f1_list


def evaluate_clf_cls(
    labels: np.ndarray,
    num_classes: int,
    num_nodes: int,
    data_name: str,
    embeddings: torch.Tensor,
    quiet: bool = True,
    method: str = "both",
) -> Tuple[List[Tuple[float]], float]:
    """Evaluation of node classification (linear regression) and clustering.

    Args:
        labels (np.ndarray): Labels.
        num_classes (int): Num of classes.
        num_nodes (int): Num of nodes.
        data_name (str): Dataset name.
        embeddings (torch.Tensor): Node embedding matrix.
        quiet (bool, optional): Whether to print info. Defaults to True.
        method (bool, optional): method for evaluation, \
            "clf" for linear regression (node classification), \
                "cls" for node clustering, "both" for both. Defaults to "both".

    Returns:
        Tuple[List[Tuple[float]], float]: [svm_macro_f1_list, svm_micro_f1_list, \
            acc_mean, acc_std, nmi_mean, nmi_std, ami_mean, ami_std, ari_mean,ari_std, \
                f1_mean, f1_std]
    """

    acc_mean = acc_std = nmi_mean = nmi_std = ari_mean = ari_std = f1_mean = f1_std = 0
    svm_macro_f1_list = svm_micro_f1_list = [(0, 0), (0, 0), (0, 0), (0, 0)]

    if method in ("both", "clf"):
        (
            svm_macro_f1_list,
            svm_micro_f1_list,
        ) = svm_test(
            num_nodes=num_nodes,
            data_name=data_name,
            embeddings=embeddings,
            labels=labels,
        )
        if not quiet:
            print("SVM test for linear regression:")
            maf1 = [
                f"{macro_f1_mean * 100:.2f}±{macro_f1_std * 100:.2f} ({train_size:.1f})" for (
                    macro_f1_mean,
                    macro_f1_std,
                ), train_size in zip(svm_macro_f1_list, [10, 20, 30, 40])
            ]
            mif1 = [
                f"{micro_f1_mean * 100:.2f}±{micro_f1_std * 100:.2f} ({train_size:.1f})" for (
                    micro_f1_mean,
                    micro_f1_std,
                ), train_size in zip(svm_micro_f1_list, [10, 20, 30, 40])
            ]
            tab_printer(
                {
                    "Macro F1": "\n".join(maf1),
                    "Micro F1": "\n".join(mif1),
                },
                sort=False,
            )

    if method in ("both", "cls"):
        (
            acc_mean,
            acc_std,
            nmi_mean,
            nmi_std,
            ami_mean,
            ami_std,
            ari_mean,
            ari_std,
            f1_mean,
            f1_std,
        ) = kmeans_test(
            embeddings,
            labels,
            num_classes,
        )
        if not quiet:
            print("K-means test for node clustering:")
            tab_printer(
                {
                    "ACC": f"{acc_mean * 100:.2f}±{acc_std * 100:.2f}",
                    "NMI": f"{nmi_mean * 100:.2f}±{nmi_std * 100:.2f}",
                    "AMI": f"{ami_mean * 100:.2f}±{ami_std * 100:.2f}",
                    "ARI": f"{ari_mean * 100:.2f}±{ari_std * 100:.2f}",
                    "Macro F1": f"{f1_mean * 100:.2f}±{f1_std * 100:.2f}",
                },
                sort=False,
            )

    return (
        svm_macro_f1_list,
        svm_micro_f1_list,
        acc_mean,
        acc_std,
        nmi_mean,
        nmi_std,
        ami_mean,
        ami_std,
        ari_mean,
        ari_std,
        f1_mean,
        f1_std,
    )


def evaluate_from_embeddings(
    labels: np.ndarray,
    num_classes: int,
    num_nodes: int,
    data_name: str,
    embeddings: torch.Tensor,
    quiet: bool = True,
    method: str = "both",
) -> Tuple[Dict, Dict]:
    """evaluate embeddings with LR and Clustering.

    Args:
        labels (np.ndarray): labels.
        num_classes (int): number of classes.
        num_nodes (int): number of nodes.
        data_name (str): name of the datasets.
        embeddings (torch.Tensor): embeddings.
        quiet (bool, optional): whether to print info. Defaults to True.
        method (bool, optional): method for evaluation, \
            "clf" for linear regression (node classification), \
                "cls" for node clustering, "both" for both. Defaults to "both".

    Returns:
        Tuple[Dict, Dict]: (clustering_results, classification_results)
    """
    # Call the evaluate_results_nc function with the loaded embeddings
    (
        svm_macro_f1_list,
        svm_micro_f1_list,
        acc_mean,
        acc_std,
        nmi_mean,
        nmi_std,
        ami_mean,
        ami_std,
        ari_mean,
        ari_std,
        f1_mean,
        f1_std,
    ) = evaluate_clf_cls(
        labels,
        num_classes,
        num_nodes,
        data_name,
        embeddings,
        quiet=quiet,
        method=method,
    )

    # Format the output as desired
    clustering_results = {
        "ACC": f"{acc_mean * 100:.2f}±{acc_std * 100:.2f}",
        "NMI": f"{nmi_mean * 100:.2f}±{nmi_std * 100:.2f}",
        "AMI": f"{ami_mean * 100:.2f}±{ami_std * 100:.2f}",
        "ARI": f"{ari_mean * 100:.2f}±{ari_std * 100:.2f}",
        "MaF1": f"{f1_mean * 100:.2f}±{f1_std * 100:.2f}",
    }

    svm_macro_f1_list = [f"{res[0] * 100:.2f}±{res[1] * 100:.2f}" for res in svm_macro_f1_list]
    svm_micro_f1_list = [f"{res[0] * 100:.2f}±{res[1] * 100:.2f}" for res in svm_micro_f1_list]

    classification_results = {}
    for i, percent in enumerate(["10%", "20%", "30%", "40%"]):
        classification_results[f"{percent}_MaF1"] = svm_macro_f1_list[i]
        classification_results[f"{percent}_MiF1"] = svm_micro_f1_list[i]

    return clustering_results, classification_results
