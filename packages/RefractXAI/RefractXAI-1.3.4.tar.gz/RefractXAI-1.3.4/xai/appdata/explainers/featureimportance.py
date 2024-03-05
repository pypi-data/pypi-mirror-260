from .base import ModelInterpreter
from ..constants import Log
import numpy as np
from ..logging import build_logger
from constants import ProblemType

logger = build_logger(Log.logger_level, "fi")


class FeatureImportance(ModelInterpreter):
    """
        This class is used to generate feature importance for a model.

        Args:
            model: The model to be explained.
            x_train: The training data.
            y_train: The training labels.
            feature_names: The names of the features to be explained.
            target_names: The names of the targets to be explained.
            mode: The mode of the explainer ( Classifcation / Regression ).
            predict_fn: The prediction function of the model.

        Returns:
            object: The feature importance object.
    """

    def __init__(self, interpreter):
        super().__init__(interpreter)

    def generate_data(self):
        """
            Generates the data for the feature importance.

            Returns:
                list: A list of dictionaries containing the feature importance data.

        """

        if self.mode == ProblemType.REGRESSION :
            instanceShaps = self.shap_data[0] 
            sortedIdx = np.argsort(np.sum(np.abs(instanceShaps),axis=0))
            sortedShaps = instanceShaps[:,sortedIdx]
            sortedFeatureNames = np.array(self.feature_names)[sortedIdx].tolist()
            sortedWeights = np.sum(np.abs(sortedShaps),axis=0).tolist()
            sortedWeights = self.generated_fi_percentages(sortedWeights)
            sortedWeights = [round(x,3) for x in sortedWeights]
            dictWeights = dict(zip(sortedFeatureNames,sortedWeights))

            return {
                "model_target_info" :{"target_name" : self.target_names[0]},
                "predictions":sortedWeights
            }
        else:
            shap_values= self.shap_data[0]
            dictWeights = {}
            for i in range(len(shap_values)):
                instanceShaps = shap_values[i]
                #sorting weights
                sortedIdx = np.argsort(np.sum(np.abs(instanceShaps),axis=0))
                sortedShaps = instanceShaps[:,sortedIdx]
                sortedFeatureNames = np.array(self.feature_names)[sortedIdx].tolist()
                sortedWeights = np.sum(np.abs(sortedShaps),axis=0).tolist()
                sortedWeights = self.generated_fi_percentages(sortedWeights)
                sortedWeights = [round(x,3) for x in sortedWeights]
                className = self.process_obj["labelInfo"][f"{i}"]
                dictWeights[className] = dict(zip(sortedFeatureNames,sortedWeights))
            dictWeights["model_target_info"] = {"target_name" : self.target_names[0]}
                
            return dictWeights
        
    def generated_fi_percentages(self,data):
        maximum = sum(data)
        updated_values = [(x/maximum)*100 for x in data]
        return updated_values
