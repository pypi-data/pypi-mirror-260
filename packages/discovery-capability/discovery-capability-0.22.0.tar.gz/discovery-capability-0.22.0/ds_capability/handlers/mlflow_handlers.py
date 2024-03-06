import os
import pyarrow as pa
import pyarrow.compute as pc
from ds_core.handlers.abstract_handlers import AbstractSourceHandler, AbstractPersistHandler
from ds_core.handlers.abstract_handlers import ConnectorContract, HandlerFactory

class MlflowSourceHandler(AbstractSourceHandler):
    """ A MLFlow source handler"""

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the source_contract dictionary """
        # required module import
        self.mlflow = HandlerFactory.get_module('mlflow')
        super().__init__(connector_contract)
        # connection
        self.connection = self.mlflow.set_tracking_uri(uri=f"{connector_contract.schema}://{connector_contract.address}")
        # address
        self.experiment = connector_contract.path
        self._changed_flag = True

    def supported_types(self) -> list:
        return ['']

    def exists(self) -> bool:
        _kwargs = self.connector_contract.query
        return True

    def has_changed(self) -> bool:
        return True

    def reset_changed(self, changed: bool=None):
        """ manual reset to say the file has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed

    def load_canonical(self, **kwargs) -> pa.Table:
        _kwargs = {**self.connector_contract.query, **kwargs}
        model = None
        return model


class MlflowPersistHandler(MlflowSourceHandler, AbstractPersistHandler):

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists the canonical dataset
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        with self.mlflow.start_run():
            model_info = self.mlflow.sklearn.log_model(sk_model=lr, artifact_path="iris_model")

    def remove_canonical(self, **kwargs) -> bool:
        return True

    def backup_canonical(self, canonical: pa.Table, uri: str, **kwargs) -> bool:
        pass

