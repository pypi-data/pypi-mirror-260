from .base import ModelInterpreter
from tqdm.auto import tqdm
from sklearn.inspection import PartialDependenceDisplay
from ..constants import Log
from ..logging import build_logger
from constants import ProblemType

logger = build_logger(Log.logger_level, "pdp")


class PartialDependencePlot(ModelInterpreter):
    """
        This class is used to generate partial dependence plots for a model.

        Args:
            model: The model to be explained.
            x_train: The training data.
            y_train: The training labels.
            feature_names: The names of the features to be explained.
            target_names: The names of the targets to be explained.
            mode: The mode of the explainer ( Classifcation / Regression ).
            predict_fn: The prediction function of the model.

        Returns:
            object: A partial dependence plot object.
    """

    def __init__(self, interpreter):
        super().__init__(interpreter)

        self.target_pdp_names = self.target_names
        if not self.mode == ProblemType.REGRESSION:
            self.target_names = self.unique_values

    def generate_data(self):
        """
            Generates the data for the partial dependence for the feature ids provided

            Returns:
                list: A list of json values for partial dependence plots.

        """

        dict_list = []
        binaryMode = 'false' if len(self.target_names) >2 else 'true'
        feature_maps = {feat:i for i,feat in enumerate(self.feature_names) }

        if self.mode == ProblemType.REGRESSION:
            for feat in tqdm(self.feature_ids):
                pdp_data = PartialDependenceDisplay.from_estimator(
                        self.model,
                        self.x_train,
                        features=[feature_maps[feat]]
                    )
                
                dict_list.append({
                    "feature_name" : feat,
                    "feature_data" : pdp_data.pd_results[0]['values'][0].tolist(),
                    "pdp_values" : pdp_data.pd_results[0].average[0].tolist(),
                    "regressionMode": "true"
                })

            return dict_list, self.target_names,self.mode
        else:
            for feat in tqdm(self.feature_ids):
                yax = {}
                temp_target_names = []
                pdp_data =  PartialDependenceDisplay.from_estimator(
                    self.model,
                    self.x_train,
                    features=[feature_maps[feat]],
                    target=[1]
                    )
                
                if len(self.target_names) > 2:
                    for j in range(len(self.target_names)):
                        temp = {self.process_obj['labelInfo'][f'{self.target_names[j]}']: pdp_data.pd_results[0].average[j].tolist() }
                        temp_target_names.append(self.process_obj['labelInfo'][f'{self.target_names[j]}'])
                        yax.update(temp)
                else:
                    temp = {self.process_obj['labelInfo']['1']: pdp_data.pd_results[0].average[0].tolist() }
                    temp_target_names.append(self.process_obj['labelInfo']['1'])
                    yax.update(temp)


                dict_list.append({
                    "feature_name" : feat,
                    "feature_data" : pdp_data.pd_results[0]['values'][0].tolist(),
                    "pdp_values" : yax,
                    "binaryMode": binaryMode
                })
            return dict_list,temp_target_names,self.mode