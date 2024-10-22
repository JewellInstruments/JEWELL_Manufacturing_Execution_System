import time
from system import serial_protocols

res_channels = 12
volt_channels = 8
scans = 5
meas = {
    "GND": 0,
    "mems_X": 1,
    "mems_Y": 2,
    "mems_Z": 3,
    "mems_T": 4,
    "PWR+": 5,
    "VCC": 6,
    "PWR-": 7,
    "R_bias_X": 8,
    "R_offset_X": 9,
    "R_gnd_X": 10,
    "R_scale_X": 11,
    "R_bias_Y": 12,
    "R_offset_Y": 13,
    "R_gnd_Y": 14,
    "R_scale_Y": 15,
    "R_bias_Z": 16,
    "R_offset_Z": 17,
    "R_gnd_Z": 18,
    "R_scale_Z": 19,
}

def Ruby_Scan_Voltage(daq, supply):
    #turn power supply on
    serial_protocols.serial_write(supply, "OUTP CH1, ON")
    serial_protocols.serial_write(supply, "OUTP CH2, ON")
    serial_protocols.serial_write(supply, "APPL CH1,15,.3")
    serial_protocols.serial_write(supply, "APPL CH2,15,.3")
    #create voltage scan with .1 sec delay btw channels, repeat scan 5 times
    serial_protocols.serial_write(daq, "SENS:FUNC 'VOLT', (@101:108)")
    serial_protocols.serial_write(daq, "ROUT:DEL .1, (@101:108)")
    serial_protocols.serial_write(daq, "ROUT:SCAN:COUN:SCAN " + str(scans))
    serial_protocols.serial_write(daq, "ROUT:SCAN:CRE (@101:108)")
    serial_protocols.serial_write(daq, "INIT")
    #approximately 1 secs per scan to complete, this is for pyvisa timeouts
    time.sleep(1*scans)
    serial_protocols.serial_write(daq, "*WAI")
    serial_protocols.serial_write(daq, "ROUT:OPEN:ALL")
    #turn power supply off
    serial_protocols.serial_write(supply, "OUTP CH1, OFF")
    serial_protocols.serial_write(supply, "OUTP CH2, OFF")
    serial_protocols.serial_write(supply, "APPL CH1,0,.3")
    serial_protocols.serial_write(supply, "APPL CH2,0,.3")
    #get start and end of data buffer
    buffer_start = serial_protocols.serial_write_read(daq, ":TRAC:ACT:STAR?")
    buffer_start = buffer_start.strip("\n")
    buffer_end = serial_protocols.serial_write_read(daq, ":TRAC:ACT:END?")
    buffer_end = buffer_end.strip("\n")
    #put data in the buffer, convert to float
    list = serial_protocols.serial_write_read(daq, ":TRAC:DATA? " + buffer_start + ", " + buffer_end + ", \"defbuffer1\", READ")
    list = list.split(",")
    for item in range(0, len(list)):
        list[item] = float(list[item])
    
    return list

def Ruby_Scan_Resistance(daq, supply):
    #make sure power supply is off
    serial_protocols.serial_write(supply, "OUTP CH1, OFF")
    serial_protocols.serial_write(supply, "OUTP CH2, OFF")
    #create resistance scan with .1 sec delay btw channels, repeat scan 5 times
    serial_protocols.serial_write(daq, "SENS:FUNC 'RES', (@109:120)")
    serial_protocols.serial_write(daq, "ROUT:DEL .1, (@109:120)")
    serial_protocols.serial_write(daq, "ROUT:SCAN:COUN:SCAN " + str(scans))
    serial_protocols.serial_write(daq, "ROUT:SCAN:CRE (@109:120)")
    serial_protocols.serial_write(daq, "INIT")
    #approximately 1.6 secs per scan to complete, this is for pyvisa timeouts
    time.sleep(1.6*scans)
    serial_protocols.serial_write(daq, "*WAI")
    serial_protocols.serial_write(daq, "ROUT:OPEN:ALL")
    #get start and end of data buffer
    buffer_start = serial_protocols.serial_write_read(daq, ":TRAC:ACT:STAR?")
    buffer_start = buffer_start.strip("\n")
    buffer_end = serial_protocols.serial_write_read(daq, ":TRAC:ACT:END?")
    buffer_end = buffer_end.strip("\n")
    #put data in the buffer, convert to float
    list = serial_protocols.serial_write_read(daq, ":TRAC:DATA? " + buffer_start + ", " + buffer_end + ", \"defbuffer1\", READ")
    list = list.split(",")
    for item in range(0, len(list)):
        list[item] = float(list[item])
    return list

#function to measure over 20 channels of the DMM used for the RUBY bed of nails
def Ruby_calibration_measurement():
    #talk to the daq and power supply
    daq = serial_protocols.serial_open("TCPIP::192.168.2.74::inst0::INSTR")
    supply = serial_protocols.serial_open("TCPIP::192.168.2.57::INSTR")
    print(serial_protocols.serial_write_read(daq, "*IDN?"))
    print(serial_protocols.serial_write_read(supply, "*IDN?"))
    serial_protocols.serial_write(daq, "*RST")
    serial_protocols.serial_write(daq, "FORM:ASC:PREC 5")
    
    #scan channels for voltage and resistance measurements
    res_list = Ruby_Scan_Resistance(daq, supply)
    volt_list = Ruby_Scan_Voltage(daq, supply)
    res_array = []
    volt_array = []
    #average out the scans and put data into arrays
    for i in range(res_channels):
        col = []
        for j in range(scans):
            col.append(res_list[i+j*res_channels])
        res_array.append(sum(col) / len(col))
    
    for i in range(volt_channels):
        col = []
        for j in range(scans):
            col.append(volt_list[i+j*volt_channels])
        volt_array.append(sum(col) / len(col))
    
    #clear daq buffer and close out devices
    serial_protocols.serial_write(daq, ":TRAC:CLE")
    serial_protocols.serial_close(daq)
    serial_protocols.serial_close(supply)

    #output returns the channels (101-120) in order with value labels
    temp = volt_array + res_array
    for key, value in meas.items():
        meas[key] = temp[value]
    return (meas)