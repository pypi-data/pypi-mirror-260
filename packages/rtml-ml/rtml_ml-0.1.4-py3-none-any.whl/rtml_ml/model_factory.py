from typing import Any, Dict, Optional

def get_model(
    model_name: str,
    hyperparameters: Optional[Dict[str, Any]] = {},
) -> 'Model':
    """
    Returns a model instance based on the model name
    """
    if model_name == 'RandomForestClassifier':
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(**hyperparameters)
    
    elif model_name == 'XGBoostClassifier':
        from xgb import XGBClassifier
        return XGBClassifier(**hyperparameters)

    else:
        raise ValueError(f"Model {model_name} not supported")