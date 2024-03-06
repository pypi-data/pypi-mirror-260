"""
Data Preparation in Vantage with Views
============================
tdprepview (speak T-D-prep-view) is a package for fitting
and transforming re-usable data preparation pipelines that are
saved in view definitions. Hence, no other permanent database objects
are required.
"""

__author__ = """Martin Hillebrand"""
__email__ = 'martin.hillebrand@teradata.com'
__version__ = '1.2.0'

from .pipeline._pipeline import Pipeline

from .preprocessing._impute import (
    Impute,
    ImputeText,
    SimpleImputer,
    IterativeImputer
)

from .preprocessing._transform import (
    Scale,
    StandardScaler,
    MaxAbsScaler,
    MinMaxScaler,
    RobustScaler,
    CutOff,
    CustomTransformer,
    Normalizer
)

from .preprocessing._discretize import (
    FixedWidthBinning,
    VariableWidthBinning,
    QuantileTransformer,
    DecisionTreeBinning,
    ThresholdBinarizer,
    Binarizer,
    ListBinarizer,
    LabelEncoder
)

from .preprocessing._features import (
    PolynomialFeatures,
    OneHotEncoder,
    MultiLabelBinarizer
)

from .preprocessing._dimensionality_reduction import (
    PCA
)

from .preprocessing._miscellaneous import (
    TryCast
)

from .preprocessing._hashing import (
    SimpleHashEncoder
)


__all__ = [
     'Pipeline',
     'Impute',
     'ImputeText',
     'SimpleImputer',
     'IterativeImputer',
     'Scale',
     'StandardScaler',
     'MaxAbsScaler',
     'MinMaxScaler',
     'RobustScaler',
     'CutOff',
     'CustomTransformer',
     'Normalizer',
     'FixedWidthBinning',
     'VariableWidthBinning',
     'QuantileTransformer',
     'DecisionTreeBinning',
     'ThresholdBinarizer',
     'Binarizer',
     'ListBinarizer',
     'LabelEncoder',
     'PolynomialFeatures',
     'OneHotEncoder',
     'MultiLabelBinarizer',
     'PCA',
     'TryCast',
     'SimpleHashEncoder'
]
