import pal.gadget
from pal.config import config


class Cxx11RegisterAccessorWriter():

    def declare_register_accessors(self, outfile, register):
        self._declare_register_constants(outfile, register)

        if register.is_readable():
            self._declare_register_get(outfile, register)
        if register.is_writeable():
            self._declare_register_set(outfile, register)

    def call_register_get(self, outfile, register, destination, index="index"):
        call = "auto {dest} = {read}({index});".format(
            dest=destination,
            read=self._register_read_function_name(register),
            index=str(index) if register.is_indexed else ""
        )
        outfile.write(call)
        self.write_newline(outfile)

    # -------------------------------------------------------------------------
    # private
    # -------------------------------------------------------------------------

    def _declare_register_constants(self, outfile, register):
        self._declare_string_constant(outfile, "name", register.name.lower())
        self.write_newline(outfile)

        if register.long_name:
            self._declare_string_constant(outfile, "long_name", register.long_name)
            self.write_newline(outfile)

        if register.access_mechanisms.get("rdmsr"):
            addr = register.access_mechanisms["rdmsr"][0].address
            self._declare_hex_integer_constant(outfile, "address", addr)
            self.write_newline(outfile)

        if register.access_mechanisms.get("ldr"):
            offset = register.access_mechanisms["ldr"][0].offset
            self._declare_hex_integer_constant(outfile, "offset", offset)
            self.write_newline(outfile)
        elif register.access_mechanisms.get("str"):
            offset = register.access_mechanisms["str"][0].offset
            self._declare_hex_integer_constant(outfile, "offset", offset)
            self.write_newline(outfile)
        elif register.access_mechanisms.get("vmread"):
            encoding = register.access_mechanisms["vmread"][0].encoding
            self._declare_hex_integer_constant(outfile, "encoding", encoding)
            self.write_newline(outfile)
        elif register.access_mechanisms.get("vmwrite"):
            encoding = register.access_mechanisms["vmwrite"][0].encoding
            self._declare_hex_integer_constant(outfile, "encoding", encoding)
            self.write_newline(outfile)


        self.write_newline(outfile)

    def _declare_register_get(self, outfile, register):
        gadget = self.gadgets["pal.cxx.function_definition"]
        gadget.name = config.register_read_function
        gadget.return_type = self._register_size_type(register)
        gadget.args = []

        if register.is_indexed:
            gadget.args = [("uint32_t", "index")]
            gadget.name = gadget.name + "_at_index"

        self._declare_register_get_details(outfile, register)

    @pal.gadget.cxx.function_definition
    def _declare_register_get_details(self, outfile, register):
        for am_key, am_list in register.access_mechanisms.items():
            for am in am_list:
                if am.is_read():
                    size_type = self._register_size_type(register)
                    self._declare_variable(outfile, "value", 0, [size_type])

                    if am.is_memory_mapped():
                        addr_calc = str(am.component) + '_base_address() + offset'
                        if register.is_indexed:
                            addr_calc += " + (index * sizeof(" + size_type + "))"

                        self._declare_variable(outfile, "address", addr_calc,
                                               keywords=[size_type])

                    self.call_readable_access_mechanism(
                        outfile, register, am, "value"
                    )
                    outfile.write("return value;")
                    return

    def _declare_register_set(self, outfile, register):
        size_type = self._register_size_type(register)
        gadget = self.gadgets["pal.cxx.function_definition"]
        gadget.name = config.register_write_function
        gadget.return_type = "void"
        gadget.args = [(size_type, "value")]

        self._declare_register_set_details(outfile, register)

    @pal.gadget.cxx.function_definition
    def _declare_register_set_details(self, outfile, register):
        for am_key, am_list in register.access_mechanisms.items():
            for am in am_list:
                if am.is_write():
                    if am.is_memory_mapped():
                        size_type = self._register_size_type(register)
                        addr_calc = str(am.component) + '_base_address() + offset'
                        if register.is_indexed:
                            addr_calc += " + (index * sizeof(" + size_type + "))"

                        self._declare_variable(outfile, "address", addr_calc,
                                               keywords=[size_type])

                    self.call_writable_access_mechanism(
                        outfile, register, am, "value"
                    )
                    return