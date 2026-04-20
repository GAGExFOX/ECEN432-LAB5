
class SubFlashADC2_5Bit:
    def __init__(self, v_fs=1.0):
        """
        Initializes the 2.5-bit ADC with 6 reference levels.
        Assumes a single-ended input range from 0 to v_fs.
        """
        self.v_fs = v_fs
        
        # The 6 thresholds: 3/16, 5/16, 7/16, 9/16, 11/16, 13/16 of V_FS
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
        # 1. Generate the Thermometer Code (list of 1s and 0s)
        # If Vin is greater than the threshold, the comparator outputs a 1.
        thermometer_code = [1 if v_in >= th else 0 for th in self.thresholds]
        
        # 2. Encode to a Digital Value
        # Summing a thermometer code gives you the integer region (0 through 6)
        digital_out = sum(thermometer_code)
        
        return thermometer_code, digital_out

# ==========================================
# Example Usage and Testing
# ==========================================
if __name__ == "__main__":
    # Initialize the ADC with a 1V full-scale range
    adc = SubFlashADC2_5Bit(v_fs=1.0)
    
    # Test a few different input voltages
    test_voltages = [0.1, 0.25, 0.5, 0.75, 0.9]
    
    print(f"ADC Thresholds: {[round(th, 4) for th in adc.thresholds]}\n")
    print(f"{'Input (V)':<12} | {'Thermometer Code':<20} | {'Digital Out'}")
    print("-" * 50)
    
    for v in test_voltages:
        t_code, d_out = adc.quantize(v)
        # Format thermometer code as a string for easy reading
        t_str = "".join(map(str, t_code))
        print(f"{v:<12} | {t_str:<20} | {d_out}")
