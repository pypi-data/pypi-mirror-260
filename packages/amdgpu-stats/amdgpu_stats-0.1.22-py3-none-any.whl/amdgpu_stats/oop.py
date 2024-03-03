class AMDGPU:
    def __init__(self, name, core_clock, mem_clock, util_pct, voltage, pwr_con, pwr_lim_cur, pwr_lim_def, pwr_capability, fan_rpm, temp_edge, temp_junction, temp_mem):
        self.name = name
        self.core_clock = core_clock
        self.mem_clock = mem_clock
        self.util_pct = util_pct
        self.voltage = voltage
        self.pwr_con = pwr_con
        self.pwr_lim_cur = pwr_lim_cur
        self.pwr_lim_def = pwr_lim_def
        self.pwr_capability = pwr_capability
        self.fan_rpm = fan_rpm
        self.temp_edge = temp_edge
        self.temp_junction = temp_junction
        self.temp_mem = temp_mem
