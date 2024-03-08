import ast
import base64
import bz2
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

import dill
import jijmodeling as jm
import numpy as np
from dimod import (
    BinaryQuadraticModel,
    ConstrainedQuadraticModel,
    DiscreteQuadraticModel,
)


class StrangeworksModelType(Enum):
    BinaryQuadraticModel = "BinaryQuadraticModel"
    ConstrainedQuadraticModel = "ConstrainedQuadraticModel"
    DiscreteQuadraticModel = "DiscreteQuadraticModel"
    JiJProblem = "JiJProblem"
    AquilaModel = "ndarray"
    QuboDict = "QuboDict"
    MPSFile = "MPSFile"
    HitachiModel = "HitachiModel"
    FujitsuModel = "FujitsuModel"
    MatrixMarket = "MatrixMarket"
    QplibFile = "QplibFile"


class MPSFile:
    def __init__(self, data: str):
        self.data = data

    @staticmethod
    def read_file(fname):
        with open(fname, "r") as f:
            file_string = f.read()
        return MPSFile(data=file_string)


class QuboDict:
    def __init__(self, data: dict):
        self.data = data


class AquilaNDArray:
    def __init__(self, data: np.ndarray):
        self.data = data


class HitachiModelList:
    def __init__(self, data: list[list[int]]):
        self.model = data


class FujitsuModelList:
    def __init__(self, data: dict[str, list[Any]]):
        self.model = data


class MatrixMarket:
    def __init__(self, model: str):
        self.model = model

    @staticmethod
    def read_file(fname):
        with open(fname, "r") as f:
            file_string = f.read()
        return MatrixMarket(model=file_string)


class QplibFile:
    def __init__(self, model: str):
        self.model = model

    @staticmethod
    def read_file(fname):
        with open(fname, "r") as f:
            file_string = f.read()
        return QplibFile(model=file_string)


class StrangeworksModel(ABC):
    """
    Abstract base class for Strangeworks optimization models. To create a new model type,
    subclass this class and implement the `to_str` and `from_str` methods. The `from_str`
    method should return the appropriate model object for the model type. The `to_str`
    method should return a string representation of the model object.

    Add the new model type to the `StrangeworksModelType` enum. The 'model_options' and
    'strangeworks_parameters' are optional parameters that can be used to pass additional
    information about the model to the optimization service.

    Attributes:
        model (Any): The optimization model object.
        model_type (StrangeworksModelType): The type of the optimization model.
        model_options (dict | None): Optional model options.
        strangeworks_parameters (dict | None): Optional parameters for Strangeworks optimization services.

    """

    model: Any
    model_type: StrangeworksModelType
    model_options: dict | None = None
    strangeworks_parameters: dict | None = None

    @abstractmethod
    def to_str(self) -> str:
        ...

    @staticmethod
    @abstractmethod
    def from_str(
        model_str: str,
    ) -> (
        BinaryQuadraticModel
        | ConstrainedQuadraticModel
        | DiscreteQuadraticModel
        | jm.Problem
        | AquilaNDArray
        | QuboDict
        | MPSFile
        | HitachiModelList
        | FujitsuModelList
        | MatrixMarket
        | QplibFile
    ):
        ...


class StrangeworksRemoteModel(StrangeworksModel):
    """
    TODO
    A model that is stored remotely and can be downloaded.
    Should be able to pass around a file identifier and download the model when needed.
    Should instantiate the appropriate model class when downloaded.

    Implementation proposal:

    ```
    model_url: str
    model_type: str
    headers: dict = None

    def to_str(self) -> str:
        return self.model_url

    def from_str(self, model_url=None):
        if model_url is None:
            model_url = self.model_url
        model_res = requests.get(model_url, headers=self.headers)
        model_str = model_res.content.decode(encoding=model_res.encoding)
        return StrangeworksModel.from_model_str(model_str)
    ```
    """

    pass


