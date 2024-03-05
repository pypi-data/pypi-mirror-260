"""24 port Nokia ONT hardware
    slot_port = '1/1'
    slots = {'1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8', '1/1/1/1/1/4': '4', '1/1/1/1/1/5': '4'}
"""


class SlotsPortsManager:
    """Process slots and ports
            received data should be something like this:
            24_ports = {'1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8', '1/1/1/1/1/4', '1/1/1/1/1/5'}
            16_ports = {'1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8'}
            16_ports_plus4 = {'1/1/1/3/10/1': '4', '1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8'}
            8_ports = {'1/1/3/10/1/1': '8'}
            4_ports = {'1/1/1/3/10/1': '4'}

    """
    def __init__(self, slots, slot_port):
        self.slots_dict = slots
        self.slot_port = slot_port
        self.slot_port_erros = f"""
        [ {self.slot_port} ] is not a valid slot/port value
        These are the valid slots [1, 3, 4, 5]
        These are the valid port [1-8]
        This is a slot/port example: 1/3
        """

    def get_target_port(self):
        """"""
        data = self.slots_dict
        print(data)
        if not self.slot_port:
            print(f"No slot/port value provided\n")
            print(f"These are the valid slots [1, 3, 4, 5]")
            print(f"These are the valid port values for slot1 and slot3 [1-8]\n\n")
            exit()

        slot1 = {}
        slot3 = {}
        slot4 = {}
        slot5 = {}
        for k, v in data.items():
            if k.endswith('1') and '8' in v:
                slot1[k] = v
            if k.endswith('3') and '8' in v:
                slot3[k] = v
            if k.endswith('4') and '4' in v:
                slot4[k] = v
            if k.endswith('5') and '4' in v:
                slot5[k] = v

        if self.slot_port:
            """
            {'1/1/1/1/1/1': '8', '1/1/1/1/1/3': '8', '1/1/1/1/1/4': '4', '1/1/1/1/1/5': '4'}
            
            ont-slot-idx : 1/1/1/1/1/1  act-num-data-ports : 8  act-num-voice-ports : 0   actual-card-type : ethernet  actual-ont-integ : integrated
            ont-slot-idx : 1/1/1/1/1/3  act-num-data-ports : 8  act-num-voice-ports : 0   actual-card-type : ethernet  actual-ont-integ : integrated
            ont-slot-idx : 1/1/1/1/1/4  act-num-data-ports : 4  act-num-voice-ports : 0   actual-card-type : ethernet  actual-ont-integ : integrated
            ont-slot-idx : 1/1/1/1/1/5  act-num-data-ports : 4  act-num-voice-ports : 0   actual-card-type : ethernet  actual-ont-integ : integrated
            """
            print(f"Slot_ports {self.slot_port}\n")
            print(f"Len of slot port {len(str(self.slot_port))}\n")

            if len(str(self.slot_port)) == 3:
                print(f"Yes {self.slot_port}")
                sl, _, port = list(self.slot_port)
                if str(sl).isnumeric() and str(port).isnumeric():
                    if int(sl) == 1:
                        # check if provided port is numeric
                        if str(port).isnumeric():
                            # check if provided port is in within the correct range
                            if int(port) in range(1, int(list(slot1.values())[0]) + 1):
                                target_port = f"{list(slot1.keys())[0]}/{port}"
                                return target_port
                            else:
                                print(f"\n[ {port} ] is no a valid port value for slot1")
                                print(f"These are the valid ports [1-8]\n")
                                exit()
                        else:
                            print(f"\n[ {sl} ] must be a numeric value")
                            print(f"These are the valid ports [1-8]\n")
                            exit()
                    elif int(sl) == 3:
                        # check if provided port is numeric
                        if str(port).isnumeric():
                            # check if provided port is in within the correct range
                            if int(port) in range(1, int(list(slot3.values())[0]) + 1):
                                target_port = f"{list(slot3.keys())[0]}/{port}"
                                return target_port
                            else:
                                print(f"\n[ {port} ] is no a valid port value for slot3")
                                print(f"These are the valid ports [1-8]\n")
                                exit()
                    elif int(sl) == 4:
                        # check if provided port is numeric
                        if str(port).isnumeric():
                            # check if provided port is in within the correct range
                            if int(port) in range(1, int(list(slot4.values())[0]) + 1):
                                target_port = f"{list(slot4.keys())[0]}/{port}"
                                return target_port
                            else:
                                print(f"\n[ {port} ] is no a valid port value for slot4")
                                print(f"These are the valid ports [1-4]\n")
                                exit()
                    elif int(sl) == 5:
                        # check if provided port is numeric
                        if str(port).isnumeric():
                            # check if provided port is in within the correct range
                            if int(port) in range(1, int(list(slot5.values())[0]) + 1):
                                target_port = f"{list(slot5.keys())[0]}/{port}"
                                return target_port
                            else:
                                print(f"\n[ {port} ] is no a valid port value for slot5")
                                print(f"These are the valid ports [1-4]\n")
                                exit()
                        else:
                            print(f"\n[ {sl} ] must be a numeric value")
                            print(f"These are the valid ports [1-8]\n")
                            exit()
                    else:
                        print(f"\n[ {self.slot_port} ] is not a valid slot value")
                        print(f"These are the valid slots [1, 3, 4, 5]\n")
                        exit()
                else:
                    print(self.slot_port_erros)
                    exit()
            else:
                print(self.slot_port_erros)
                exit()
        else:
            print(self.slot_port_erros)
            exit()


# HOW TO USE THIS MODULE
"""
slot_port = '1/1'
slots = {'1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8', '1/1/1/1/1/4': '4', '1/1/1/1/1/5': '4'}
target_port = SlotsPortsManager(slots, slot_port).get_target_port()
print(f"Target port: {target_port}")
print(f"Done")
"""
















#