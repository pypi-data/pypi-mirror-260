#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import UserList
from pathlib import Path

from mako.template import Template
from pkg_resources import resource_filename
from systemrdl import RDLListener
from systemrdl import RDLWalker
from systemrdl.node import AddrmapNode
from systemrdl.node import FieldNode
from systemrdl.node import RegfileNode
from systemrdl.node import RegNode
from systemrdl.node import RootNode

# from typing import List

# from typing import Any
# from typing import Optional
# from typing import Union


class Node(UserList):
    def __init__(self, node: AddrmapNode | RegfileNode | RegNode | FieldNode) -> None:
        self.node = node
        super().__init__()

    def __getattr__(self, item):
        return getattr(self.node, item)

    @property
    def name(self):
        return self.inst_name

    @property
    def path(self):
        return self.get_rel_path(
            self.owning_addrmap,
            hier_separator="_",
            array_suffix="_{index:d}",
        )


class Field(Node):
    @property
    def onread(self):
        return self.get_property("onread")

    @property
    def onwrite(self):
        return self.get_property("onwrite")

    @property
    def reset(self):
        return self.get_property("reset")

    @property
    def swmod(self):
        return self.get_property("swmod")

    def get_bit_slice(self):
        """Returns the"""
        if self.msb == self.lsb:
            return f"{self.msb}"
        else:
            return f"{self.msb}:{self.lsb}"

    def get_cpuif_bit_slice(self) -> str:
        """Returns the bit slice used by SW to access the field.

        In the simple case when (regwidth == accesswidth), this method returns the same
        string as self.get_bit_slice().  When (regwidth > accesswidth), then ...

        """
        accesswidth = self.parent.get_property("accesswidth")
        subreg_idx = self.msb // accesswidth
        msb = self.msb - (subreg_idx * accesswidth)
        lsb = self.lsb - (subreg_idx * accesswidth)
        if msb == lsb:
            return f"{msb}"
        else:
            return f"{msb}:{lsb}"


class Register(Node):
    @property
    def accesswidth(self):
        return self.get_property("accesswidth")

    @property
    def regwidth(self):
        return self.get_property("regwidth")

    @property
    def is_wide(self):
        return self.regwidth > self.accesswidth

    @property
    def addressinc(self):
        return self.accesswidth // 8

    @property
    def subregs(self) -> int:
        """Returns an int identifying how many sub-registers are present.

        If the regwidth is greater than the accesswidth, then the register is divided
        into a number of sub-registers that are accessed at different cpuif address.

        """
        return self.regwidth // self.accesswidth

    def get_subreg_fields(self, subreg: int):
        """Returns a list of fields that are present in a sub-register."""
        fields = []
        for f in self:
            if (f.msb // self.accesswidth) == subreg:
                fields.append(f)
        return fields


class RegisterFile(Node):
    pass


class AddressMap(Node):
    def get_registers(self) -> list[Register]:
        def get_child_regs(child, regs):
            if isinstance(child, (AddressMap, Field)):
                raise RuntimeError(
                    f"unexpected call to get_child_regs on object {child}",
                )
            elif isinstance(child, RegisterFile):
                for ch in child:
                    get_child_regs(ch, regs)
            elif isinstance(child, Register):
                regs.append(child)
            else:
                raise RuntimeError(f"unrecognised type: {type(child)}")

        registers = []
        for i, child in enumerate(self):
            get_child_regs(child, registers)
        return registers

    @property
    def addrwidth(self) -> int:
        return self.size.bit_length()

    @property
    def accesswidth(self) -> int:
        return min([reg.get_property("accesswidth") for reg in self.get_registers()])


class VerilogExporter(RDLListener):
    def __init__(self):
        self._active_node = []  # REVISIT: better name
        self.top = None

    @property
    def _current_node(self):
        return self._active_node[-1]

    def push(self, node: AddressMap | RegisterFile | Register):
        try:
            self._current_node.append(node)
        except IndexError:
            pass
        self._active_node.append(node)

    def pop(self) -> None:
        self.top = self._active_node.pop()

    def enter_Addrmap(self, node) -> None:
        self.push(AddressMap(node))

    def exit_Addrmap(self, node) -> None:
        self.pop()

    def enter_Regfile(self, node: RegfileNode) -> None:
        self.push(RegisterFile(node))

    def exit_Regfile(self, node: RegfileNode) -> None:
        self.pop()

    def enter_Reg(self, node: RegNode) -> None:
        self.push(Register(node))

    def exit_Reg(self, node: RegNode) -> None:
        self.pop()

    def enter_Field(self, node: FieldNode) -> None:
        self.push(Field(node))

    def exit_Field(self, node: FieldNode) -> None:
        self.pop()

    def export(self, node: RootNode | AddrmapNode, options: argparse.Namespace) -> None:
        if isinstance(node, RootNode):
            node = node.top

        RDLWalker(unroll=True).walk(node, self)

        outpath = Path(options.output)
        if not outpath.exists():
            outpath.mkdir(parents=True, exist_ok=True)

        reg_pkg_path = outpath / f"{node.inst_name}_reg_pkg.sv"
        reg_top_path = outpath / f"{node.inst_name}_reg_top.sv"

        reg_top_tpl = Template(
            filename=resource_filename("peakrdl_sv", "reg_top.sv.tpl"),
        )
        with reg_top_path.open("w") as f:
            f.write(reg_top_tpl.render(block=self.top))

        reg_pkg_tpl = Template(
            filename=resource_filename("peakrdl_sv", "reg_pkg.sv.tpl"),
        )
        with reg_pkg_path.open("w") as f:
            f.write(reg_pkg_tpl.render(block=self.top))
