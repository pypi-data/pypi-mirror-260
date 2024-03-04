from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from vectice.api.json.dataset_version_representation import DatasetVersionRepresentationOutput
from vectice.models.representation.dataset_representation import DatasetRepresentation
from vectice.utils.common_utils import repr_class, strip_dict_list
from vectice.utils.dataframe_utils import repr_list_as_pd_dataframe

if TYPE_CHECKING:
    from pandas import DataFrame


class DatasetVersionRepresentation:
    """Represents the metadata of a Vectice dataset version.

    A Dataset Version Representation shows information about a specific version of a dataset from the Vectice app. It makes it easier to get and read this information through the API.
    NOTE: **Hint**
        A dataset version ID starts with 'DTV-XXX'. Retrieve the ID in the Vectice App, then use the ID with the following methods to get the dataset version:
        ```connect.dataset_version('DTV-XXX')``` or ```connect.browse('DTV-XXX')```
        (see [Connection page](https://api-docs.vectice.com/reference/vectice/connection/#vectice.Connection.dataset_version)).

    Attributes:
        id (str): The unique identifier of the dataset version.
        project_id (str): The identifier of the project to which the dataset version belongs.
        name (str): The name of the dataset version. For dataset versions it corresponds to the version number.
        description (str): The description of the dataset version.
        properties (List[Dict[str, Any]]): The properties associated with the dataset version.
        resources (List[Dict[str, Any]]): The resources summary with the type, number of files and aggregated total number of columns for each resource inside the dataset version.
        dataset_representation (DatasetRepresentation): Holds informations about the source dataset linked to the dataset version, where all versions are grouped together.
    """

    def __init__(self, output: DatasetVersionRepresentationOutput):
        self.id = output.id
        self.project_id = output.project_id
        self.name = output.name
        self.description = output.description
        self.properties = strip_dict_list(output.properties)
        self.resources = output.resources
        self.dataset_representation = DatasetRepresentation(output.dataset)

    def __repr__(self):
        return repr_class(self)

    def asdict(self) -> Dict[str, Any]:
        """Transform the DatasetVersionRepresentation into a organised dictionary.

        Returns:
            The object represented as a dictionary
        """
        flat_properties = {prop["key"]: prop["value"] for prop in self.properties}
        flat_resources = self._flatten_resources(self.resources) if self.resources else {}
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "properties": flat_properties,
            "resources": flat_resources,
            "dataset_representation": (
                self.dataset_representation._asdict()  # pyright: ignore reportPrivateUsage
                if self.dataset_representation
                else None
            ),
        }

    def properties_as_dataframe(self) -> DataFrame:
        """Transforms the properties of the DatasetVersionRepresentation into a DataFrame for better readability.

        Returns:
            A pandas DataFrame containing the properties of the dataset version.
        """
        return repr_list_as_pd_dataframe(self.properties)

    def resources_as_dataframe(self) -> DataFrame:
        """Transforms the resources of the DatasetVersionRepresentation into a DataFrame for better readability.

        Returns:
            A pandas DataFrame containing the resources of the dataset version.
        """
        return repr_list_as_pd_dataframe(self.resources)

    def _flatten_resources(self, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        flattened_resource = {}
        if len(resources) > 1 or (resources[0]["resource_type"] != "GENERIC"):
            flattened_resource = {}
            for res in resources:
                resource_type = res.pop("resource_type")
                flattened_resource[resource_type] = res
        else:
            resource_dict = resources[0]
            flattened_resource = {
                "number_of_items": resource_dict.get("number_of_items", None),
                "total_number_of_columns": resource_dict.get("total_number_of_columns", None),
            }
        return flattened_resource
