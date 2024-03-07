from keras.models import Sequential
from sklearn.model_selection import KFold
from concurrent.futures import ThreadPoolExecutor
import threading

from .lib.apply_noise import apply_noise
from .lib.metrics import compute_metrics
from .lib.train_model import train_model
from .lib.consts import NOISE_LEVELS, NIGEP_AVAILABLE_KWARGS
from .classes.results_writer import ResultsWriter
from .lib.functions import validate_kwargs, write_model


class NigepOOD:

    def __init__(self, **kwargs):
        self.lock = threading.Lock()
        """
        Initialize Nigep instance.

        Parameters:
        - execution_name (str): Name of the execution.
        - model (Sequential): Keras Sequential model.
        - batch_size (int): Batch size for training.
        - input_shape (tuple[int, int]): Input shape of the data.
        - x_data (list[any]): Input data.
        - y_data (list[any]): Target data.
        - target_names (list[str], optional): Names of target classes.
        - class_mode (str, optional): Classification mode (default: 'categorical').
        - k_fold_n (int, optional): Number of folds in k-fold cross-validation (default: 5).
        - epochs (int, optional): Number of training epochs (default: 10).
        - callbacks (list[any], optional): List of callbacks for model training.
        - noise_levels (any, optional): Noise levels for data augmentation (default: NOISE_LEVELS).
        - save_models (bool, optional): Save trained models (default: False).
        - evaluate_models (bool, optional): Evaluate models during testing (default: False).
        - kfold_random_state (int, optional): K-Fold random state.
        """
        # validate_kwargs(kwargs=kwargs, allowed_kwargs=NIGEP_AVAILABLE_KWARGS)
        self.execution_name: str = kwargs['execution_name']
        self.model: Sequential = kwargs['model']
        self.batch_size: int = kwargs['batch_size']
        self.input_shape: tuple[int, int] = kwargs['input_shape']

        self.x_data: list[any] = kwargs['x_data']
        self.y_data: list[any] = kwargs['y_data']
        self.ood_x_data: list[any] = kwargs['y_data']
        self.ood_y_data: list[any] = kwargs['y_data']

        self.target_names: list[str] = kwargs.get('target_names', None)
        self.class_mode: str = kwargs.get('class_mode', 'categorical')
        self.epochs: int = kwargs.get('epochs', 10)
        self.callbacks: list[any] = kwargs.get('callbacks', [])
        self.noise_levels: any = kwargs.get('noise_levels', NOISE_LEVELS)
        self.save_models: bool = kwargs.get('save_models', False)
        self.evaluate_models: bool = kwargs.get('evaluate_models', False)
        self.rw = ResultsWriter(self.execution_name)

    def __train_and_write_model(self, results_folder, train_data, train_noise):
        print(f'Training with Noise: {str(train_noise)}')

        with self.lock:
            train_model(self.model, self.epochs, self.callbacks, train_data)
            write_model(results_folder, self.save_models, self.model, train_noise)

    def __out_of_distribution_evaluation(self, results_folder, test_noise, train_noise):
        print(f'Out of Distribution Evaluation: {str(train_noise)} - Test Noise: {str(test_noise)}')

        x_test, y_test = apply_noise(self.ood_x_data, self.ood_y_data, test_noise)

        if self.evaluate_models:
            self.model.evaluate(x_test, y_test)

        cm, cr = compute_metrics(self.model, self.class_mode, self.target_names, x_test, y_test)
        self.rw.write_new_metrics(results_folder, train_noise, test_noise, cr, cm, self.target_names)

    def __execute(self, noise_level):
        results_folder = self.rw.write_k_subset_folder(1)

        noised_data = apply_noise(self.x_data, self.y_data, noise_level)

        self.__train_and_write_model(results_folder, noised_data, noise_level)

        self.__out_of_distribution_evaluation(results_folder, noise_level)

    def execute(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(
                self.__execute, noise_level)
                for noise_level
                in self.noise_levels
            ]

            for future in futures:
                future.result()

        self.rw.save_mean_merged_results()
        self.rw.save_heatmap_csv()

    def plot_and_save_generalization_profile(self):
        self.rw.plot_and_save_heatmap_png()
