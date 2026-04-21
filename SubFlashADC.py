import math
import numpy as np
import matplotlib.pyplot as plt

v_fs = 1.0


# 2.5 Bit Sub Flash ADC with 1-Bit Redundancy
class SubFlashADC2_5Bit:
    def __init__(self, v_fs=1.0):
        """
        Initializes the 2.5-bit ADC with 6 reference levels.
        Assumes a single-ended input range from 0 to v_fs.
        """
        self.v_fs = v_fs
        
        # Voltage Thresholds
        self.thresholds = [
            (3/16) * self.v_fs,  # 0.1875V
            (5/16) * self.v_fs,  # 0.3125V
            (7/16) * self.v_fs,  # 0.4375V
            (9/16) * self.v_fs,  # 0.5625V
            (11/16) * self.v_fs, # 0.6875V
            (13/16) * self.v_fs  # 0.8125V
        ]

    def quantize(self, v_in):
        """
        Compares the input voltage against the thresholds.
        Returns the thermometer code and the encoded digital integer (0 to 6).
        """
        # Generate list holding each comparator output of the thermometer code
        thermometer_code = [1 if v_in >= th else 0 for th in self.thresholds]
        
        # Summation to get digital output of thermometer code
        digital_out = sum(thermometer_code)
        
        return thermometer_code, digital_out

#  - - - MAIN CODE - - -
if __name__ == "__main__":
    # Initialize the ADC with a 1V full-scale range
    adc = SubFlashADC2_5Bit(v_fs)
    
    # Ramp from 0 to VFS=1.0 V of test voltages
    test_voltages = np.arange(0, 1, 0.01)
    dig_code_vals = []

	# Quantize values through ADC and convert to 3-Bit Binary Output
    for v in test_voltages:
        therm_code, digital_code = adc.quantize(v)
        dig_code_vals.append(bin(digital_code).replace("0b", ""))

	# Plotting Characteristic Graph of 2.5-Bit Sub Flash ADC with 1-Bit Redundancy
    plt.figure(figsize=(8, 5))
    plt.step(test_voltages, dig_code_vals, where='post', linewidth=2, color='blue')
    plt.title('2.5-Bit Sub-Flash ADC Transfer Characteristic')
    plt.xlabel('Analog Input Voltage (V)')
    plt.ylabel('Digital Output Code')
    plt.yticks(range(7)) 
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.show()
