from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.models_upload_stream_response_200_insert_models_returning_item import \
      ModelsUploadStreamResponse200InsertModelsReturningItem





T = TypeVar("T", bound="ModelsUploadStreamResponse200InsertModels")


@attr.s(auto_attribs=True)
class ModelsUploadStreamResponse200InsertModels:
    """  Response payload wrapper.

        Attributes:
            returning (List['ModelsUploadStreamResponse200InsertModelsReturningItem']):  List of response details.
     """

    returning: List['ModelsUploadStreamResponse200InsertModelsReturningItem']
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        returning = []
        for returning_item_data in self.returning:
            returning_item = returning_item_data.to_dict()

            returning.append(returning_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "returning": returning,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.models_upload_stream_response_200_insert_models_returning_item import \
            ModelsUploadStreamResponse200InsertModelsReturningItem
        d = src_dict.copy()
        returning = []
        _returning = d.pop("returning")
        for returning_item_data in (_returning):
            returning_item = ModelsUploadStreamResponse200InsertModelsReturningItem.from_dict(returning_item_data)



            returning.append(returning_item)


        models_upload_stream_response_200_insert_models = cls(
            returning=returning,
        )

        models_upload_stream_response_200_insert_models.additional_properties = d
        return models_upload_stream_response_200_insert_models

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
