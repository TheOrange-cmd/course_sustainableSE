import sys
import clr

def run_diagnostics():
    """
    Connects to LibreHardwareMonitor and prints a detailed tree of all
    detected hardware, sub-hardware, and their sensors.
    """
    try:
        # Adjust this path if your DLL is located elsewhere
        dll_path = "C:\\Users\\danie\\AppData\\Local\\Microsoft\\WinGet\\Packages\\LibreHardwareMonitor.LibreHardwareMonitor_Microsoft.Winget.Source_8wekyb3d8bbwe\\LibreHardwareMonitorLib.dll"
        clr.AddReference(dll_path)
    except Exception as e:
        print(f"Error adding DLL reference. Ensure the path is correct: {e}")
        print("Please adjust the 'dll_path' variable in the script.")
        sys.exit(1)

    from LibreHardwareMonitor import Hardware

    computer = Hardware.Computer()
    computer.IsCpuEnabled = True
    computer.IsGpuEnabled = True
    computer.IsMemoryEnabled = True
    computer.IsMotherboardEnabled = True
    computer.IsStorageEnabled = True
    
    print("Opening LibreHardwareMonitor handle for diagnostics...")
    computer.Open()
    print("-" * 50)

    # Allow some time for sensors to initialize
    import time
    time.sleep(2)

    for hw in computer.Hardware:
        # This is crucial! You must call Update() on the hardware to get new readings.
        hw.Update()
        print(f"[Hardware] Name: '{hw.Name}', Type: '{hw.HardwareType}'")

        # --- Print Direct Sensors on this Hardware ---
        if hw.Sensors:
            for sensor in hw.Sensors:
                print(f"  [-> Sensor] Name: '{sensor.Name}', Type: '{sensor.SensorType}', Value: {sensor.Value}")
        else:
            print("  (No direct sensors on this hardware item)")

        # --- IMPORTANT: Check for Sub-Hardware ---
        if hw.SubHardware:
            for sub_hw in hw.SubHardware:
                sub_hw.Update()
                print(f"  [Sub-Hardware] Name: '{sub_hw.Name}', Type: '{sub_hw.HardwareType}'")
                
                # --- Print Sensors on the Sub-Hardware ---
                if sub_hw.Sensors:
                    for sensor in sub_hw.Sensors:
                        print(f"    [-> Sensor] Name: '{sensor.Name}', Type: '{sensor.SensorType}', Value: {sensor.Value}")
                else:
                    print("    (No sensors on this sub-hardware item)")
        else:
             print("  (No sub-hardware)")
        
        print("-" * 50)

    computer.Close()
    print("Diagnostics complete. Handle closed.")


if __name__ == "__main__":
    import ctypes
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False
    
    if not is_admin:
        print("[ERROR] Please run this script with Administrator privileges to access all hardware sensors.")
    else:
        run_diagnostics()