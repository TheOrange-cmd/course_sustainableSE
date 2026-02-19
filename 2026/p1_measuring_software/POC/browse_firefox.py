import sys
import clr
import time
import csv
import threading
import random 
import shutil
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import os

# ==============================================================================
# --- 1. MASTER CONFIGURATION
# ==============================================================================

# --- Experiment Parameters ---

NUM_REPETITIONS = 5
COOLDOWN = 10


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESULTS_DIR = os.path.join(BASE_DIR, "results")

def find_dll():
    winget_root = os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages"
    )

    for root, dirs, files in os.walk(winget_root):
        if "LibreHardwareMonitorLib.dll" in files:
            return os.path.join(root, "LibreHardwareMonitorLib.dll")

    raise FileNotFoundError("LibreHardwareMonitorLib.dll not found.")

DLL_PATH = find_dll()

# --- Define Your Experiments ---
EXPERIMENTS = [
    {
        "name": "youtube_no_adblock",
        "url": "https://www.youtube.com/watch?v=7ZhdXgRfxHI",
        "duration_seconds": 60,
        "use_adblock": False,
        "output_file": "results_no_adblock.csv"
    },
    {
        "name": "youtube_with_adblock",
        "url": "https://www.youtube.com/watch?v=7ZhdXgRfxHI",
        "duration_seconds": 60,
        "use_adblock": True,
        "output_file": "results_with_adblock.csv"
    }
]


def generate_randomized_schedule():
    schedule = []

    for config in EXPERIMENTS:
        for i in range(NUM_REPETITIONS):
            run_config = config.copy()
            run_config["run_id"] = i + 1
            run_config["output_file"] = f"results/{config['name']}_run_{i+1}.csv"
            schedule.append(run_config)

    random.shuffle(schedule)
    return schedule


# ==============================================================================
# --- 2. HARDWARE MONITORING CLASS (Unchanged)
# ==============================================================================

class HardwareMonitor:
    """A class to initialize LibreHardwareMonitor and collect hardware metrics."""
    def __init__(self, dll_path):
        self.handle = None
        self.sensors = {'cpu_load': None, 'cpu_power': None, 'gpu_load': None, 'mem_used': None}
        try:
            clr.AddReference(dll_path)
            from LibreHardwareMonitor import Hardware
            self.Hardware = Hardware 
            self.computer = self.Hardware.Computer()
            self.computer.IsCpuEnabled = True
            self.computer.IsGpuEnabled = True
            self.computer.IsMemoryEnabled = True
        except Exception as e:
            print(f"Error initializing LibreHardwareMonitor: {e}")
            sys.exit(1)

    def find_sensors(self):
        """Finds the required sensors."""
        print("Searching for required sensors...")
        self.computer.Open()
        time.sleep(2) 
        for hw in self.computer.Hardware:
            hw.Update()
            if hw.HardwareType == self.Hardware.HardwareType.Cpu:
                for sensor in hw.Sensors:
                    if sensor.SensorType == self.Hardware.SensorType.Load and sensor.Name == "CPU Total":
                        self.sensors['cpu_load'] = sensor
                    if sensor.SensorType == self.Hardware.SensorType.Power and sensor.Name == "CPU Package":
                        self.sensors['cpu_power'] = sensor
            if hw.HardwareType in [
                self.Hardware.HardwareType.GpuAmd, 
                self.Hardware.HardwareType.GpuNvidia,
                self.Hardware.HardwareType.GpuIntel
            ]:
                for sensor in hw.Sensors:
                    if sensor.SensorType == self.Hardware.SensorType.Load and (sensor.Name == "GPU Core" or "D3D 3D" in sensor.Name):
                        self.sensors['gpu_load'] = sensor
            if hw.HardwareType == self.Hardware.HardwareType.Memory:
                for sensor in hw.Sensors:
                    if sensor.SensorType == self.Hardware.SensorType.Data and sensor.Name == "Memory Used":
                        self.sensors['mem_used'] = sensor
        
        for key, sensor_obj in self.sensors.items():
            if sensor_obj:
                print(f"  [FOUND] Sensor for '{key}'")
            else:
                print(f"\n[WARNING] Could not find the sensor for '{key}'.")
        print("Sensor search complete.\n")

    def get_metrics(self):
        """Retrieves current values from found sensors."""
        for hw in self.computer.Hardware:
            hw.Update()
        metrics = {}
        for key, sensor in self.sensors.items():
            metrics[key] = sensor.Value if sensor and sensor.Value is not None else 0.0
        return metrics

    def close(self):
        """Closes the handle to LibreHardwareMonitor."""
        if self.computer:
            self.computer.Close()
            print("Hardware monitor handle closed.")

# ==============================================================================
# --- 3. CONCURRENT TASK FUNCTIONS
# ==============================================================================

