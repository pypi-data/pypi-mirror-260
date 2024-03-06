def get_results_columns(target_names):
    classes_precision_columns = []
    classes_recall_columns = []
    classes_f1score_columns = []
    for index, item in enumerate(target_names):
        classes_precision_columns.append(f'precision({item})')
        classes_recall_columns.append(f'recall({item})')
        classes_f1score_columns.append(f'f1-score({item})')

    return [
        'train-dataset-noise', 'test-dataset-noise',
        *classes_precision_columns,
        'precision(macro-avg)', 'precision(weighted-avg)',
        *classes_recall_columns,
        'recall(macro-avg)',  'recall(weighted-avg)',
        *classes_f1score_columns,
        'f1-score(accuracy)', 'f1-score(macro-avg)', 'f1-score(weighted-avg)'
    ]


def validate_kwargs(
    kwargs, allowed_kwargs, error_message="Keyword argument not understood:"
):
    """Checks that all keyword arguments are in the set of allowed keys."""
    for kwarg in kwargs:
        if kwarg not in allowed_kwargs:
            raise TypeError(error_message, kwarg)