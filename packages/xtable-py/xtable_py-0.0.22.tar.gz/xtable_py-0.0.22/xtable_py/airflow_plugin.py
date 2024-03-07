from pathlib import Path

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.plugins_manager import AirflowPlugin

from xtable_py import xtable_cmd


class XtableOperator(BaseOperator):

    @apply_defaults
    def __init__(self, config: Path, catalog:Path, jars: Path, *args, **kwargs):
        super(XtableOperator, self).__init__(*args, **kwargs)
        self.config: Path = config
        self.catalog: Path = catalog
        self.jars: Path = jars

    def execute(self, context):
        xtable_cmd.setup(jars=self.jars)
        xtable_cmd.sync(config=self.config, catalog=self.catalog, jars=self.jars)


class XtablePlugin(AirflowPlugin):
    # The name of your plugin (str)
    name = "xtable"
    operators = [XtableOperator]
