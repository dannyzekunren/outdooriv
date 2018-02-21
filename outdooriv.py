# Keithley IV Sweep for 2400 SourceMeter
# Import Pyplot, NumPy, and SciPy
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
# Variable intake and assignment
import sys
startv = 0
stopv = 0.75
stepv = 0.01

startvprime = float(startv)
stopvprime = float(stopv)
stepvprime = float(stepv)
steps = (stopvprime - startvprime) / stepvprime

# Import PyVisa and choose GPIB Channel 25 as Drain-Source
import visa
rm = visa.ResourceManager()
rm.list_resources()
Keithley = rm.open_resource('GPIB0::24::INSTR')
Keithley.write("*RST")
Keithley.timeout = 25000

# Turn off concurrent functions and set sensor to current with fixed voltage
Keithley.write(":SENS:FUNC:CONC OFF")
Keithley.write(":SOUR:FUNC VOLT")
Keithley.write(":SENS:FUNC 'CURR:DC' ")

# Voltage starting, ending, and spacing values based on input
Keithley.write(":SOUR:VOLT:STAR ", startv)
Keithley.write(":SOUR:VOLT:STOP ", str(stopv))
Keithley.write(":SOUR:VOLT:STEP ", str(stepv))
Keithley.write(":SOUR:SWE:RANG AUTO")

# Set compliance current (in A), sweep direction, and data acquisition
Keithley.write(":SENS:CURR:PROT 1")
Keithley.write(":SOUR:SWE:SPAC LIN")
Keithley.write(":SOUR:SWE:POIN ", str(int(steps)))
Keithley.write(":SOUR:SWE:DIR UP")
Keithley.write(":TRIG:COUN ", str(int(steps)))
Keithley.write(":FORM:ELEM CURR")

# Set sweep mode and turn output on
Keithley.write(":SOUR:VOLT:MODE SWE")
Keithley.write(":OUTP ON")



# Initiate sweep, collect ACSII current values, and turn output off
timestep =30 #interval for iv sweep
for i in range(1000):
    starttime = time.time() #start time
    result = Keithley.query(":READ?")
    yvalues = Keithley.query_ascii_values(":FETC?")
    Keithley.write(":OUTP OFF")
    Keithley.write(":SOUR:VOLT 0")
    # Create xvalues array and calculate conductance
    xvalues = np.arange(startvprime,stopvprime,stepvprime)
    #slope, intercept, r_value, p_value, std_error = stats.linregress(xvalues, yvalues)
    # Plot values and output conductance to command line
    plt.plot(xvalues,yvalues)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title('IV Curve')
    plt.show()

    filename = 'test1'+str(timestep*i)
    np.savetxt(filename, (xvalues,yvalues))
    endtime= time.time()
    elapsed = startime- endtime
    waittime = timestep-elapsed
    time.sleep (waittime)
    i=i+1
