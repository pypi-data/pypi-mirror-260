# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
# pylint: disable=too-many-branches
"""
ANTA runner function
"""
from __future__ import annotations

import asyncio
import logging
from typing import Tuple

from anta import GITHUB_SUGGESTION
from anta.catalog import AntaCatalog, AntaTestDefinition
from anta.device import AntaDevice
from anta.inventory import AntaInventory
from anta.logger import anta_log_exception
from anta.models import AntaTest
from anta.result_manager import ResultManager

logger = logging.getLogger(__name__)

AntaTestRunner = Tuple[AntaTestDefinition, AntaDevice]


async def main(manager: ResultManager, inventory: AntaInventory, catalog: AntaCatalog, tags: list[str] | None = None, established_only: bool = True) -> None:
    """
    Main coroutine to run ANTA.
    Use this as an entrypoint to the test framwork in your script.

    Args:
        manager: ResultManager object to populate with the test results.
        inventory: AntaInventory object that includes the device(s).
        catalog: AntaCatalog object that includes the list of tests.
        tags: List of tags to filter devices from the inventory. Defaults to None.
        established_only: Include only established device(s). Defaults to True.

    Returns:
        any: ResultManager object gets updated with the test results.
    """
    if not catalog.tests:
        logger.info("The list of tests is empty, exiting")
        return
    if len(inventory) == 0:
        logger.info("The inventory is empty, exiting")
        return
    await inventory.connect_inventory()
    devices: list[AntaDevice] = list(inventory.get_inventory(established_only=established_only, tags=tags).values())

    if not devices:
        logger.info(
            f"No device in the established state '{established_only}' "
            f"{f'matching the tags {tags} ' if tags else ''}was found. There is no device to run tests against, exiting"
        )

        return
    coros = []
    # Using a set to avoid inserting duplicate tests
    tests_set: set[AntaTestRunner] = set()
    for device in devices:
        if tags:
            # If there are CLI tags, only execute tests with matching tags
            tests_set.update((test, device) for test in catalog.get_tests_by_tags(tags))
        else:
            # If there is no CLI tags, execute all tests without filters
            tests_set.update((t, device) for t in catalog.tests if t.inputs.filters is None or t.inputs.filters.tags is None)

            # Then add the tests with matching tags from device tags
            tests_set.update((t, device) for t in catalog.get_tests_by_tags(device.tags))

    tests: list[AntaTestRunner] = list(tests_set)

    if not tests:
        logger.info(f"There is no tests{f' matching the tags {tags} ' if tags else ' '}to run on current inventory. " "Exiting...")
        return

    for test_definition, device in tests:
        try:
            test_instance = test_definition.test(device=device, inputs=test_definition.inputs)

            coros.append(test_instance.test())
        except Exception as e:  # pylint: disable=broad-exception-caught
            # An AntaTest instance is potentially user-defined code.
            # We need to catch everything and exit gracefully with an
            # error message
            message = "\n".join(
                [
                    f"There is an error when creating test {test_definition.test.__module__}.{test_definition.test.__name__}.",
                    f"If this is not a custom test implementation: {GITHUB_SUGGESTION}",
                ]
            )
            anta_log_exception(e, message, logger)
    if AntaTest.progress is not None:
        AntaTest.nrfu_task = AntaTest.progress.add_task("Running NRFU Tests...", total=len(coros))

    logger.info("Running ANTA tests...")
    test_results = await asyncio.gather(*coros)
    for r in test_results:
        manager.add_test_result(r)
    for device in devices:
        if device.cache_statistics is not None:
            logger.info(
                f"Cache statistics for '{device.name}': "
                f"{device.cache_statistics['cache_hits']} hits / {device.cache_statistics['total_commands_sent']} "
                f"command(s) ({device.cache_statistics['cache_hit_ratio']})"
            )
        else:
            logger.info(f"Caching is not enabled on {device.name}")
