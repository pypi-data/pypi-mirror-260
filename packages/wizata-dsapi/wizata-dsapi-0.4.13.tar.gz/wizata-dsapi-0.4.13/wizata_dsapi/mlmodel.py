import json
import uuid
from .api_dto import ApiDto
from enum import Enum


def get_bool(obj, name: str):
    if isinstance(obj[name], str) and obj[name].lower() == "false":
        return False
    else:
        return bool(obj[name])


class MLModelConfig(ApiDto):
    """
    a model config defines execution properties for a specific model.
    usually to define how a pipeline should train and predict your model.

    :ivar train_script: name of function referencing the script to train the model.
    :ivar train_test_split_pct: percentage repartition to split the data for training and scoring.
    :ivar target_feat: target feature name if existing.
    :ivar features: filter list of datapoint columns if necessary.
    :ivar train_test_split_type: name of function referencing the script to train the model.
    :ivar model_key: key of the model to store (or use story property if dynamic).
    :ivar output_property: name of dataframe column where to store results (or template property).
    """

    def __init__(self,
                 train_script=None,
                 train_test_split_pct: float = 1.0,
                 train_test_split_type: str = "ignore",
                 function: str = "predict",
                 target_feat: str = None,
                 output_property: str = "result",
                 features: list = None,
                 model_key: str = None,
                 model_type: str = None,
                 model_alias: str = None,
                 by_twin: bool = False,
                 by_property: bool = False,
                 property_name: str = None,
                 source: str = "wizata"
                 ):

        # training
        self.train_script = train_script
        self.train_test_split_pct = train_test_split_pct
        self.train_test_split_type = train_test_split_type
        self.function = function

        # features management
        self.target_feat = target_feat
        self.features = features
        self.output_property = output_property

        # key and identification
        self.model_key = model_key
        self.by_twin = by_twin
        self.by_property = by_property
        self.property_name = property_name

        # source
        self.source = source
        self.model_type = model_type
        self.model_alias = model_alias

    def from_json(self, obj):

        # blocking old configs
        if "store_property" in obj.keys():
            raise ValueError("deprecated and unsupported configuration 'store_property'")
        if "model_key_type" in obj.keys():
            raise ValueError("deprecated and unsupported configuration 'model_key_type'")

        # training info
        if "train_script" in obj.keys() and obj["train_script"] is not None:
            self.train_script = obj["train_script"]
        if "train_test_split_pct" in obj.keys() and obj["train_test_split_pct"] is not None:
            self.train_test_split_pct = float(obj["train_test_split_pct"])
        if "train_test_split_type" in obj.keys() and obj["train_test_split_type"] is not None:
            self.train_test_split_type = obj["train_test_split_type"]
        if "function" in obj.keys() and obj["function"] is not None:
            self.function = obj["function"]

        # features info
        if "target_feat" in obj.keys() and obj["target_feat"] is not None:
            self.target_feat = obj["target_feat"]
        if "features" in obj.keys() and obj["features"] is not None:
            self.features = obj["features"]
        if "output_property" in obj.keys() and obj["output_property"] is not None:
            self.output_property = obj["output_property"]

        # source
        if "source" in obj.keys() and obj["source"] is not None:
            self.source = obj["source"]
            if self.source not in ["wizata", "mlflow"]:
                raise ValueError("source must be wizata or mlflow")

        # key and target
        if "model_key" not in obj.keys() or obj["model_key"] is None:
            raise KeyError('model_key must be declared in the config.')
        self.model_key = obj["model_key"]
        if "by_twin" in obj.keys():
            self.by_twin = get_bool(obj, name="by_twin")
        if "by_property" in obj.keys():
            self.by_property = get_bool(obj, name="by_property")
        if "property_name" in obj.keys() and obj["property_name"] is not None:
            self.property_name = obj["property_name"]
        if "model_type" in obj.keys() and obj["model_type"] is not None:
            self.model_type = obj["model_type"]
        if "model_alias" in obj.keys() and obj["model_alias"] is not None:
            self.model_type = obj["model_alias"]

    def to_json(self, target: str = None):
        obj = {
            "source": self.source
        }

        # training info
        if self.train_script is not None:
            obj["train_script"] = str(self.train_script)
        if self.train_test_split_pct is not None:
            obj["train_test_split_pct"] = float(self.train_test_split_pct)
        if self.train_test_split_type is not None:
            obj["train_test_split_type"] = str(self.train_test_split_type)
        if self.features is not None:
            obj["features"] = self.features

        # features info
        if self.target_feat is not None:
            obj["target_feat"] = str(self.target_feat)
        if self.output_property is not None:
            obj["output_property"] = self.output_property
        if self.function is not None:
            obj["function"] = self.function

        # key and target
        if self.model_key is not None:
            obj["model_key"] = self.model_key
        if self.model_type is not None:
            obj["model_type"] = self.model_type
        if self.model_alias is not None:
            obj["model_alias"] = self.model_alias
        if self.by_twin is not None:
            obj["by_twin"] = str(self.by_twin)
        if self.by_property is not None:
            obj["by_property"] = str(self.by_property)
        if self.property_name is not None:
            obj["property_name"] = self.property_name

        return obj


