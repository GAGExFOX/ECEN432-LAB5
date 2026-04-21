import math
import numpy as np
import matplotlib.pyplot as plt

v_fs = 1.0


# 2.5 Bit Sub Flash ADC with 1-Bit Redundancy
class SubFlashADC2_5Bit:
	def __init__(self, v_fs=1.0, v_os_list=None, a1=0, a2=0, a3=0):
		"""
		Initializes the 2.5-bit ADC with 6 reference levels.
		Assumes a single-ended input range from 0 to v_fs.
		"""
		self.v_fs = v_fs
		
		# Ideal Voltage Thresholds
		self.ideal_thresholds = np.array([3/16, 5/16, 7/16, 9/16, 11/16, 13/16]) * self.v_fs
		
		# Apply Offset Errors to the thresholds
		if v_os_list is None:
			self.v_os_list = np.zeros(6)
		else:
			self.v_os_list = np.array(v_os_list)
			
		self.actual_thresholds = self.ideal_thresholds + self.v_os_list
		
		# Store non-linearities
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3

	def quantize(self, v_in):
		"""
		Compares the input voltage against the thresholds.
		Returns the thermometer code and the encoded digital integer.
		"""
		# Apply gain and non-linearities to the input voltage
		v_eff = (1 + self.a1)*v_in + self.a2*(v_in**2) + self.a3*(v_in**3)
		
		# Compare effective voltage against actual shifted thresholds
		thermometer_code = [1 if v_eff >= th else 0 for th in self.actual_thresholds]
		return sum(thermometer_code)

#  - - - MAIN CODE - - -
if __name__ == "__main__":
	# Initialize the ADC with a 1V full-scale range
	adc = SubFlashADC2_5Bit(v_fs)

	# Ramp from 0 to VFS=1.0 V of test voltages
	test_voltages = np.arange(0, 1, 0.01)
	dig_code_vals = []
	quantization_error = []

	# Quantize values through ADC and convert to 3-Bit Binary Output
	for v in test_voltages:
		digital_code = adc.quantize(v)
		dig_code_vals.append(bin(digital_code).replace("0b", ""))
		
		# Calculate Error
		voltage_level = ((digital_code + 1) / 8) * v_fs
		error = v - voltage_level
		quantization_error.append(error)
		

	# Plotting Characteristic Graph of 2.5-Bit Sub Flash ADC with 1-Bit Redundancy
	plt.figure(figsize=(8, 5))
	plt.step(test_voltages, dig_code_vals, where='post', linewidth=2, color='blue')
	plt.title('2.5-Bit Sub-Flash ADC Transfer Characteristic')
	plt.xlabel('Analog Input Voltage (V)')
	plt.ylabel('Digital Output Code')
	plt.yticks(range(7)) 
	plt.grid(True, linestyle='--', alpha=0.7)
	plt.show()
	
	# Plotting Quantization Error as Function of Vin
	plt.figure(figsize=(8, 5))
	plt.plot(test_voltages, quantization_error, linewidth=2, color='blue')
	plt.title('2.5-Bit Sub-Flash ADC Quantization Error vs Vin')
	plt.xlabel('Analog Input Voltage (V)')
	plt.ylabel('Quantization Error (V)')
	plt.grid(True, linestyle='--', alpha=0.7)
	plt.show()
	print(f"Max Error = {max(quantization_error)} and Min Error = {min(quantization_error)}")
	
	
	# Creating Non-Ideal Transfer Characteristic Graphs of 2.5-Bit Sub Flash ADC with 1-Bit Redundancy
	plt.figure(figsize=(8, 5))
	for num in range(0, 100):
		np.random.seed((num+1)*3)
		voltage_offsets = np.random.uniform(low=-0.02, high=0.02, size=6)
		gain_errors = np.random.uniform(low=-0.03, high=0.03, size=3)
		
		# Create non-ideal ADC object
		adc = SubFlashADC2_5Bit(v_fs, v_os_list=voltage_offsets, a1=gain_errors[0], a2=gain_errors[1], a3=gain_errors[2])
		
		test_voltages = np.arange(0, 1, 0.01)
		dig_code_vals = []
		quantization_error = []

		for v in test_voltages:
			digital_code = adc.quantize(v)
			dig_code_vals.append(bin(digital_code).replace("0b", ""))
			
		# Plot single step graph over 100 loops
		plt.step(test_voltages, dig_code_vals, where='post', linewidth=2, color='blue', alpha=0.2)
	
	# Create original function to plot over all graphs
	adc = SubFlashADC2_5Bit(v_fs)

	test_voltages = np.arange(0, 1, 0.01)
	dig_code_vals = []
	quantization_error = []
	
	for v in test_voltages:
		digital_code = adc.quantize(v)
		dig_code_vals.append(bin(digital_code).replace("0b", ""))
		
	# Plot all 100 loops and original function
	plt.step(test_voltages, dig_code_vals, where='post', linewidth=2, color='red')
	plt.title('2.5-Bit Sub-Flash ADC Transfer Characteristic')
	plt.xlabel('Analog Input Voltage (V)')
	plt.ylabel('Digital Output Code')
	plt.yticks(range(7)) 
	plt.grid(True, linestyle='--', alpha=0.7)
	plt.show()
	
	
	DNLs = [0, 0, 0, 0, 0, 0]
	# Calculating DNL and INL of Voltage Offsets
	for num in range(0, 100):
		np.random.seed((num+1)*3)
		voltage_offsets = np.random.uniform(low=-0.02, high=0.02, size=6)
		
		# Create non-ideal ADC object
		adc = SubFlashADC2_5Bit(v_fs, v_os_list=voltage_offsets)
		
		test_voltages = np.arange(0, 1, 0.001)
		dig_code_vals = []
		quantization_error = []


		bucket_start = 0
		bucket_end = 0
		prev_digital_code = 0
		k = 0
		for v in test_voltages:
			digital_code = adc.quantize(v)
			dig_code_vals.append(bin(digital_code).replace("0b", ""))
			
			if digital_code > prev_digital_code:
				bucket_end = v
				DNLs[k] += ((bucket_end-bucket_start) - 0.125) / 0.125
				bucket_start = v
				k += 1
				
			prev_digital_code = digital_code
			
for i, num in enumerate(DNLs):
	DNLs[i] = DNLs[i] / 100
	print(DNLs[i])

INL = sum(DNLs)
print(f"INL = {INL}")