class StrangeworksBinaryQuadraticModel(StrangeworksModel):
    """
    A Strangeworks optimization model for binary quadratic problems.

    Attributes:
        model (BinaryQuadraticModel): The binary quadratic optimization model.
        model_type (StrangeworksModelType): The type of the optimization model.
    """

    def __init__(self, model: BinaryQuadraticModel):
        """
        Initializes a StrangeworksBinaryQuadraticModel object.

        Args:
            model (BinaryQuadraticModel): The binary quadratic optimization model.
        """
        self.model = model
        self.model_type = StrangeworksModelType.BinaryQuadraticModel

    def to_str(self) -> str:
        """
        Returns a string representation of the binary quadratic optimization model.

        Returns:
            str: A string representation of the binary quadratic optimization model.
        """
        bqm_str = json.dumps(self.model.to_serializable())
        bqm_bytes = bqm_str.encode("utf-8")
        bqm_bytes_compressed = bz2.compress(bqm_bytes)
        bqm_bytes_compressed_base64 = base64.b64encode(bqm_bytes_compressed)
        return bqm_bytes_compressed_base64.decode("utf-8")

    @staticmethod
    def from_str(model_str: str) -> BinaryQuadraticModel:
        """
        Returns a binary quadratic optimization model parsed from a string representation.

        Args:
            model_str (str): A string representation of the binary quadratic optimization model.

        Returns:
            BinaryQuadraticModel: The binary quadratic optimization model.
        """
        try:
            bqm_dict = json.loads(model_str)
        except json.decoder.JSONDecodeError:
            bqm_bytes_compressed_base64 = model_str.encode("utf-8")
            bqm_bytes_compressed = base64.b64decode(bqm_bytes_compressed_base64)
            bqm_bytes = bz2.decompress(bqm_bytes_compressed)
            bqm_str = bqm_bytes.decode("utf-8")
            bqm_dict = json.loads(bqm_str)
        return BinaryQuadraticModel.from_serializable(bqm_dict)


class StrangeworksConstrainedQuadraticModel(StrangeworksModel):
    """
    A Strangeworks optimization model for constrained quadratic problems.

    Attributes:
        model (ConstrainedQuadraticModel): The constrained quadratic optimization model.
        model_type (StrangeworksModelType): The type of the optimization model.

    """

    def __init__(self, model: ConstrainedQuadraticModel):
        """
        Initializes a StrangeworksConstrainedQuadraticModel object.

        Args:
            model (ConstrainedQuadraticModel): The constrained quadratic optimization model.
        """
        self.model = model
        self.model_type = StrangeworksModelType.ConstrainedQuadraticModel

    def to_str(self) -> str:
        """
        Returns a string representation of the constrained quadratic optimization model.

        Returns:
            str: A string representation of the constrained quadratic optimization model.
        """
        cqm_file = self.model.to_file()
        cqm_bytes = base64.b64encode(cqm_file.read())
        return cqm_bytes.decode("ascii")

    @staticmethod
    def from_str(model_str: str) -> ConstrainedQuadraticModel:
        """
        Returns a constrained quadratic optimization model parsed from a string representation.

        Args:
            model_str (str): A string representation of the constrained quadratic optimization model.

        Returns:
            ConstrainedQuadraticModel: The constrained quadratic optimization model.
        """
        return ConstrainedQuadraticModel.from_file(base64.b64decode(model_str))


class StrangeworksDiscreteQuadraticModel(StrangeworksModel):
    """
    A Strangeworks optimization model for discrete quadratic problems.

    Attributes:
        model (DiscreteQuadraticModel): The discrete quadratic optimization model.
        model_type (StrangeworksModelType): The type of the optimization model.

    """

    def __init__(self, model: DiscreteQuadraticModel):
        """
        Initializes a StrangeworksDiscreteQuadraticModel object.

        Args:
            model (DiscreteQuadraticModel): The discrete quadratic optimization model.
        """
        self.model = model
        self.model_type = StrangeworksModelType.DiscreteQuadraticModel

    def to_str(self) -> str:
        """
        Returns a string representation of the discrete quadratic optimization model.

        Returns:
            str: A string representation of the discrete quadratic optimization model.
        """
        cqm_file = self.model.to_file()
        cqm_bytes = base64.b64encode(cqm_file.read())
        return cqm_bytes.decode("ascii")

    @staticmethod
    def from_str(model_str: str) -> DiscreteQuadraticModel:
        """
        Returns a discrete quadratic optimization model parsed from a string representation.

        Args:
            model_str (str): A string representation of the discrete quadratic optimization model.

        Returns:
            DiscreteQuadraticModel: The discrete quadratic optimization model.
        """
        dqm = DiscreteQuadraticModel.from_file(base64.b64decode(model_str))
        if isinstance(dqm, DiscreteQuadraticModel):
            return dqm
        else:
            raise TypeError("Unexpected type for DQM model")


