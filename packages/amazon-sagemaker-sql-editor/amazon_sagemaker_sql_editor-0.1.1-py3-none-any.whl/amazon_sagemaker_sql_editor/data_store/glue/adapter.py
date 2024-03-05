# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from amazon_sagemaker_sql_editor.adapter.adapters import (
    GetConnectionsResponseAdapter,
    PostDataSourcesResponseAdapter,
)
from amazon_sagemaker_sql_editor.model.models import (
    ConnectionsResponseModel,
    ConnectionMetadataModel,
    ConnectionModel,
    DataSourcesNodeDataModel as NodeDataModel,
    DataSourcesNodeResponseModel as NodeResponseModel,
)
from amazon_sagemaker_sql_editor.utils.constants import (
    NodeType,
    DataSourceType,
    DataSourcesConstants,
)
from amazon_sagemaker_sql_editor.utils.date_time import current_time_utc

from amazon_sagemaker_sql_editor.utils.exceptions import (
    SagemakerSQLResponseAdapterFault,
)


class GlueGetConnectionsResponseAdapter(GetConnectionsResponseAdapter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_model(**kwargs)

    def _set_model(self, **kwargs):
        connections_kwarg_name = "connections"
        if "connections" not in kwargs:
            raise SagemakerSQLResponseAdapterFault(
                f"{self.__class__.__name__}"
                f'.{self.__class__._set_model.__name__}() requires "{connections_kwarg_name}" as keyword argument'
            )

        connections = kwargs.get(connections_kwarg_name)
        connection_models = []
        for connection in connections["ConnectionList"]:
            # only add compatible connections
            if connection["ConnectionType"] in DataSourceType:
                connection_model = ConnectionModel(
                    name=connection["Name"],
                    type=connection["ConnectionType"],
                    source=DataSourcesConstants.CONNECTION_TYPE_GLUE,
                    metadata=ConnectionMetadataModel(description=connection["Description"]),
                    lastUpdateTime=connection["LastUpdatedTime"].timestamp(),
                )
                connection_models.append(connection_model)

        model = ConnectionsResponseModel(connections=connection_models)
        self.model = model


class GluePostDataSourcesResponseAdapter(PostDataSourcesResponseAdapter):
    def _set_model(self, **kwargs):
        if "connections" not in kwargs:
            raise SagemakerSQLResponseAdapterFault(
                f"{self.__class__.__name__}"
                f'._set_model() requires "connections" as positional argument'
            )

        connections = kwargs.get("connections")
        node_list = []
        for connection in connections["ConnectionList"]:
            # only add compatible connections
            if connection["ConnectionType"] in DataSourceType:
                node_model = NodeResponseModel(
                    name=connection["Name"],
                    nodeType=NodeType.DATA_SOURCE.value.__str__(),
                    isLeaf=False,
                    lastUpdateTime=connection["LastUpdatedTime"].timestamp(),
                    nodeData=NodeDataModel(
                        source=DataSourcesConstants.CONNECTION_TYPE_GLUE,
                        type=connection["ConnectionType"],
                    ),
                )
                node_list.append(node_model)

        self.model = NodeResponseModel(
            isLeaf=False,
            lastUpdateTime=current_time_utc().timestamp(),
            nodeData=NodeDataModel(type="", source=""),
            nodeList=node_list,
            nodeType=self._get_parent_node_type(NodeType.DATA_SOURCE.value.__str__()),
            name="root",
        )

    def _create_model_for_type(self, node_type: str, **kwargs):
        """
        Method to create model object for a specific node type

        :param node_type: node type defining the model object
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def _get_parent_node_type(self, child_node_type) -> str:
        """
        Method to get parent node type from child node type

        :param child_node_type: child node type
        :return:
        """
        return NodeType.ROOT.value.__str__()