def run_monitoring_task(monitor, config, stop_event):
    """This function runs in a separate thread, collecting hardware data."""
    output_file = config["output_file"]
    headers = ["timestamp", "Cpu_Load_Total", "Cpu_Power_Package_W", "Gpu_Load_Core", "Memory_Used_GB"]
    
    print(f"MONITOR: Starting monitoring. Data will be saved to '{output_file}'")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        while not stop_event.is_set():
            metrics = monitor.get_metrics()
            timestamp = datetime.now().isoformat()
            
            writer.writerow([
                timestamp,
                f"{metrics.get('cpu_load', 0.0):.2f}",
                f"{metrics.get('cpu_power', 0.0):.2f}",
                f"{metrics.get('gpu_load', 0.0):.2f}",
                f"{metrics.get('mem_used', 0.0):.2f}",
            ])
            stop_event.wait(1)
            
    print("MONITOR: Stop signal received. Monitoring finished.")

def run_browser_task(config, stop_event):
    """
    This function runs Firefox browser automation using Selenium.
    """
    print(f"BROWSER: Starting Firefox browser automation for experiment: '{config['name']}'")
    
    driver = None
    try:
        # Set up Firefox options
        options = FirefoxOptions()
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        
        # If adblock is enabled, install the extension
        if config["use_adblock"]:
            print(f"BROWSER: Ad blocker is ENABLED. Will install uBlock Origin...")
            extension_path = os.path.join(BASE_DIR, "uBlock0@raymondhill.net.xpi")
        else:
            print(f"BROWSER: Ad blocker is DISABLED. Using clean profile.")
            extension_path = None
        
        # Initialize the Firefox driver
        print(f"BROWSER: Launching Firefox with Selenium...")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # Install extension if needed
        if extension_path and os.path.exists(extension_path):
            driver.install_addon(extension_path, temporary=True)
            print(f"BROWSER: uBlock Origin extension installed")
            time.sleep(2)  # Give extension time to initialize
        
        # Set window size
        driver.set_window_size(1920, 1080)
        
        print(f"BROWSER: Navigating to {config['url']}...")
        driver.get(config['url'])
        
        # Wait for page to load
        time.sleep(3)
        
        # Try to accept cookies
        try:
            print("BROWSER: Looking for cookie consent dialog...")
            wait = WebDriverWait(driver, 10)
            accept_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label*="Accept"]'))
            )
            accept_button.click()
            print("BROWSER: Accepted cookies.")
            time.sleep(random.uniform(1, 2))
        except Exception:
            print("BROWSER: Cookie consent dialog not found or already accepted.")
        
        print(f"BROWSER: 'Watching' video for {config['duration_seconds']} seconds...")
        time.sleep(config['duration_seconds'])
        
        print("BROWSER: Task finished.")

    except Exception as e:
        print(f"BROWSER: A critical error occurred in the browser task: {e}")
    
    finally:
        # Clean up
        if driver:
            try:
                driver.quit()
                print("BROWSER: Browser closed.")
            except Exception as e:
                print(f"BROWSER: Warning - couldn't close browser: {e}")
        
        # This 'finally' block is responsible for signaling the other thread.
        print("BROWSER: Signaling monitor to stop.")
        stop_event.set()

# ==============================================================================
# --- 4. MAIN EXECUTION LOGIC
# ==============================================================================

def main():
    """Main function to orchestrate the experiments."""
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[ERROR] This script requires Administrator privileges to access hardware sensors.")
        return
    
    # Make sure results folder exists
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print(f"Results will be stored in: {RESULTS_DIR}")

    monitor = HardwareMonitor(DLL_PATH)
    monitor.find_sensors()

    schedule = generate_randomized_schedule()

    print("\n" + "=" *80)
    print(f"TOTAL RUNS: {len(schedule)}")
    print(f"{NUM_REPETITIONS} repetitions per condition")
    print("Execution order has been RANDOMIZED.")
    print("Using Selenium with Firefox + uBlock Origin for adblock tests.")
    print("=" * 80)

    for i, experiment_config in enumerate(schedule):
        print("\n" + "="*80)
        print(
            f"RUN {i+1}/{len(schedule)} | "
            f"{experiment_config['name']} | "
            f"Rep {experiment_config['run_id']}"
        )
        print("="*80)
        
        stop_monitoring_event = threading.Event()
        
        monitor_thread = threading.Thread(target=run_monitoring_task, args=(monitor, experiment_config, stop_monitoring_event))
        browser_thread = threading.Thread(target=run_browser_task, args=(experiment_config, stop_monitoring_event))
        
        monitor_thread.start()
        time.sleep(2)
        browser_thread.start()
        
        browser_thread.join()
        monitor_thread.join()
        
        print(f"--- Run {i+1} complete. ---")

        if i < len(schedule) - 1:
            print(f"\nSystem cooling down for {COOLDOWN} seconds before next experiment...")
            time.sleep(COOLDOWN)

    monitor.close()
    print("\nAll experiments finished.")

if __name__ == "__main__":
    main()