class MLModel(ApiDto):
    """
    A trained Machine Learning Model stored to be executed on demand.
    Can contain also a scaler, both object are stored as pickled file.

    :ivar model_id: The UUID of the ML Model.
    :ivar key: Logical String ID of the Model
    :ivar generatedById: The UUID of the Execution from which the ML Model was created.
    :ivar status: 'draft', 'valid' or 'invalid' - When generated model are tested by API, only valid model can be used.
    :ivar needExactColumnNumbers: True by default, define if the model requires exact columns numbers to be executed.
    :ivar needExactColumnNames: True by default, define if the model requires exact columns names to be executed.
    :ivar has_anomalies: False by default, define if a model generate potential anomalies.
    :ivar has_target_feat: False by default, define if a model requires a target features to be trained or executed.
    :ivar input_columns: list of all columns used to trained the model.
    :ivar output_columns: list of all columns generated by the model.
    :ivar label_counts: Count of labels generated by the model.
    :ivar trained_model: The Trained model
    :ivar scaler: The scaler
    """

    @classmethod
    def route(cls):
        return "mlmodels"

    @classmethod
    def from_dict(cls, data):
        obj = MLModel()
        obj.from_json(data)
        return obj

    @classmethod
    def operations(cls):
        return ['lists', 'get_by_id', 'get_by_key', 'delete']

    @classmethod
    def get_type(cls):
        return "pickle"

    def __init__(self, model_id=None, generated_by_id=None,
                 exact_names=True, exact_numbers=True,
                 key=None):
        if model_id is None:
            model_id = uuid.uuid4()
        self.model_id = model_id
        self.key = key

        self.generatedById = generated_by_id

        self.status = 'draft'
        self.input_columns = []
        self.output_columns = []

        self.needExactColumnNumbers = exact_numbers
        self.needExactColumnNames = exact_names
        self.has_anomalies = False
        self.label_counts = 0
        self.has_target_feat = False

        self.trained_model = None
        self.scaler = None

        self.experimentId = None

    def api_id(self) -> str:
        """
        Id of the ML Model (model_id)

        :return: string formatted UUID of the Model ID.
        """
        return str(self.model_id).upper()

    def endpoint(self) -> str:
        """
        Name of the endpoints used to manipulate ML Models.
        :return: Endpoint name.
        """
        return "MLModels"

    def to_json(self, target: str = None):
        obj = {"id": str(self.model_id),
               "status": str(self.status),
               "needExactColumnNames": str(self.needExactColumnNames),
               "needExactColumnNumbers": str(self.needExactColumnNumbers),
               "hasAnomalies": str(self.has_anomalies),
               "hasTargetFeat": str(self.has_target_feat),
               "labelCount": str(self.label_counts)
               }
        if self.key is not None:
            obj["key"] = str(self.key)
        if self.generatedById is not None:
            obj["generatedById"] = str(self.generatedById)
        if self.input_columns is not None:
            obj["inputColumns"] = json.dumps(list(self.input_columns))
        if self.output_columns is not None:
            obj["outputColumns"] = json.dumps(list(self.output_columns))
        if self.experimentId is not None:
            obj["experimentId"] = str(self.experimentId)
        return obj

    def from_json(self, obj):
        """
        Load the ML Model entity from a dictionary representation of the ML Model.

        :param obj: Dict version of the ML Model.
        """
        if "id" in obj.keys():
            self.model_id = obj["id"]
        if "key" in obj.keys() and obj["key"] is not None:
            self.key = obj["key"]
        if "generatedById" in obj.keys() and obj["generatedById"] is not None:
            self.generatedById = uuid.UUID(obj["generatedById"])
        if "experimentId" in obj.keys() and obj["experimentId"] is not None:
            self.experimentId = uuid.UUID(obj["experimentId"])
        if "status" in obj.keys():
            self.status = str(obj["status"]).lower()
        if "inputColumns" in obj.keys():
            self.input_columns = json.loads(obj["inputColumns"])
        if "outputColumns" in obj.keys():
            self.output_columns = json.loads(obj["outputColumns"])
        if "labelCount" in obj.keys():
            self.label_counts = int(obj["labelCount"])
        if "hasAnomalies" in obj.keys():
            if isinstance(obj["hasAnomalies"], str) and obj["hasAnomalies"].lower() == "false":
                self.has_anomalies = False
            else:
                self.has_anomalies = bool(obj["hasAnomalies"])
        if "hasTargetFeat" in obj.keys():
            if isinstance(obj["hasTargetFeat"], str) and obj["hasTargetFeat"].lower() == "false":
                self.has_target_feat = False
            else:
                self.has_target_feat = bool(obj["hasTargetFeat"])
        if "needExactColumnNumbers" in obj.keys():
            if isinstance(obj["needExactColumnNumbers"], str) and obj["needExactColumnNumbers"].lower() == "false":
                self.needExactColumnNumbers = False
            else:
                self.needExactColumnNumbers = bool(obj["needExactColumnNumbers"])
        if "needExactColumnNames" in obj.keys():
            if isinstance(obj["needExactColumnNames"], str) and obj["needExactColumnNames"].lower() == "false":
                self.needExactColumnNames = False
            else:
                self.needExactColumnNames = bool(obj["needExactColumnNames"])

    def get_sample_payload(self):
        """
        Get a JSON formatted sample payload to call the ML Model.
        :return: JSON formatted sample payload.
        """
        pl_columns = {"timestamp": "[timestamp]"}
        for hardwareId in self.input_columns:
            pl_columns[hardwareId] = "[" + hardwareId + "]"
        pl_json = {
            "id": str(self.model_id),
            "dataset": pl_columns
        }
        return pl_json