class StrangeworksQuboDictModel(StrangeworksModel):
    """
    A Strangeworks optimization model for QUBO problems represented as a dictionary.

    Attributes:
        model (QuboDict): The QUBO problem represented as a dictionary.
        model_type (StrangeworksModelType): The type of the optimization model.

    """

    def __init__(self, model: QuboDict):
        """
        Initializes a StrangeworksQuboDictModel object.

        Args:
            model (QuboDict): The QUBO problem represented as a dictionary.
        """
        self.model = model.data
        self.model_type = StrangeworksModelType.QuboDict

    def to_str(self) -> str:
        """
        Returns a string representation of the QUBO problem.

        Returns:
            str: A string representation of the QUBO problem.
        """
        model_str_keys = {str(key): value for key, value in self.model.items()}
        return json.dumps(model_str_keys)

    @staticmethod
    def from_str(model_str: str) -> QuboDict:
        """
        Returns a QUBO problem parsed from a string representation.

        Args:
            model_str (str): A string representation of the QUBO problem.

        Returns:
            QuboDict: The QUBO problem represented as a dictionary.
        """
        model_str_keys = json.loads(model_str)
        return QuboDict({ast.literal_eval(key): value for key, value in model_str_keys.items()})


class StrangeworksMPSFileModel(StrangeworksModel):
    """
    A Strangeworks optimization model for MPS file models.

    Attributes:
        model (MPSFile): The MPS file model.
        model_type (StrangeworksModelType): The type of the optimization model.
    """

    def __init__(self, model: MPSFile):
        """
        Initializes a StrangeworksMPSFileModel object.

        Args:
            model (MPSFIle): The MPS file model.
        """
        self.model = model
        self.model_type = StrangeworksModelType.MPSFile

    def to_str(self) -> str:
        """
        Returns a string representation of the MPS file model.

        Returns:
            str: A string representation of the MPS file model.
        """
        return str(self.model.data)

    @staticmethod
    def from_str(model_str: str) -> MPSFile:
        """
        Returns an MPS file model parsed from a string representation.

        Args:
            model_str (str): A string representation of the MPS file model.

        Returns:
            MPSFile: The MPS file model.
        """
        return MPSFile(model_str)


class StrangeworksJiJProblem(StrangeworksModel):
    """
    A Strangeworks optimization model for JiJ problems.

    Attributes:
        model (jm.Problem): The JiJ problem.
        model_type (StrangeworksModelType): The type of the optimization model.

    """

    def __init__(self, model: jm.Problem):
        """
        Initializes a StrangeworksJiJProblem object.

        Args:
            model (jm.Problem): The JiJ problem.
        """
        self.model = model
        self.model_type = StrangeworksModelType.JiJProblem

    def to_str(self) -> str:
        """
        Returns a string representation of the JiJ problem.

        Returns:
            str: A string representation of the JiJ problem.
        """
        return base64.b64encode(jm.to_protobuf(self.model)).decode()

    @staticmethod
    def from_str(model_str: str) -> jm.Problem:
        """
        Returns a JiJ problem parsed from a string representation.

        Args:
            model_str (str): A string representation of the JiJ problem.

        Returns:
            jm.Problem: The JiJ problem.
        """
        return jm.from_protobuf(base64.b64decode(model_str))  # type: ignore


