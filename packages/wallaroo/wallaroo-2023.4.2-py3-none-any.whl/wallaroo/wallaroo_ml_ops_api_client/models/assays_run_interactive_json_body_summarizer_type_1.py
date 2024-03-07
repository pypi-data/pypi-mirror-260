from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.assays_run_interactive_json_body_summarizer_type_1_type import \
    AssaysRunInteractiveJsonBodySummarizerType1Type

T = TypeVar("T", bound="AssaysRunInteractiveJsonBodySummarizerType1")


@attr.s(auto_attribs=True)
class AssaysRunInteractiveJsonBodySummarizerType1:
    """ 
        Attributes:
            name (str):
            type (AssaysRunInteractiveJsonBodySummarizerType1Type):
     """

    name: str
    type: AssaysRunInteractiveJsonBodySummarizerType1Type
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "type": type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = AssaysRunInteractiveJsonBodySummarizerType1Type(d.pop("type"))




        assays_run_interactive_json_body_summarizer_type_1 = cls(
            name=name,
            type=type,
        )

        assays_run_interactive_json_body_summarizer_type_1.additional_properties = d
        return assays_run_interactive_json_body_summarizer_type_1

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
