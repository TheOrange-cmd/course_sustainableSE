import sys
import clr
import time
import csv
import threading
import random 
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import shutil 
import os

# ==============================================================================
# --- 1. MASTER CONFIGURATION
# ==============================================================================

# --- IMPORTANT: UPDATE THIS PATH ---
# This must be the FULL, ABSOLUTE path to the UNPACKED uBlock Origin Lite extension folder.
UBLOCK_LITE_PATH = "C:\\Users\\danie\\Documents\\GitHub\\course_sustainableSE\\2026\\p1_measuring_software\\POC\\extensions\\ublock_chrome"

# --- Directory for the persistent browser profile ---
# A new folder will be created here. It's good practice to clean it between full test suites.
USER_DATA_DIR = "./playwright_user_data"

# --- IMPORTANT: UPDATE THIS PATH ---
# --- LibreHardwareMonitor DLL Path ---
DLL_PATH = "C:\\Users\\danie\\AppData\\Local\\Microsoft\\WinGet\\Packages\\LibreHardwareMonitor.LibreHardwareMonitor_Microsoft.Winget.Source_8wekyb3d8bbwe\\LibreHardwareMonitorLib.dll"

# --- Define Your Experiments ---
EXPERIMENTS = [
    # {
    #     "name": "youtube_no_adblock",
    #     "url": "https://www.youtube.com/watch?v=7ZhdXgRfxHI",
    #     "duration_seconds": 60,
    #     "use_adblock": False,
    #     "output_file": "results_no_adblock.csv"
    # },
    {
        "name": "youtube_with_adblock",
        "url": "https://www.youtube.com/watch?v=7ZhdXgRfxHI",
        "duration_seconds": 60,
        "use_adblock": True,
        "output_file": "results_with_adblock.csv"
    }
]

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
                    if sensor.SensorType == self.Hardware.SensorType.Power and sensor.Name == "Package":
                        self.sensors['cpu_power'] = sensor
            if hw.HardwareType in [self.Hardware.HardwareType.GpuAmd, self.Hardware.HardwareType.GpuNvidia]:
                for sensor in hw.Sensors:
                    if sensor.SensorType == self.Hardware.SensorType.Load and sensor.Name == "GPU Core":
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
    This function runs the Playwright browser automation.
    """
    print(f"BROWSER: Starting browser automation for experiment: '{config['name']}'")
    
    try:
        with sync_playwright() as p:
            context = None  # Define context here to ensure it's in scope for finally
            try:
                launch_args = ["--start-maximized"]
                
                if config["use_adblock"]:
                    print("BROWSER: Ad blocker is ENABLED for this run.")
                    launch_args.extend([
                        f"--disable-extensions-except={UBLOCK_LITE_PATH}",
                        f"--load-extension={UBLOCK_LITE_PATH}",
                    ])
                else:
                    print("BROWSER: Ad blocker is DISABLED for this run.")

                context = p.chromium.launch_persistent_context(
                    USER_DATA_DIR,
                    headless=False,
                    channel="chromium",
                    args=launch_args,
                    no_viewport=True,
                )
                
                if config["use_adblock"]:
                    print("BROWSER: Waiting for ad blocker service worker to initialize...")
                    if not context.service_workers:
                        service_worker = context.wait_for_event('serviceworker')
                    else:
                        service_worker = context.service_workers[0]
                    print(f"BROWSER: Service worker for extension is active: {service_worker.url}")
                    time.sleep(3)

                page = context.new_page()
                stealth = Stealth()
                stealth.apply_stealth_sync(page)

                print(f"BROWSER: Navigating to {config['url']}...")
                page.goto(config['url'], timeout=90000, wait_until="domcontentloaded")
                
                try:
                    print("BROWSER: Looking for cookie consent dialog...")
                    accept_button = page.locator('button[aria-label="Accept the use of cookies and other data for the purposes described"]')
                    accept_button.click(timeout=10000)
                    print("BROWSER: Accepted cookies.")
                    time.sleep(random.uniform(1, 2))
                except Exception:
                    print("BROWSER: Cookie consent dialog not found or already accepted.")
                
                print(f"BROWSER: 'Watching' video for {config['duration_seconds']} seconds...")
                time.sleep(config['duration_seconds'])
                
                print("BROWSER: Task finished.")

            finally:
                # This 'finally' block executes before the 'with sync_playwright()' block exits.
                if context:
                    context.close()
                    print("BROWSER: Context closed.")
    
    except Exception as e:
        print(f"BROWSER: A critical error occurred in the browser task: {e}")
    
    finally:
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

    # Clean up the old user data directory for a fresh start
    if os.path.exists(USER_DATA_DIR):
        print(f"Removing old user data directory: {USER_DATA_DIR}")
        shutil.rmtree(USER_DATA_DIR)

    monitor = HardwareMonitor(DLL_PATH)
    monitor.find_sensors()

    for i, experiment_config in enumerate(EXPERIMENTS):
        print("\n" + "="*80)
        print(f"RUNNING EXPERIMENT {i+1}/{len(EXPERIMENTS)}: {experiment_config['name']}")
        print("="*80)
        
        stop_monitoring_event = threading.Event()
        
        monitor_thread = threading.Thread(target=run_monitoring_task, args=(monitor, experiment_config, stop_monitoring_event))
        browser_thread = threading.Thread(target=run_browser_task, args=(experiment_config, stop_monitoring_event))
        
        monitor_thread.start()
        time.sleep(2)
        browser_thread.start()
        
        browser_thread.join()
        monitor_thread.join()
        
        print(f"--- Experiment '{experiment_config['name']}' complete. ---")

        if i < len(EXPERIMENTS) - 1:
            print("\nSystem cooling down for 10 seconds before next experiment...")
            time.sleep(10)

    monitor.close()
    print("\nAll experiments finished.")

if __name__ == "__main__":
    main()