class StrangeworkAquilaProblem(StrangeworksModel):
    """
    A Strangeworks optimization model for Aquila problems.

    Attributes:
        model (AquilaNDArray): The Aquila problem.
        model_type (StrangeworksModelType): The type of the optimization model.

    """

    def __init__(self, model: AquilaNDArray):
        """
        Initializes a StrangeworkAquilaProblem object.

        Args:
            model (AquilaNDArray): The Aquila problem.
        """
        self.model = model.data
        self.model_type = StrangeworksModelType.AquilaModel

    def to_str(self) -> str:
        """
        Returns a string representation of the Aquila problem.

        Returns:
            str: A string representation of the Aquila problem.
        """
        return base64.b64encode(dill.dumps(self.model)).decode()

    @staticmethod
    def from_str(model_str: str) -> AquilaNDArray:
        """
        Returns an Aquila problem parsed from a string representation.

        Args:
            model_str (str): A string representation of the Aquila problem.

        Returns:
            AquilaNDArray: The Aquila problem.
        """
        return AquilaNDArray(np.array(dill.loads(base64.b64decode(model_str))))


class StrangeworksHitachiProblem(StrangeworksModel):
    """
    https://annealing-cloud.com/en/web-api/reference/v2.html
    """

    def __init__(self, model: HitachiModelList):
        """
        Initializes a StrangeworkHitachiProblem object.

        Args:
            model (HitachiModelList): The Hitachi problem.
        """
        self.model = model
        self.model_type = StrangeworksModelType.HitachiModel

    def to_str(self) -> str:
        return json.dumps(self.model.model)

    @staticmethod
    def from_str(model_str: str) -> HitachiModelList:
        return HitachiModelList(json.loads(model_str))


class StrangeworksFujitsuProblem(StrangeworksModel):
    """ """

    def __init__(self, model: FujitsuModelList):
        """
        Initializes a StrangeworksFujitsuProblem object.

        Args:
            model (FujitsuModelList): The Fujitsu problem.
        """
        self.model = model
        self.model_type = StrangeworksModelType.FujitsuModel

    def to_str(self) -> str:
        return json.dumps(self.model.model)

    @staticmethod
    def from_str(model_str: str) -> FujitsuModelList:
        return FujitsuModelList(json.loads(model_str))


class StrangeworksMatrixMarketProblem(StrangeworksModel):
    """
    A Strangeworks optimization model for MatrixMarket text file models.

    Attributes:
        model (MatrixMarket): The qubo text file model.
        model_type (StrangeworksModelType): The type of the optimization model.
    """

    def __init__(self, model: MatrixMarket):
        """
        Initializes a StrangeworksMatrixMarketProblem object.

        Args:
            model (MatrixMarket): The MatrixMarket file model.
        """
        self.model = model
        self.model_type = StrangeworksModelType.MatrixMarket

    def to_str(self) -> str:
        """
        Returns a string representation of the file model.

        Returns:
            str: A string representation of the file model.
        """
        return str(self.model.model)

    @staticmethod
    def from_str(model_str: str) -> MatrixMarket:
        """
        Returns a MatrixMarket file model parsed from a string representation.

        Args:
            model_str (str): A string representation of the file model.

        Returns:
            MatrixMarket: The file model.
        """
        return MatrixMarket(model_str)


class StrangeworksQplibFileProblem(StrangeworksModel):
    """
    A Strangeworks optimization model for QplibFile .qplib file models.

    Attributes:
        model (QplibFile): The .qplib file model.
        model_type (StrangeworksModelType): The type of the optimization model.
    """

    def __init__(self, model: QplibFile):
        """
        Initializes a StrangeworksQplibFileProblem object.

        Args:
            model (QplibFile): The QplibFile file model.
        """
        self.model = model
        self.model_type = StrangeworksModelType.QplibFile

    def to_str(self) -> str:
        """
        Returns a string representation of the file model.

        Returns:
            str: A string representation of the file model.
        """
        return str(self.model.model)

    @staticmethod
    def from_str(model_str: str) -> QplibFile:
        """
        Returns a QplibFile file model parsed from a string representation.

        Args:
            model_str (str): A string representation of the file model.

        Returns:
            QplibFile: The file model.
        """
        return QplibFile(model_str)


