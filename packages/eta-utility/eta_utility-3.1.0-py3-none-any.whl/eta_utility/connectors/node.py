""" This module implements the node class, which is used to parametrize connections

"""
from __future__ import annotations

import enum
import pathlib
from collections.abc import Mapping
from datetime import timedelta
from typing import TYPE_CHECKING

import pandas as pd
from attrs import converters, define, field, validators
from wetterdienst.metadata.parameter import Parameter
from wetterdienst.provider.dwd.mosmix.api import DwdMosmixParameter
from wetterdienst.provider.dwd.observation import (
    DwdObservationParameter,
    DwdObservationResolution,
)

from eta_utility import dict_get_any, get_logger, url_parse

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any, Callable
    from urllib.parse import ParseResult

    from eta_utility.type_hints import Path

default_schemes = {
    "modbus": "modbus.tcp",
    "opcua": "opc.tcp",
    "eneffco": "https",
    "local": "https",
    "entsoe": "https",
    "cumulocity": "https",
    "wetterdienst_observation": "https",
    "wetterdienst_prediction": "https",
}


log = get_logger("connectors")


def _strip_str(value: str) -> str:
    """Convenience function to convert a string to its stripped version.

    :param value: String to convert.
    :return: Stripped string.
    """
    return value.strip()


def _lower_str(value: str) -> str:
    """Convenience function to convert a string to its stripped and lowercase version.

    :param value: String to convert.
    :return: Stripped and lowercase string.
    """
    return value.strip().lower()


def _dtype_converter(value: str) -> Callable | None:
    """Specify data type conversion functions (i.e. to convert modbus types to python).

    :param value: Data type string to convert to callacle datatype converter.
    :return: Python datatype (callable).
    """
    _dtypes = {
        "boolean": bool,
        "bool": bool,
        "int": int,
        "uint32": int,
        "integer": int,
        "sbyte": int,
        "float": float,
        "double": float,
        "short": float,
        "string": str,
        "str": str,
        "bytes": bytes,
    }
    try:
        dtype = _dtypes[_lower_str(value)]
    except KeyError:
        log.warning(
            f"The specified data type ({value}) is currently not available in the datatype map and "
            f"will not be applied."
        )
        dtype = None

    return dtype


class NodeMeta(type):
    """Metaclass to define all Node classes as frozen attr dataclasses."""

    def __new__(cls, name: str, bases: tuple, namespace: dict[str, Any], **kwargs: Any) -> NodeMeta:
        new_cls = super().__new__(cls, name, bases, namespace, **kwargs)
        return define(frozen=True, slots=False)(new_cls)


