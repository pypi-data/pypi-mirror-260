
import os
from utilities import ModelArtifacts,XAIHTML
import os,json
import numpy as np
from appdata.html_content import *
from appdata import ModelExplainer
from constants import ProblemType
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris,load_breast_cancer,load_diabetes

# model_type = "Binary Classification"
# model_type = "Multiclass Classification"
# model_type = "Regression"


data = load_diabetes()
model_type = "Regression"
os.environ['drift_type'] = "model_explanations"
process_obj ={"labelInfo" :{'0':'0',
                            '1':'1',
                            # '2':'2'
                            },
              "featureInfo" : {}
            }

x_train,x_test,y_train,y_test = train_test_split(data.data,data.target)
model_flavour = "sklearn"
os.environ['problem_type'] = model_type
feature_names = data.feature_names
# target_names = data.target_names
target_names = ["Target"]

class_mapping = None
os.environ['output_path'] = os.getcwd()

# os.environ['target_class_names'] = ",".join(data.target_names.tolist())
# classe_names = os.getenv("target_class_names").strip().split(",")
# class_mapping = {str(index):value for index,value in enumerate(classe_names)}


model = RandomForestRegressor()
# model = RandomForestClassifier()
model.fit(x_train,y_train)

output_path = os.getenv("output_path")

## XAI Base HTML
html_obj = XAIHTML(output_path,target_class_names=class_mapping)

train_table = x_train
test_table = x_test
train_target = y_train
test_target = y_test


row_count = 100 if test_table.shape[0] > 100 else test_table.shape[0]

train_table = train_table if type(train_table) == np.ndarray else train_table.to_numpy()
train_target = train_target if type(train_target) == np.ndarray else train_target.to_numpy()
test_table = test_table if type(test_table) == np.ndarray else test_table.to_numpy()
test_target = test_target if type(test_target) == np.ndarray else test_target.to_numpy()
        
#sample rows for lime
insert_random_rows_lime, indexs = insert_random_dataindexes(row_count,"lime")

explainer = ModelExplainer(
        model=model,
        x_train=train_table,
        y_train=train_target,
        x_test=test_table,
        y_test=test_target,
        sample_rows=indexs,
        feature_names=feature_names,
        target_names=target_names,
        process_obj=process_obj,
        mode=model_type,
        feature_ids=None,
        preprocessing=None,
        sample_req=indexs,
        predict_fn=None,
        shap_data=None
)

# Feature Importance
fi_data = explainer.fi.generate_data()
multi_class_labels = load_multi_class_names(fi_data)
html_feature_importance = get_html_feature_importance(fi_data)
print("Completed Feature Importance")

# Model Overview
get_model_stats = explainer.ml_overview.generate_data()
multi_class_labelsroc = load_multi_class_names_for_roc(get_model_stats) if not model_type==ProblemType.REGRESSION else None
model_overview_html_script  = get_model_overview_html(get_model_stats,model_type)
print("Completed Model Overview")

# LimePlots
lime_data = explainer.lf.generate_data()
insert_multi_class_labels_lime,classnames = insert_class_labels_lime(lime_data)
lime_plot_data = get_lime_html(lime_data,classnames)
print("Completed LimePlots")

# PDP
pdp_data,target_labels,mode = explainer.pdp.generate_data()
pdp_features_names,htmlClassLabels = insert_pdp_dropdown_list(feature_names,target_labels,mode)
pdp_plot_data = get_pdp_html(pdp_data)
print("Completed PDP")

#Decision_plots
dplot_data = explainer.dplot.generate_data()
insert_dplot_rows,dplot_classes = insert_dplot_rows_class_info(dplot_data)
dplot_explainer_html = insert_dplot_plot(dplot_data)
print("Completed Decision Plots")

html_params_list = [
("feature_importance",html_feature_importance),
("multi_class_labels",multi_class_labels),
("multi_class_labelsroc",multi_class_labelsroc),
("model_overview_html_script",model_overview_html_script),
("insert_random_rows_lime",insert_random_rows_lime),
("insert_multi_class_labels_lime",insert_multi_class_labels_lime),
("lime_plot_data",lime_plot_data),
("pdp_features_names",pdp_features_names),
("htmlClassLabelsPDP",htmlClassLabels),
("pdp_plot_data",pdp_plot_data),
("insert_dplot_rows",insert_dplot_rows),
("insert_dplot_classes",dplot_classes),
("dplot_explainer_html",dplot_explainer_html)
]


json_params_list = [
                ("feature_importance",fi_data),
                ("model_stats",{key:value for key,value in get_model_stats.items() if not key=="confusion_matrix_ui"}),
                ("lime_data",lime_data),
                ("partial_dependence_plot_data",pdp_data),
                ("decision_plot_data",dplot_data)
]



html_obj.load_html(**dict(html_params_list))

# html_obj.save_json_file(**dict(json_params_list))



