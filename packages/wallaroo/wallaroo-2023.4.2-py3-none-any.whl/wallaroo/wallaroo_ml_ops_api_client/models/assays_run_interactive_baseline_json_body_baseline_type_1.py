from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.assays_run_interactive_baseline_json_body_baseline_type_1_static import \
      AssaysRunInteractiveBaselineJsonBodyBaselineType1Static





T = TypeVar("T", bound="AssaysRunInteractiveBaselineJsonBodyBaselineType1")


@attr.s(auto_attribs=True)
class AssaysRunInteractiveBaselineJsonBodyBaselineType1:
    """ 
        Attributes:
            static (AssaysRunInteractiveBaselineJsonBodyBaselineType1Static):  Result from summarizing one sample
                collection.
     """

    static: 'AssaysRunInteractiveBaselineJsonBodyBaselineType1Static'
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        static = self.static.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "static": static,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assays_run_interactive_baseline_json_body_baseline_type_1_static import \
            AssaysRunInteractiveBaselineJsonBodyBaselineType1Static
        d = src_dict.copy()
        static = AssaysRunInteractiveBaselineJsonBodyBaselineType1Static.from_dict(d.pop("static"))




        assays_run_interactive_baseline_json_body_baseline_type_1 = cls(
            static=static,
        )

        assays_run_interactive_baseline_json_body_baseline_type_1.additional_properties = d
        return assays_run_interactive_baseline_json_body_baseline_type_1

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
