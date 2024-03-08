from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class EnumValue:
    """
    :ivar name: The name of the value.
    :ivar description: A description of the value.
    :ivar version: The version when the value was added. The string
        should match the content of the root version attribute of the
        schema. For example, "1.4.0.0".
    :ivar is_abstract: True ("1" or "true") indicates that the property
        is abstract and cannot be used to characterize a value. False
        ("0" or "false") or not given indicates a non-abstract property
        that can be instantiated.
    :ivar parent_kind: Points to a parent property kind
    """

    class Meta:
        name = "enumValue"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_length": 1,
            "max_length": 4000,
            "white_space": "collapse",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )
    is_abstract: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isAbstract",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parent_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )


@dataclass
class Value:
    class Meta:
        name = "value"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    is_abstract: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isAbstract",
            "type": "Element",
            "required": True,
        },
    )
    parent_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentKind",
            "type": "Element",
        },
    )


@dataclass
class EnumList:
    class Meta:
        name = "enumList"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    naming_system: Optional[str] = field(
        default=None,
        metadata={
            "name": "namingSystem",
            "type": "Element",
            "required": True,
        },
    )
    value: List[Value] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class EnumList1:
    """
    :ivar name: The name of the list.
    :ivar description: A description of the list. This specifies what
        the individual values represent.
    :ivar naming_system: The naming system within which the terms are
        defined.
    :ivar value: A description of an enumeration value.
    """

    class Meta:
        name = "enumList"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_length": 1,
            "max_length": 4000,
            "white_space": "collapse",
        },
    )
    naming_system: Optional[str] = field(
        default=None,
        metadata={
            "name": "namingSystem",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )
    value: List[EnumValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class EnumListSet:
    class Meta:
        name = "enumListSet"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"

    schema_location: Optional[str] = field(
        default=None,
        metadata={
            "name": "schemaLocation",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    enum_list: Optional[EnumList] = field(
        default=None,
        metadata={
            "name": "enumList",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class EnumListSet1:
    """
    :ivar enum_list: A single enumeration list.
    :ivar version: Data object schema version.  The fourth level must
        match the version of the schema constraints (enumerations and
        XML loader files) that are assumed by the document instance.
    """

    class Meta:
        name = "enumListSet"

    enum_list: List[EnumList] = field(
        default_factory=list,
        metadata={
            "name": "enumList",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
