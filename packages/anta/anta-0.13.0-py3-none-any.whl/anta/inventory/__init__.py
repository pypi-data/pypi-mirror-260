# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""
Inventory Module for ANTA.
"""

from __future__ import annotations

import asyncio
import logging
from ipaddress import ip_address, ip_network
from pathlib import Path
from typing import Any, Optional

from pydantic import ValidationError
from yaml import YAMLError, safe_load

from anta.device import AntaDevice, AsyncEOSDevice
from anta.inventory.exceptions import InventoryIncorrectSchema, InventoryRootKeyError
from anta.inventory.models import AntaInventoryInput
from anta.logger import anta_log_exception

logger = logging.getLogger(__name__)


class AntaInventory(dict):  # type: ignore
    # dict[str, AntaDevice] - not working in python 3.8 hence the ignore
    """
    Inventory abstraction for ANTA framework.
    """

    # Root key of inventory part of the inventory file
    INVENTORY_ROOT_KEY = "anta_inventory"
    # Supported Output format
    INVENTORY_OUTPUT_FORMAT = ["native", "json"]

    def __str__(self) -> str:
        """Human readable string representing the inventory"""
        devs = {}
        for dev in self.values():
            if (dev_type := dev.__class__.__name__) not in devs:
                devs[dev_type] = 1
            else:
                devs[dev_type] += 1
        return f"ANTA Inventory contains {' '.join([f'{n} devices ({t})' for t, n in devs.items()])}"

    @staticmethod
    def _update_disable_cache(inventory_disable_cache: bool, kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Return new dictionary, replacing kwargs with added disable_cache value from inventory_value
        if disable_cache has not been set by CLI.

        Args:
            inventory_disable_cache (bool): The value of disable_cache in the inventory
            kwargs: The kwargs to instantiate the device
        """
        updated_kwargs = kwargs.copy()
        updated_kwargs["disable_cache"] = inventory_disable_cache or kwargs.get("disable_cache")
        return updated_kwargs

    @staticmethod
    def _parse_hosts(inventory_input: AntaInventoryInput, inventory: AntaInventory, **kwargs: Any) -> None:
        """
        Parses the host section of an AntaInventoryInput and add the devices to the inventory

        Args:
            inventory_input (AntaInventoryInput): AntaInventoryInput used to parse the devices
            inventory (AntaInventory): AntaInventory to add the parsed devices to
        """
        if inventory_input.hosts is None:
            return

        for host in inventory_input.hosts:
            updated_kwargs = AntaInventory._update_disable_cache(host.disable_cache, kwargs)
            device = AsyncEOSDevice(name=host.name, host=str(host.host), port=host.port, tags=host.tags, **updated_kwargs)
            inventory.add_device(device)

    @staticmethod
    def _parse_networks(inventory_input: AntaInventoryInput, inventory: AntaInventory, **kwargs: Any) -> None:
        """
        Parses the network section of an AntaInventoryInput and add the devices to the inventory.

        Args:
            inventory_input (AntaInventoryInput): AntaInventoryInput used to parse the devices
            inventory (AntaInventory): AntaInventory to add the parsed devices to

        Raises:
            InventoryIncorrectSchema: Inventory file is not following AntaInventory Schema.
        """
        if inventory_input.networks is None:
            return

        for network in inventory_input.networks:
            try:
                updated_kwargs = AntaInventory._update_disable_cache(network.disable_cache, kwargs)
                for host_ip in ip_network(str(network.network)):
                    device = AsyncEOSDevice(host=str(host_ip), tags=network.tags, **updated_kwargs)
                    inventory.add_device(device)
            except ValueError as e:
                message = "Could not parse network {network.network} in the inventory"
                anta_log_exception(e, message, logger)
                raise InventoryIncorrectSchema(message) from e

    @staticmethod
    def _parse_ranges(inventory_input: AntaInventoryInput, inventory: AntaInventory, **kwargs: Any) -> None:
        """
        Parses the range section of an AntaInventoryInput and add the devices to the inventory.

        Args:
            inventory_input (AntaInventoryInput): AntaInventoryInput used to parse the devices
            inventory (AntaInventory): AntaInventory to add the parsed devices to

        Raises:
            InventoryIncorrectSchema: Inventory file is not following AntaInventory Schema.
        """
        if inventory_input.ranges is None:
            return

        for range_def in inventory_input.ranges:
            try:
                updated_kwargs = AntaInventory._update_disable_cache(range_def.disable_cache, kwargs)
                range_increment = ip_address(str(range_def.start))
                range_stop = ip_address(str(range_def.end))
                while range_increment <= range_stop:  # type: ignore[operator]
                    # mypy raise an issue about comparing IPv4Address and IPv6Address
                    # but this is handled by the ipaddress module natively by raising a TypeError
                    device = AsyncEOSDevice(host=str(range_increment), tags=range_def.tags, **updated_kwargs)
                    inventory.add_device(device)
                    range_increment += 1
            except ValueError as e:
                message = f"Could not parse the following range in the inventory: {range_def.start} - {range_def.end}"
                anta_log_exception(e, message, logger)
                raise InventoryIncorrectSchema(message) from e
            except TypeError as e:
                message = f"A range in the inventory has different address families for start and end: {range_def.start} - {range_def.end}"
                anta_log_exception(e, message, logger)
                raise InventoryIncorrectSchema(message) from e

    @staticmethod
    def parse(
        filename: str | Path,
        username: str,
        password: str,
        enable: bool = False,
        enable_password: Optional[str] = None,
        timeout: Optional[float] = None,
        insecure: bool = False,
        disable_cache: bool = False,
    ) -> AntaInventory:
        # pylint: disable=too-many-arguments
        """
        Create an AntaInventory instance from an inventory file.
        The inventory devices are AsyncEOSDevice instances.

        Args:
            filename (str): Path to device inventory YAML file
            username (str): Username to use to connect to devices
            password (str): Password to use to connect to devices
            enable (bool): Whether or not the commands need to be run in enable mode towards the devices
            enable_password (str, optional): Enable password to use if required
            timeout (float, optional): timeout in seconds for every API call.
            insecure (bool): Disable SSH Host Key validation
            disable_cache (bool): Disable cache globally

        Raises:
            InventoryRootKeyError: Root key of inventory is missing.
            InventoryIncorrectSchema: Inventory file is not following AntaInventory Schema.
        """

        inventory = AntaInventory()
        kwargs: dict[str, Any] = {
            "username": username,
            "password": password,
            "enable": enable,
            "enable_password": enable_password,
            "timeout": timeout,
            "insecure": insecure,
            "disable_cache": disable_cache,
        }
        if username is None:
            message = "'username' is required to create an AntaInventory"
            logger.error(message)
            raise ValueError(message)
        if password is None:
            message = "'password' is required to create an AntaInventory"
            logger.error(message)
            raise ValueError(message)

        try:
            with open(file=filename, mode="r", encoding="UTF-8") as file:
                data = safe_load(file)
        except (TypeError, YAMLError, OSError) as e:
            message = f"Unable to parse ANTA Device Inventory file '{filename}'"
            anta_log_exception(e, message, logger)
            raise

        if AntaInventory.INVENTORY_ROOT_KEY not in data:
            exc = InventoryRootKeyError(f"Inventory root key ({AntaInventory.INVENTORY_ROOT_KEY}) is not defined in your inventory")
            anta_log_exception(exc, f"Device inventory is invalid! (from {filename})", logger)
            raise exc

        try:
            inventory_input = AntaInventoryInput(**data[AntaInventory.INVENTORY_ROOT_KEY])
        except ValidationError as e:
            anta_log_exception(e, f"Device inventory is invalid! (from {filename})", logger)
            raise

        # Read data from input
        AntaInventory._parse_hosts(inventory_input, inventory, **kwargs)
        AntaInventory._parse_networks(inventory_input, inventory, **kwargs)
        AntaInventory._parse_ranges(inventory_input, inventory, **kwargs)

        return inventory

    ###########################################################################
    # Public methods
    ###########################################################################

    ###########################################################################
    # GET methods
    ###########################################################################

    def get_inventory(self, established_only: bool = False, tags: Optional[list[str]] = None) -> AntaInventory:
        """
        Returns a filtered inventory.

        Args:
            established_only: Whether or not to include only established devices. Default False.
            tags: List of tags to filter devices.

        Returns:
            AntaInventory: An inventory with filtered AntaDevice objects.
        """

        def _filter_devices(device: AntaDevice) -> bool:
            """
            Helper function to select the devices based on the input tags
            and the requirement for an established connection.
            """
            if tags is not None and all(tag not in tags for tag in device.tags):
                return False
            return bool(not established_only or device.established)

        devices: list[AntaDevice] = list(filter(_filter_devices, self.values()))
        result = AntaInventory()
        for device in devices:
            result.add_device(device)
        return result

    ###########################################################################
    # SET methods
    ###########################################################################

    def __setitem__(self, key: str, value: AntaDevice) -> None:
        if key != value.name:
            raise RuntimeError(f"The key must be the device name for device '{value.name}'. Use AntaInventory.add_device().")
        return super().__setitem__(key, value)

    def add_device(self, device: AntaDevice) -> None:
        """Add a device to final inventory.

        Args:
            device: Device object to be added
        """
        self[device.name] = device

    ###########################################################################
    # MISC methods
    ###########################################################################

    async def connect_inventory(self) -> None:
        """Run `refresh()` coroutines for all AntaDevice objects in this inventory."""
        logger.debug("Refreshing devices...")
        results = await asyncio.gather(
            *(device.refresh() for device in self.values()),
            return_exceptions=True,
        )
        for r in results:
            if isinstance(r, Exception):
                message = "Error when refreshing inventory"
                anta_log_exception(r, message, logger)
