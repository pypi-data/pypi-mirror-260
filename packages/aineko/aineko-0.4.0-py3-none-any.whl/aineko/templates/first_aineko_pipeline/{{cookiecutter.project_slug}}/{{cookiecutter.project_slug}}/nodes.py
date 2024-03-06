# Copyright 2023 Aineko Authors
# SPDX-License-Identifier: Apache-2.0
"""Example file showing how to create nodes."""

import time
from typing import Optional

from aineko.core.node import AbstractNode


class MySequencerNode(AbstractNode):
    """Example node."""

    def _pre_loop_hook(self, params: Optional[dict] = None) -> None:
        """Optional; used to initialize node state."""
        self.current_val = params.get("initial_state", 0)

    def _execute(self, params: Optional[dict] = None) -> Optional[bool]:
        """Required; function repeatedly executes.

        Accesses inputs via `self.inputs`, and outputs via
        `self.outputs`.
        Logs can be sent via the `self.log` method.
        """
        self.current_val += params.get("increment", 1)
        time.sleep(5)
        self.outputs["test_sequence"].write(self.current_val)


class PrintInput(AbstractNode):
    """Prints input."""

    def _execute(self, params: Optional[dict] = None):
        for dataset, input_value in self.inputs.items():
            msg = input_value.read(how="next")
            if msg is None:
                continue
            print(
                f"Node {params['name']} received message: {msg['message']} from {dataset}"
            )


class MySumNode(AbstractNode):
    """Example node."""

    def _pre_loop_hook(self, params: Optional[dict] = None) -> None:
        """Optional; used to initialize node state."""
        self.state = params.get("initial_state", 0)

    def _execute(self, params: Optional[dict] = None) -> Optional[bool]:
        """Required; function repeatedly executes.

        Accesses inputs via `self.inputs`, and outputs via
        `self.outputs`.
        Logs can be sent via the `self.log` method.
        """
        msg = self.inputs["test_sequence"].read(how="next")
        if msg is None:
            return
        self.log(f"Received: {msg['message']}. Adding {params['increment']}...")
        self.state = int(msg["message"]) + int(params["increment"])
        self.outputs["test_sum"].write(self.state)
