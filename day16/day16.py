#!/usr/bin/env python3

from math import prod

file = open('day16/input.txt')
hexinput = file.read()
file.close()
input_binary_string = bin(int(hexinput, 16))[2:].zfill(len(hexinput)*4)

VERSION_NUMBER_BITS = 3
TYPE_ID_BITS = 3
CONTENT_OFFSET = VERSION_NUMBER_BITS + TYPE_ID_BITS
TYPE_ID_FOR_LITERAL_VALUES = 4
LITERAL_VALUE_SIZE = 5

class Packet:
    def __init__(self, bin_string: str) -> None:
        self.bin_string = bin_string
        self.immediate_sub_packets = []
        self.version_number = int(self.bin_string[:VERSION_NUMBER_BITS], 2)
        """first three bits: version number"""
        self.type_id = int(self.bin_string[VERSION_NUMBER_BITS : VERSION_NUMBER_BITS + TYPE_ID_BITS], 2)
        """next three bits: packet type ID"""
        self.content = self.bin_string[CONTENT_OFFSET:]
        """all remaining bits: packet content"""
        self.has_sub_packets = self.type_id != TYPE_ID_FOR_LITERAL_VALUES
        """type ID 4 directly contains a literal value, every other type id is an operator with sub-packets"""
        self.value, self.consumed_bits = None, CONTENT_OFFSET

        if self.has_sub_packets:
            self.__split_into_sub_packets()
        else:
            self.__calc_literal_value()

    def __calc_literal_value(self):
        """Calculates the literal value of the packet content.
        
        Reads all groups of five bits until such a group starts with a zero which marks the last group to consider.
        Of each group, the four bits after the first one are snippets of the binary number representing the packet's content value.
        """
        read_index, value = 0, 0
        while True:
            current = self.content[read_index : read_index + LITERAL_VALUE_SIZE]
            value = (value << 4) + int(current[1:], 2)
            read_index += LITERAL_VALUE_SIZE
            if int(current[0]) == 0: break
        self.value = value
        self.consumed_bits += read_index

    def __split_into_sub_packets(self, read_index=0):
        length_type_id = int(self.content[0], 2)
        number_of_sub_packets_decides, length_of_sub_packets_decides = False, False
        if (length_type_id):
            """'1' means next 11 bits are number of sub-packets immediately contained"""
            magic_size_field_length = 11
            number_of_sub_packets_decides = True
        else:
            """'0' means next 15 bits as number represent total length (of all sub-packets) in bits"""
            magic_size_field_length = 15
            length_of_sub_packets_decides = True
        magic_number_length_or_count = int(self.content[1 : 1+ magic_size_field_length], 2)

        sub_contents = self.content[1 + magic_size_field_length :]

        while True:
            ganz_neues_packet = Packet(sub_contents[read_index:])

            self.immediate_sub_packets.append(ganz_neues_packet)
            read_index += ganz_neues_packet.consumed_bits                

            if (
                (number_of_sub_packets_decides and len(self.immediate_sub_packets) >= magic_number_length_or_count)
                or (length_of_sub_packets_decides and read_index >= magic_number_length_or_count)
            ): break

        self.consumed_bits += 1 + magic_size_field_length + sum([sub.consumed_bits for sub in self.immediate_sub_packets])

    def get_sum_of_all_version_numbers(self, print_all=False):
        if print_all: print("version is", self.version_number)
        if not self.has_sub_packets:
            return self.version_number
        temp_sum = self.version_number
        for sub_packet in self.immediate_sub_packets:
            temp_sum += sub_packet.get_sum_of_all_version_numbers(print_all)
        return temp_sum

    def calculate_special_value(self):
        switch = {
            0: lambda subs: sum(subs),
            1: lambda subs: prod(subs),
            2: lambda subs: min(subs),
            3: lambda subs: max(subs),
            4: lambda subs: self.value,
            5: lambda subs: subs[0] > subs[1],
            6: lambda subs: subs[0] < subs[1],
            7: lambda subs: subs[0] == subs[1]
        }
        return int(switch.get(self.type_id)(
            [sub.calculate_special_value()
            for sub in self.immediate_sub_packets]
            ))

def test1():
    testinput = [
        ("D2FE28", "value 2021", lambda p: p.value),
        ("38006F45291200", "version 1, type ID 6", lambda p: "version %d, type ID %d" % (p.version_number, p.type_id)),
        ("EE00D40C823060", "version 7, type ID 3", lambda p: "version %d, type ID %d" % (p.version_number, p.type_id)),
        ("8A004A801A8002F478", "version 4 containing v1 cont. v5 cont. value with v6, sum 16",
            lambda p: "version %d, containing %d ..." % (p.version_number, p.immediate_sub_packets[0].version_number)),
        ("620080001611562C8802118E34", "version 3 containing two packets with value packets, sum 12",
            lambda p: "version %d, containing %d packets, sum %d" %
            (p.version_number, len(p.immediate_sub_packets), p.get_sum_of_all_version_numbers())),
        ("C0015000016115A2E0802F182340", "sum 23", lambda p: "sum %d" % p.get_sum_of_all_version_numbers()),
        ("A0016C880162017C3686B18A3D4780", "sum 31", lambda p: "sum %d" % p.get_sum_of_all_version_numbers())
    ]
    for hex, expect, compare in testinput:
        print("\n# TEST 1 '%s' should find '%s'" % (hex, expect))
        packet = Packet(bin(int(hex, 16))[2:].zfill(len(hex)*4))
        print(compare(packet))

def part1():
    packet = Packet(input_binary_string)
    print("\npart1 %s\nsum of all version numbers: %d" % ('#'*80, packet.get_sum_of_all_version_numbers()))
    
def test2():
    testinput = {
        "C200B40A82": "3 (1 + 2)",
        "04005AC33890": "54 (6 * 9)",
        "880086C3E88112": "7 (min of 7, 8, 9)",
        "CE00C43D881120": "9 (max of 7, 8, 9)",
        "D8005AC2A8F0": "1 (5 lss 15)",
        "F600BC2D8F": "0 (5 not gtr 15)",
        "9C005AC2F8F0": "0 (5 neq 15)",
        "9C0141080250320F1802104A08": "1 (1 + 3 == 2 * 2)"
    }
    for hex, check in testinput.items():
        print("\n# TEST 2 '%s' should find '%s'" % (hex, check))
        binary_string = bin(int(hex, 16))[2:].zfill(len(hex)*4)
        packet = Packet(binary_string)
        print(packet.calculate_special_value())

def part2():
    packet = Packet(input_binary_string)
    print("\npart2 %s\ncalculated special value: %d" % ('#'*80, packet.calculate_special_value()))

# test1()
part1()
# test2()
part2()