class Node(metaclass=NodeMeta):
    """The node objects represents a single variable. Valid keyword arguments depend on the protocol."""

    #: Name for the node.
    name: str = field(converter=_strip_str, eq=True)
    #: URL of the connection.
    url: str = field(eq=True, order=True)
    #: Parse result object of the URL (in case more post-processing is required).
    url_parsed: ParseResult = field(init=False, repr=False, eq=False, order=False)
    #: Protocol of the connection.
    protocol: str = field(repr=False, eq=False, order=False)
    #: Username for login to the connection (default: None).
    usr: str | None = field(default=None, kw_only=True, repr=False, eq=False, order=False)
    #: Password for login to the connection (default: None).
    pwd: str | None = field(default=None, kw_only=True, repr=False, eq=False, order=False)
    #: Interval
    interval: str | None = field(
        default=None, converter=converters.optional(float), kw_only=True, repr=False, eq=False, order=False
    )
    #: Data type of the node (for value conversion). Note that strings will be interpreted as utf-8 encoded. If you
    #: do not want this behaviour, use 'bytes'.
    dtype: Callable | None = field(
        default=None, converter=converters.optional(_dtype_converter), kw_only=True, repr=False, eq=False, order=False
    )

    _registry = {}  # type: ignore

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Store subclass definitions to instantiate based on protocol."""
        protocol = kwargs.pop("protocol", None)
        if protocol:
            cls._registry[protocol] = cls

        return super().__init_subclass__(**kwargs)

    def __new__(cls, name: str, url: str, protocol: str, *args: Any, **kwargs: Any) -> Node:
        """Create node object of correct subclass corresponding to protocol."""
        try:
            subclass = cls._registry[protocol]
        except KeyError:
            raise ValueError(f"Specified an unsupported protocol: {protocol}.")

        # Return the correct subclass for the specified protocol
        obj = object.__new__(subclass)
        return obj

    def __attrs_post_init__(self) -> None:
        """Add post-processing to the url, username and password information. Username and password specified during
        class init take precedence.
        """
        url, usr, pwd = url_parse(self.url, scheme=default_schemes[self.protocol])

        if self.usr is None or str(self.usr) == "nan":
            object.__setattr__(self, "usr", usr)
        object.__setattr__(self, "usr", str(self.usr) if self.usr is not None else None)

        if self.pwd is None or str(self.pwd) == "nan":
            object.__setattr__(self, "pwd", pwd)
        object.__setattr__(self, "pwd", str(self.pwd) if self.pwd is not None else None)

        object.__setattr__(self, "url", url.geturl())
        object.__setattr__(self, "url_parsed", url)

    @classmethod
    def from_dict(cls, dikt: Sequence[Mapping] | Mapping[str, Any], fail: bool = True) -> list[Node]:
        """Create nodes from a dictionary of node configurations. The configuration must specify the following
        fields for each node:

            * Code (or name), URL, Protocol (i.e. modbus or opcua or eneffco).
              The URL should be a complete network location identifier. Alternatively it is possible to specify the
              location in two fields: IP and Port. These should only contain the respective parts (as in only an IP
              address and only the port number).
              The IP-Address should always be given without scheme (https://).

        For local nodes no additional fields are required.

        For Modbus nodes the following additional fields are required:

            * ModbusRegisterType (or mb_register), ModbusSlave (or mb_slave), ModbusChannel (or mb_channel).

        For OPC UA nodes the following additional fields are required:

            * Identifier.

        For EnEffCo nodes the code field must be present.

        For EntsoE nodes the endpoint field must be present.

        :param dikt: Configuration dictionary.
        :param fail: Set this to false, if you would like to log errors instead of raising them.
        :return: List of Node objects.
        """

        nodes = []

        iter_ = [dikt] if isinstance(dikt, Mapping) else dikt
        for idx, lnode in enumerate(iter_):
            node = {k.strip().lower(): v for k, v in lnode.items()}

            try:
                protocol = cls._read_dict_protocol(node)
            except KeyError as e:
                text = f"Error reading node protocol in row {idx + 1}: {e}."
                if fail:
                    raise KeyError(text)
                else:
                    log.error(text)
                continue

            try:
                node_class = cls._registry[protocol.strip().lower()]
            except KeyError:
                text = f"Specified an unsupported protocol in row {idx + 1}: {protocol}."
                if fail:
                    raise ValueError(text)
                else:
                    log.error(text)
                continue

            try:
                nodes.append(node_class._from_dict(node))
            except (TypeError, KeyError) as e:
                text = f"Error while reading the configuration data for node in row {idx + 1}: {e}."
                if fail:
                    raise TypeError(text)
                else:
                    log.error(text)

        return nodes

    @staticmethod
    def _read_dict_info(node: dict[str, Any]) -> tuple[str, str, str, str, int]:
        """Read general info about a node from a dictionary.

        :param node: dictionary containing node information.
        :return: name, pwd, url, usr of the node
        """
        # Read name first
        try:
            name = str(dict_get_any(node, "code", "name"))
            if name == "nan" or name is None:
                raise KeyError
        except KeyError:
            raise KeyError("Name or Code must be specified for all nodes in the dictionary.")
        # Find URL or IP and port
        if "url" in node and node["url"] is not None and str(node["url"]) not in {"nan", ""}:
            url = node["url"].strip()
        elif "ip" in node and node["ip"] is not None and str(node["ip"]) not in {"nan", ""}:
            _port = dict_get_any(node, "port", fail=False, default="")
            port = "" if _port in {None, ""} or str(_port) == "nan" else f":{int(_port)}"
            url = f"{dict_get_any(node, 'ip')}{port}"
        else:
            url = None
        usr = dict_get_any(node, "username", "user", "usr", fail=False)
        pwd = dict_get_any(node, "password", "pwd", "pw", fail=False)
        interval = dict_get_any(node, "interval", fail=False)
        return name, pwd, url, usr, interval

    @staticmethod
    def _read_dict_protocol(node: dict[str, Any]) -> str:
        try:
            protocol = str(dict_get_any(node, "protocol"))
            if protocol == "nan" or protocol is None:
                raise KeyError
        except KeyError:
            raise KeyError("Protocol must be specified for all nodes in the dictionary.")

        return protocol

    @staticmethod
    def _try_dict_get_any(dikt: dict[str, Any], *names: str) -> Any:
        """Get any of the specified items from the node, if any are available. The function will return
        the first value it finds, even if there are multiple matches.

        This function will output sensible error messages, when the values are not found.

        :param dikt: Dictionary of the node to get values from.
        :param names: Item names to look for.
        :return: Value from dictionary.
        """
        try:
            value = dict_get_any(dikt, *names, fail=True)
        except KeyError:
            log.error(f"For the node, the field '{names[0]}' must be specified or check the correct spelling.")
            raise KeyError(
                "The required parameter for the node configuration was not found (see log). "
                "Could not load config "
                "file. "
            )

        return value

    @classmethod
    def from_excel(cls, path: Path, sheet_name: str, fail: bool = True) -> list[Node]:
        """
        Method to read out nodes from an Excel document. The document must specify the following fields:

            * Code, IP, Port, Protocol (modbus or opcua or eneffco).

        For Modbus nodes the following additional fields are required:

            * ModbusRegisterType, ModbusByte, ModbusChannel.

        For OPC UA nodes the following additional fields are required:

            * Identifier.

        For EnEffCo nodes the Code field must be present.

        The IP-Address should always be given without scheme (https://).

        :param path: Path to Excel document.
        :param sheet_name: name of Excel sheet, which will be read out.
        :param fail: Set this to false, if you would like to log errors instead of raising them.
        :return: List of Node objects.
        """

        file = path if isinstance(path, pathlib.Path) else pathlib.Path(path)
        input_ = pd.read_excel(file, sheet_name=sheet_name, dtype=str)

        return cls.from_dict(list(input_.to_dict("index").values()), fail)

    @classmethod
    def get_eneffco_nodes_from_codes(cls, code_list: Sequence[str], eneffco_url: str) -> list[Node]:
        """
        Utility function to retrieve Node objects from a list of EnEffCo Codes (Identifiers).

        .. deprecated:: v2.0.0
            Use the *from_ids* function of the EnEffCoConnection Class instead.

        :param code_list: List of EnEffCo identifiers to create nodes from.
        :param eneffco_url: URL to the EnEffCo system.
        :return: List of EnEffCo nodes.
        """
        nodes = []
        for code in code_list:
            nodes.append(cls(name=code, url=eneffco_url, protocol="eneffco", eneffco_code=code))
        return nodes


class NodeLocal(Node, protocol="local"):
    """Local Node (no specific protocol), useful for example to manually provide data to subscription handlers."""

    def __attrs_post_init__(self) -> None:
        """Ensure username and password are processed correctly."""
        super().__attrs_post_init__()

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeLocal:
        """Create a modblocalus node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeLocal object.
        """
        name, pwd, url, usr, interval = cls._read_dict_info(dikt)
        try:
            return cls(name, url, "local", usr=usr, pwd=pwd, interval=interval)
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}")


def _mb_byteorder_converter(value: str) -> str:
    """Convert some values for mb_byteorder.

    :param value: Value to be converted to mb_byteorder
    :return: mb_byteorder corresponding to correct scheme.
    """
    value = _lower_str(value)
    if value in {"little", "littleendian"}:
        return "little"

    if value in {"big", "bigendian"}:
        return "big"

    return ""


class NodeModbus(Node, protocol="modbus"):
    """Node for the Modbus protocol."""

    #: Modbus Slave ID
    mb_slave: int | None = field(kw_only=True, default=32, converter=int)
    #: Modbus Register name. One of input, discrete_input, coils and holding. Note that only coils and
    #: holding can be written to.
    mb_register: str = field(
        kw_only=True, converter=_lower_str, validator=validators.in_({"input", "discrete_input", "coils", "holding"})
    )
    #: Modbus Channel (Address of the value)
    mb_channel: int = field(kw_only=True, converter=int)
    #: Length of the value in bits (default 32). This determines, how much data is read from the server. The
    #: value must be a multiple of 16.
    mb_bit_length: int = field(kw_only=True, default=32, converter=int, validator=validators.ge(1))

    #: Byteorder of values returned by modbus
    mb_byteorder: str = field(
        kw_only=True, converter=_mb_byteorder_converter, validator=validators.in_({"little", "big"})
    )

    def __attrs_post_init__(self) -> None:
        """Add default port to the URL and convert mb_byteorder values."""
        super().__attrs_post_init__()

        # Set port to default 502 if it was not explicitly specified
        if not isinstance(self.url_parsed.port, int):
            url = self.url_parsed._replace(netloc=f"{self.url_parsed.hostname}:502")
            object.__setattr__(self, "url", url.geturl())
            object.__setattr__(self, "url_parsed", url)

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeModbus:
        """Create a modbus node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeModbus object.
        """
        name, pwd, url, usr, interval = cls._read_dict_info(dikt)

        # Initialize node if protocol is 'modbus'
        try:
            mb_register = cls._try_dict_get_any(dikt, "mb_register", "modbusregistertype")
            mb_channel = cls._try_dict_get_any(dikt, "mb_channel", "modbuschannel")
            mb_byteorder = cls._try_dict_get_any(dikt, "mb_byteorder", "modbusbyteorder")
            mb_slave = dict_get_any(dikt, "mb_slave", "modbusslave", fail=False, default=32)
            mb_bit_length = dict_get_any(dikt, "mb_bit_length", "mb_bitlength", fail=False, default=32)
            dtype = dict_get_any(dikt, "dtype", "datentyp", fail=False)
        except KeyError:
            raise KeyError(
                f"The required parameter for the node configuration was not found (see log). The node {name} could "
                f"not load."
            )

        try:
            return cls(
                name,
                url,
                "modbus",
                usr=usr,
                pwd=pwd,
                mb_register=mb_register,
                mb_slave=mb_slave,
                mb_channel=mb_channel,
                mb_bit_length=mb_bit_length,
                mb_byteorder=mb_byteorder,
                dtype=dtype,
                interval=interval,
            )
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}.")


class NodeOpcUa(Node, protocol="opcua"):
    """Node for the OPC UA protocol."""

    #: Node ID of the OPC UA Node.
    opc_id: str | None = field(default=None, kw_only=True, converter=converters.optional(_strip_str))
    #: Path to the OPC UA node.
    opc_path_str: str | None = field(
        default=None, kw_only=True, converter=converters.optional(_strip_str), repr=False, eq=False, order=False
    )
    #: Namespace of the OPC UA Node.
    opc_ns: int | None = field(default=None, kw_only=True, converter=converters.optional(_lower_str))

    # Additional fields which will be determined automatically
    #: Type of the OPC UA Node ID Specification.
    opc_id_type: str = field(
        init=False, converter=str, validator=validators.in_({"i", "s"}), repr=False, eq=False, order=False
    )
    #: Name of the OPC UA Node.
    opc_name: str = field(init=False, repr=False, eq=False, order=False, converter=str)
    #: Path to the OPC UA node in list representation. Nodes in this list can be used to access any
    #: parent objects.
    opc_path: list[NodeOpcUa] = field(init=False, repr=False, eq=False, order=False)

    def __attrs_post_init__(self) -> None:
        """Add default port to the URL and convert mb_byteorder values."""
        super().__attrs_post_init__()

        # Set port to default 4840 if it was not explicitly specified
        if not isinstance(self.url_parsed.port, int):
            url = self.url_parsed._replace(netloc=f"{self.url_parsed.hostname}:4840")
            object.__setattr__(self, "url", url.geturl())
            object.__setattr__(self, "url_parsed", url)

        # Determine, which values to use for initialization and set values
        if self.opc_id is not None:
            try:
                parts = self.opc_id.split(";")
            except ValueError:
                raise ValueError(
                    f"When specifying opc_id, make sure it follows the format ns=2;s=.path (got {self.opc_id})."
                )
            for part in parts:
                try:
                    key, val = part.split("=")
                except ValueError:
                    raise ValueError(
                        f"When specifying opc_id, make sure it follows the format ns=2;s=.path (got {self.opc_id})."
                    )

                if key.strip().lower() == "ns":
                    object.__setattr__(self, "opc_ns", int(val))
                else:
                    object.__setattr__(self, "opc_id_type", key.strip().lower())
                    object.__setattr__(self, "opc_path_str", val.strip(" "))

            object.__setattr__(self, "opc_id", f"ns={self.opc_ns};{self.opc_id_type}={self.opc_path_str}")

        elif self.opc_path_str is not None and self.opc_ns is not None:
            object.__setattr__(self, "opc_id_type", "s")
            object.__setattr__(self, "opc_id", f"ns={self.opc_ns};s={self.opc_path_str}")
        else:
            raise ValueError("Specify opc_id or opc_path_str and ns for OPC UA nodes.")

        # Determine the name and path of the opc node
        split_path = (
            self.opc_path_str.rsplit(".", maxsplit=len(self.opc_path_str.split(".")) - 2)  # type: ignore
            if self.opc_path_str[0] == "."  # type: ignore
            else self.opc_path_str.split(".")  # type: ignore
        )

        object.__setattr__(self, "opc_name", split_path[-1].split(".")[-1])
        path = []
        for k in range(len(split_path) - 1):
            path.append(
                Node(
                    split_path[k].strip(" ."),
                    self.url,
                    "opcua",
                    usr=self.usr,
                    pwd=self.pwd,
                    opc_id="ns={};s={}".format(self.opc_ns, ".".join(split_path[: k + 1])),
                )
            )
        object.__setattr__(self, "opc_path", path)

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeOpcUa:
        """Create an opcua node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeOpcUa object.
        """
        name, pwd, url, usr, interval = cls._read_dict_info(dikt)

        opc_id = dict_get_any(dikt, "opc_id", "identifier", "identifier", fail=False)
        dtype = dict_get_any(dikt, "dtype", "datentyp", fail=False)

        if opc_id is None:
            opc_ns = dict_get_any(dikt, "opc_ns", "namespace", "ns", fail=False)
            opc_path_str = dict_get_any(dikt, "opc_path", "path", fail=False)
            try:
                return cls(
                    name,
                    url,
                    "opcua",
                    usr=usr,
                    pwd=pwd,
                    opc_ns=opc_ns,
                    opc_path_str=opc_path_str,
                    dtype=dtype,
                    interval=interval,
                )
            except (TypeError, AttributeError):
                raise TypeError(
                    f"Could not convert all types for node {name}. Either the 'node_id' or the 'opc_ns' "
                    f"and 'opc_path' must be specified."
                )
        else:
            try:
                return cls(name, url, "opcua", usr=usr, pwd=pwd, opc_id=opc_id, dtype=dtype, interval=interval)
            except (TypeError, AttributeError):
                raise TypeError(
                    f"Could not convert all types for node {name}. Either the 'node_id' or the 'opc_ns' "
                    f"and 'opc_path' must be specified."
                )


class NodeEnEffCo(Node, protocol="eneffco"):
    """Node for the EnEffCo API."""

    #: EnEffCo datapoint code / ID.
    eneffco_code: str = field(kw_only=True, converter=str)

    def __attrs_post_init__(self) -> None:
        """Ensure username and password are processed correctly."""
        super().__attrs_post_init__()

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeEnEffCo:
        """Create a EnEffCo node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeEnEffCo object.
        """
        name, pwd, url, usr, interval = cls._read_dict_info(dikt)
        try:
            code = cls._try_dict_get_any(dikt, "code", "eneffco_code")
        except KeyError:
            raise KeyError(
                f"The required parameter for the node configuration was not found (see log). The node {name} could "
                f"not load."
            )

        try:
            return cls(name, url, "eneffco", usr=usr, pwd=pwd, eneffco_code=code, interval=interval)
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}.")


class NodeEntsoE(Node, protocol="entsoe"):
    """Node for the EntsoE API (see `ENTSO-E Transparency Platform API
    <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_).

    .. list-table:: **Available endpoint**
        :widths: 25 35
        :header-rows: 1

        * - Endpoint
          - Description
        * - ActualGenerationPerType
          - Actual Generation Per Energy Type
        * - Price
          - Price day ahead

    Currently, there is only two endpoints available, due to the parameter managing required by the API documentation.
    The other possible endpoints are listed in

    `eta_utility.connectors.entso_e._ConnectionConfiguration._doc_types`

    .. list-table:: **Main bidding zone**
        :widths: 15 25
        :header-rows: 1

        * - Bidding Zone
          - Description
        * - DEU-LUX
          - Deutschland-Luxemburg

    The other possible bidding zones are listed in

    `eta_utility.connectors.entso_e._ConnectionConfiguration._bidding_zones`

    """

    #: REST endpoint.
    endpoint: str = field(kw_only=True, converter=str)
    #: Bidding zone.
    bidding_zone: str = field(kw_only=True, converter=str)

    def __attrs_post_init__(self) -> None:
        """Ensure username and password are processed correctly."""
        super().__attrs_post_init__()

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeEntsoE:
        """Create an EntsoE node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeEntsoE object.
        """
        name, pwd, url, usr, interval = cls._read_dict_info(dikt)

        try:
            endpoint = cls._try_dict_get_any(dikt, "endpoint")
            bidding_zone = cls._try_dict_get_any(dikt, "bidding zone", "bidding_zone", "zone")
        except KeyError:
            raise KeyError(
                f"The required parameter for the node configuration was not found (see log). The node {name} could "
                f"not load."
            )

        try:
            return cls(
                name, url, "entsoe", usr=usr, pwd=pwd, endpoint=endpoint, bidding_zone=bidding_zone, interval=interval
            )
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}.")


class NodeCumulocity(Node, protocol="cumulocity"):
    """Node for the Cumulocity API."""

    # parameters for reading/writing from/to cumulocity nodes
    device_id: str = field(kw_only=True, converter=str)
    measurement: str = field(kw_only=True, converter=str)
    fragment: str = field(kw_only=True, converter=str, default="")

    def __attrs_post_init__(self) -> None:
        """Ensure username and password are processed correctly."""
        super().__attrs_post_init__()

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeCumulocity:
        """Create a Cumulocity node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeCumulocity object.
        """
        name, pwd, url, usr, interval = cls._read_dict_info(dikt)
        try:
            device_id = cls._try_dict_get_any(dikt, "id", "device_id")
        except KeyError:
            raise KeyError(
                f"The required parameter for the node configuration was not found (see log). The node {name} could "
                f"not load."
            )
        try:
            measurement = cls._try_dict_get_any(dikt, "measurement", "Measurement")
        except KeyError:
            raise KeyError(
                f"The required parameter for the node configuration was not found (see log). The node {name} could "
                f"not load."
            )

        try:
            fragment = cls._try_dict_get_any(dikt, "fragment", "Fragment")
        except KeyError:
            fragment = ""
        try:
            return cls(
                name,
                url,
                "cumulocity",
                usr=usr,
                pwd=pwd,
                device_id=device_id,
                measurement=measurement,
                fragment=fragment,
            )
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}.")


class NodeWetterdienst(Node):
    """
    Basic Node for the Wetterdienst API.
    This class is not meant to be used directly, but to be subclassed by
    NodeWetterdienstObservation and NodeWetterdienstPrediction.
    """

    #: Parameter to read from wetterdienst (e.g HUMIDITY or TEMPERATURE_AIR_200)
    parameter: str = field(kw_only=True, converter=str)

    #: The id of the weather station
    station_id: str | None = field(default=None, kw_only=True)
    #: latitude and longitude (not necessarily a weather station)
    latlon: str | None = field(default=None, kw_only=True)
    #: Number of stations to be used for the query
    number_of_stations: int | None = field(default=None, kw_only=True)

    def __attrs_post_init__(self) -> None:
        """Ensure that all required parameters are present."""
        super().__attrs_post_init__()
        object.__setattr__(self, "parameter", self.parameter.upper())
        if self.station_id is None and (self.latlon is None or self.number_of_stations is None):
            raise ValueError(
                "The required parameter 'station_id' or 'latlon' and 'number_of_stations' for the node configuration "
                "was not found. The node could not load."
            )
        parameters = [item.name for item in Parameter]
        if self.parameter not in parameters:
            raise ValueError(
                f"Parameter {self.parameter} is not valid. Valid parameters can be found here:"
                f"https://wetterdienst.readthedocs.io/en/latest/data/parameters.html"
            )

    @classmethod
    def _get_params(cls, dikt: dict[str, Any]) -> dict[str, Any]:
        """Get the common parameters for a Wetterdienst node.

        :param dikt: dictionary with node information.
        :return: dict with: parameter, station_id, latlon, number_of_stations
        """
        return {
            "parameter": dikt.get("parameter"),
            "station_id": dikt.get("station_id"),
            "latlon": dikt.get("latlon"),
            "number_of_stations": dikt.get("number_of_stations"),
        }


class NodeWetterdienstObservation(NodeWetterdienst, protocol="wetterdienst_observation"):
    """
    Node for the Wetterdienst API to get weather observations.
    For more information see: https://wetterdienst.readthedocs.io/en/latest/data/coverage/dwd/observation.html
    """

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        resolution = self.convert_interval_to_resolution(self.interval)  # type: ignore
        # Sort out the parameters by resolution
        available_params = DwdObservationParameter[resolution]
        available_params = [param.name for param in available_params if type(param) is not enum.EnumMeta]

        # If the parameter is not in the available parameters for the resolution, generate a list
        # of available resolutions for the parameter and raise an error
        if self.parameter not in available_params:
            available_resolutions = []
            for resolution in DwdObservationResolution:
                params = DwdObservationParameter[resolution.name]  # type: ignore
                if self.parameter in [param.name for param in params if type(param) is not enum.EnumMeta]:
                    available_resolutions.append(resolution.name)  # type: ignore
            if len(available_resolutions) == 0:
                raise ValueError(f"Parameter {self.parameter} is not a valid observation parameter.")
            raise ValueError(
                f"Parameter {self.parameter} is not valid for the given resolution. "
                f"Valid resolutions for parameter {self.parameter} are: "
                f"{available_resolutions}"
            )

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeWetterdienstObservation:
        """Create a WetterdienstObservation node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeWetterdienst object.
        """
        name, _, url, _, interval = cls._read_dict_info(dikt)
        params = cls._get_params(dikt)
        try:
            return cls(name, url, "wetterdienst_observation", interval=interval, **params)
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}.")

    @staticmethod
    def convert_interval_to_resolution(interval: int | str | timedelta) -> str:
        resolutions = {
            60: "MINUTE_1",
            300: "MINUTE_5",
            600: "MINUTE_10",
            3600: "HOURLY",
            28800: "SUBDAILY",  # not 8h intervals, measured at 7am, 2pm, 9pm
            86400: "DAILY",
            2592000: "MONTHLY",
            31536000: "ANNUAL",
        }
        interval = int(interval.total_seconds()) if isinstance(interval, timedelta) else int(interval)
        if interval not in resolutions.keys():
            raise ValueError(f"Interval {interval} not supported. Must be one of {list(resolutions.keys())}")
        return resolutions[interval]


class NodeWetterdienstPrediction(NodeWetterdienst, protocol="wetterdienst_prediction"):
    """
    Node for the Wetterdienst API to get weather predictions.
    For more information see: https://wetterdienst.readthedocs.io/en/latest/data/coverage/dwd/mosmix.html
    """

    #: Type of the MOSMIX prediction. Either 'SMALL' or 'LARGE'
    mosmix_type: str = field(default=None, kw_only=True, converter=str)

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        object.__setattr__(self, "mosmix_type", self.mosmix_type.upper())
        if self.mosmix_type not in {"SMALL", "LARGE"}:
            raise ValueError("mosmix_type must be either 'SMALL' or 'LARGE'")
        # Sort out the parameters by resolution
        params = DwdMosmixParameter[self.mosmix_type]
        # Create list of available parameters, enums are excluded because they are datasets
        available_params = [param.name for param in params if type(param) is not enum.EnumMeta]

        if self.parameter not in available_params:
            raise ValueError(
                f"Parameter {self.parameter} is not valid for the given resolution."
                f"Valid parameters for resolution {self.mosmix_type} can be found here:"
                f"https://wetterdienst.readthedocs.io/en/latest/data/coverage/dwd/mosmix/hourly.html"
            )

    @classmethod
    def _from_dict(cls, dikt: dict[str, Any]) -> NodeWetterdienstPrediction:
        """Create a WetterdienstPrediction node from a dictionary of node information.

        :param dikt: dictionary with node information.
        :return: NodeWetterdienst object.
        """
        name, _, url, _, _ = cls._read_dict_info(dikt)
        params = cls._get_params(dikt)
        mosmix_type = dikt.get("mosmix_type")
        try:
            return cls(name, url, "wetterdienst_prediction", mosmix_type=mosmix_type, **params)
        except (TypeError, AttributeError):
            raise TypeError(f"Could not convert all types for node {name}.")