class StrangeworksModelFactory:
    """
    A factory class for creating Strangeworks optimization models.

    Methods:
        from_model(model: Any) -> StrangeworksModel:
            Returns a StrangeworksModel object for the given optimization model.
        from_model_str(model_str: str, model_type: str, model_options: str | None = None,
                       strangeworks_parameters: str | None = None) -> StrangeworksModel:
            Returns a StrangeworksModel object parsed from a string representation.

    """

    @staticmethod
    def from_model(model: Any) -> StrangeworksModel:
        """
        Returns a StrangeworksModel object for the given optimization model.

        Args:
            model (Any): The optimization model.

        Returns:
            StrangeworksModel: The Strangeworks optimization model.
        """
        if isinstance(model, StrangeworksModel):
            return model
        elif isinstance(model, BinaryQuadraticModel):
            return StrangeworksBinaryQuadraticModel(model=model)
        elif isinstance(model, ConstrainedQuadraticModel):
            return StrangeworksConstrainedQuadraticModel(model=model)
        elif isinstance(model, DiscreteQuadraticModel):
            return StrangeworksDiscreteQuadraticModel(model=model)
        elif isinstance(model, QuboDict):
            return StrangeworksQuboDictModel(model=model)
        elif isinstance(model, jm.Problem):
            return StrangeworksJiJProblem(model=model)
        elif isinstance(model, AquilaNDArray):
            return StrangeworkAquilaProblem(model=model)
        elif isinstance(model, MPSFile):
            return StrangeworksMPSFileModel(model=model)
        elif isinstance(model, HitachiModelList):
            return StrangeworksHitachiProblem(model=model)
        elif isinstance(model, FujitsuModelList):
            return StrangeworksFujitsuProblem(model=model)
        elif isinstance(model, MatrixMarket):
            return StrangeworksMatrixMarketProblem(model=model)
        elif isinstance(model, QplibFile):
            return StrangeworksQplibFileProblem(model=model)
        else:
            raise ValueError("Unsupported model type")

    @staticmethod
    def from_model_str(
        model_str: str,
        model_type: str,
        model_options: str | None = None,
        strangeworks_parameters: str | None = None,
    ):
        """
        From a type and string representation of a model, return the appropriate
        StrangeworksModel. This is currently how we are deserializing models from
        into general native data formats.

        Returns a StrangeworksModel object parsed from a string representation.

        Args:
            model_str (str): A string representation of the optimization model.
            model_type (str): The type of the optimization model.
            model_options (str | None): The options used to create the optimization model.
            strangeworks_parameters (str | None): The parameters used to create the optimization model.

        Returns:
            StrangeworksModel: The Strangeworks optimization model.
        """
        m: (
            BinaryQuadraticModel
            | ConstrainedQuadraticModel
            | DiscreteQuadraticModel
            | jm.Problem
            | AquilaNDArray
            | QuboDict
            | MPSFile
            | HitachiModelList
            | FujitsuModelList
            | MatrixMarket
            | QplibFile
        )
        strangeworks_model_type = StrangeworksModelType(model_type)
        if strangeworks_model_type == StrangeworksModelType.BinaryQuadraticModel:
            m = StrangeworksBinaryQuadraticModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.ConstrainedQuadraticModel:
            m = StrangeworksConstrainedQuadraticModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.DiscreteQuadraticModel:
            m = StrangeworksDiscreteQuadraticModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.QuboDict:
            m = StrangeworksQuboDictModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.MPSFile:
            m = StrangeworksMPSFileModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.JiJProblem:
            m = StrangeworksJiJProblem.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.AquilaModel:
            m = StrangeworkAquilaProblem.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.HitachiModel:
            m = StrangeworksHitachiProblem.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.FujitsuModel:
            m = StrangeworksFujitsuProblem.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.MatrixMarket:
            m = StrangeworksMatrixMarketProblem.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.QplibFile:
            m = StrangeworksQplibFileProblem.from_str(model_str)
        else:
            raise ValueError("Unsupported model type")
        sm = StrangeworksModelFactory.from_model(m)
        sm.model_type = strangeworks_model_type
        sm.model_options = json.loads(model_options) if model_options else None
        sm.strangeworks_parameters = json.loads(strangeworks_parameters) if strangeworks_parameters else None
        return sm
