from pal.model.access_mechanism import AbstractAccessMechanism
from dataclasses import dataclass

@dataclass()
class MCRR(AbstractAccessMechanism):
    """ Access mechanism for writing a coprocessor register using two """
    """ general purpose registers """

    coproc: bytes = 0
    """ Coprocessor number """

    opc1: bytes = 0
    """ Coprocessor-specific opcode """

    crm: bytes = 0
    """ Operational register """

    rt1: bytes = 0b0
    """ Source general purpose register 1 (default = r0) """

    rt2: bytes = 0b1
    """ Source general purpose register 2 (default = r1) """

    name: str = "mcrr"
    """ The name of this access mechanism """

    def is_read(self):
        return False

    def is_write(self):
        return True

    def is_memory_mapped(self):
        return False

    def is_valid(self):
        if self.rt1 > 0b1110: return False
        if self.rt2 > 0b1110: return False
        if self.coproc > 0b1111: return False
        if self.opc1 > 0b111: return False
        if self.crm > 0b1111: return False

        return True

    def binary_encoded(self):
        raise NotImplementedError()
