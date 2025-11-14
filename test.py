#!/usr/bin/env python3

import paramiko
import json
import csv
import logging
from datetime import datetime
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_health_main.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class ServerHealthMonitor:
    def __init__(self, config_file: Optional[str] = None):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.servers = self._load_servers(config_file)
        self.collected_data = {}
        self.failed_connections = []
        logs_dir = os.path.join(self.script_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        main_log_path = os.path.join(self.script_dir, 'server_health_main.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(main_log_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.main_logger = logging.getLogger()
        
    def _load_servers(self, config_file: Optional[str] = None) -> List[Dict[str, Any]]:
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    servers = json.load(f)
                self.main_logger.info(f"Loaded server configuration from {config_file}")
                return servers
            except Exception as e:
                self.main_logger.error(f"Failed to load config file: {e}")
        return [
            {
                "name": "ubuntu-vm",
                "hostname": "192.168.1.37",
                "username": "neo", 
                "password": "marshall",
                "port": 22
            },
            {
                "name": "redhat-vm", 
                "hostname": "192.168.1.24",
                "username": "neon",
                "password": "neon",
                "port": 22
            }
        ]
    
    def get_server_logger(self, server_name: str) -> logging.Logger:
        logger_name = f"server_{server_name}"
        server_logger = logging.getLogger(logger_name)
        if not server_logger.handlers:
            server_logger.setLevel(logging.INFO)
            server_logger.propagate = False
            log_filename = os.path.join(self.script_dir, 'logs', f'{server_name}.log')
            file_handler = logging.FileHandler(log_filename)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            server_logger.addHandler(file_handler)
        return server_logger
    
    def execute_remote_command(self, ssh_client: paramiko.SSHClient, command: str) -> tuple:
        try:
            stdin, stdout, stderr = ssh_client.exec_command(command, timeout=30)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            if error and "Warning" not in error:
                logging.warning(f"Command '{command}' returned error: {error}")
            return output, error
        except Exception as e:
            logging.error(f"Failed to execute command '{command}': {e}")
            return "", str(e)
    
    def parse_uptime(self, uptime_output: str) -> Dict[str, Any]:
        try:
            if not uptime_output:
                return {"load_1min": 0, "load_5min": 0, "load_15min": 0, "uptime_string": "Unknown"}
            parts = uptime_output.split('load average:')
            load_avg = parts[1].strip().split(',') if len(parts) > 1 else ['0', '0', '0']
            return {
                "load_1min": float(load_avg[0].strip()),
                "load_5min": float(load_avg[1].strip()),
                "load_15min": float(load_avg[2].strip()),
                "uptime_string": parts[0].strip() if parts else uptime_output
            }
        except Exception as e:
            logging.error(f"Error parsing uptime: {e}")
            return {"load_1min": 0, "load_5min": 0, "load_15min": 0, "uptime_string": "Unknown"}
    
    def parse_disk_usage(self, df_output: str) -> List[Dict[str, str]]:
        disks = []
        try:
            if not df_output:
                return disks
            lines = df_output.split('\n')[1:]
            for line in lines:
                if line.strip() and not line.startswith('tmpfs') and not line.startswith('udev'):
                    parts = line.split()
                    if len(parts) >= 6:
                        disk_info = {
                            "filesystem": parts[0],
                            "size": parts[1],
                            "used": parts[2],
                            "available": parts[3],
                            "use_percent": parts[4].rstrip('%'),
                            "mounted_on": parts[5]
                        }
                        disks.append(disk_info)
            return disks
        except Exception as e:
            logging.error(f"Error parsing disk usage: {e}")
            return []
    
    def parse_memory_usage(self, free_output: str) -> Dict[str, int]:
        try:
            if not free_output:
                return {}
            lines = free_output.split('\n')
            if len(lines) < 3:
                return {}
            memory_line = lines[1].split()
            swap_line = lines[2].split()
            memory_data = {
                "memory_total": int(memory_line[1]),
                "memory_used": int(memory_line[2]),
                "memory_free": int(memory_line[3]),
                "memory_available": int(memory_line[6]) if len(memory_line) > 6 else 0
            }
            if len(swap_line) >= 4:
                memory_data.update({
                    "swap_total": int(swap_line[1]),
                    "swap_used": int(swap_line[2]),
                    "swap_free": int(swap_line[3])
                })
            if memory_data["memory_total"] > 0:
                memory_data["memory_usage_percent"] = round(
                    (memory_data["memory_used"] / memory_data["memory_total"]) * 100, 2
                )
            return memory_data
        except Exception as e:
            logging.error(f"Error parsing memory usage: {e}")
            return {}
    
    def collect_server_data(self, server_config: Dict[str, Any]) -> Dict[str, Any]:
        server_name = server_config["name"]
        server_logger = self.get_server_logger(server_name)
        server_data = {
            "timestamp": datetime.now().isoformat(),
            "server_name": server_name,
            "hostname": server_config["hostname"],
            "status": "success"
        }
        server_logger.info(f"Starting health check for {server_name}")
        self.main_logger.info(f"Checking server: {server_name}")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            server_logger.info(f"Connecting to {server_config['hostname']}")
            ssh_client.connect(
                hostname=server_config["hostname"],
                username=server_config["username"],
                password=server_config["password"],
                port=server_config.get("port", 22),
                timeout=15,
                banner_timeout=20
            )
            server_logger.info("Successfully connected to server")
            self.main_logger.info(f"Connected to {server_name}")
            uptime_output, uptime_error = self.execute_remote_command(ssh_client, "uptime")
            server_logger.info(f"Uptime command executed - Output length: {len(uptime_output)}")
            df_output, df_error = self.execute_remote_command(ssh_client, "df -h")
            server_logger.info(f"Disk usage command executed - Output length: {len(df_output)}")
            free_output, free_error = self.execute_remote_command(ssh_client, "free -m")
            server_logger.info(f"Memory usage command executed - Output length: {len(free_output)}")
            server_data["uptime"] = self.parse_uptime(uptime_output)
            server_data["disk_usage"] = self.parse_disk_usage(df_output)
            server_data["memory"] = self.parse_memory_usage(free_output)
            if uptime_error and "Warning" not in uptime_error:
                server_data["uptime_error"] = uptime_error
                server_logger.warning(f"Uptime command error: {uptime_error}")
            if df_error and "Warning" not in df_error:
                server_data["disk_error"] = df_error
                server_logger.warning(f"Disk usage command error: {df_error}")
            if free_error and "Warning" not in free_error:
                server_data["memory_error"] = free_error
                server_logger.warning(f"Memory usage command error: {free_error}")
            server_logger.info("Health check completed successfully")
            self.main_logger.info(f"Successfully collected data from {server_name}")
        except paramiko.AuthenticationException:
            error_msg = f"Authentication failed for {server_name}"
            server_logger.error(error_msg)
            self.main_logger.error(f"{server_name}: Authentication failed")
            server_data["status"] = "failed"
            server_data["error"] = "Authentication failed"
            self.failed_connections.append({
                "server": server_name,
                "error": "Authentication failed",
                "timestamp": datetime.now().isoformat()
            })
        except paramiko.SSHException as e:
            error_msg = f"SSH connection failed for {server_name}: {e}"
            server_logger.error(error_msg)
            self.main_logger.error(f"{server_name}: SSH connection failed")
            server_data["status"] = "failed"
            server_data["error"] = str(e)
            self.failed_connections.append({
                "server": server_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            error_msg = f"Unexpected error connecting to {server_name}: {e}"
            server_logger.error(error_msg)
            self.main_logger.error(f"{server_name}: Connection failed - {e}")
            server_data["status"] = "failed"
            server_data["error"] = str(e)
            self.failed_connections.append({
                "server": server_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        finally:
            ssh_client.close()
            server_logger.info("SSH connection closed")
        return server_data
    
    def save_to_json(self, filename: str = "server_health_data.json"):
        try:
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "servers_checked": len(self.servers),
                "successful_connections": len([d for d in self.collected_data.values() if d["status"] == "success"]),
                "failed_connections": len(self.failed_connections),
                "data": self.collected_data,
                "failed_connections_detail": self.failed_connections
            }
            filepath = os.path.join(self.script_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(output_data, f, indent=2)
            self.main_logger.info(f"Data saved to {filepath}")
        except Exception as e:
            self.main_logger.error(f"Failed to save JSON: {e}")
    
    def save_to_csv(self, filename: str = "server_health_data.csv"):
        try:
            filepath = os.path.join(self.script_dir, filename)
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'server_name', 'timestamp', 'status', 'hostname',
                    'load_1min', 'load_5min', 'load_15min', 'uptime_string',
                    'memory_total_mb', 'memory_used_mb', 'memory_free_mb', 
                    'memory_available_mb', 'memory_usage_percent',
                    'swap_total_mb', 'swap_used_mb', 'swap_free_mb',
                    'root_disk_usage_percent'
                ])
                for server_name, data in self.collected_data.items():
                    if data["status"] == "success":
                        root_disk_usage = 0
                        for disk in data["disk_usage"]:
                            if disk["mounted_on"] == "/":
                                root_disk_usage = disk["use_percent"]
                                break
                        writer.writerow([
                            server_name,
                            data["timestamp"],
                            data["status"],
                            data["hostname"],
                            data["uptime"]["load_1min"],
                            data["uptime"]["load_5min"],
                            data["uptime"]["load_15min"],
                            data["uptime"]["uptime_string"],
                            data["memory"].get("memory_total", 0),
                            data["memory"].get("memory_used", 0),
                            data["memory"].get("memory_free", 0),
                            data["memory"].get("memory_available", 0),
                            data["memory"].get("memory_usage_percent", 0),
                            data["memory"].get("swap_total", 0),
                            data["memory"].get("swap_used", 0),
                            data["memory"].get("swap_free", 0),
                            root_disk_usage
                        ])
                    else:
                        writer.writerow([
                            server_name,
                            data["timestamp"],
                            data["status"],
                            data["hostname"],
                            0, 0, 0, "Unknown",
                            0, 0, 0, 0, 0,
                            0, 0, 0, 0
                        ])
            self.main_logger.info(f"Data saved to {filepath}")
        except Exception as e:
            self.main_logger.error(f"Failed to save CSV: {e}")
    
    def visualize_data(self, output_file: str = "server_health_dashboard.png"):
        if not self.collected_data:
            self.main_logger.warning("No data to visualize")
            return
        try:
            servers = []
            load_1min = []
            load_5min = []
            load_15min = []
            memory_usage = []
            disk_usage = []
            statuses = []
            for server_name, data in self.collected_data.items():
                servers.append(server_name)
                if data["status"] == "success":
                    statuses.append(1)
                    load_1min.append(data["uptime"]["load_1min"])
                    load_5min.append(data["uptime"]["load_5min"])
                    load_15min.append(data["uptime"]["load_15min"])
                    mem_usage = data["memory"].get("memory_usage_percent", 0)
                    memory_usage.append(mem_usage)
                    root_disk_usage = 0
                    for disk in data["disk_usage"]:
                        if disk["mounted_on"] == "/":
                            root_disk_usage = float(disk["use_percent"])
                            break
                    disk_usage.append(root_disk_usage)
                else:
                    statuses.append(0)
                    load_1min.append(0)
                    load_5min.append(0)
                    load_15min.append(0)
                    memory_usage.append(0)
                    disk_usage.append(0)
            plt.switch_backend('Agg')
            plt.style.use('seaborn-v0_8')
            fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 18))
            fig.suptitle('Server Health Dashboard', fontsize=20, fontweight='bold')
            bars1 = ax1.bar(servers, load_1min, color='lightblue', alpha=0.7)
            ax1.set_title('1-minute Load Average\n(Immediate CPU Demand)', fontweight='bold', fontsize=12)
            ax1.set_ylabel('Load Average')
            ax1.tick_params(axis='x', rotation=45)
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom', fontsize=9)
            ax1.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Overload Threshold')
            ax1.legend()
            bars2 = ax2.bar(servers, load_5min, color='lightsteelblue', alpha=0.7)
            ax2.set_title('5-minute Load Average\n(Recent CPU Trend)', fontweight='bold', fontsize=12)
            ax2.set_ylabel('Load Average')
            ax2.tick_params(axis='x', rotation=45)
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom', fontsize=9)
            ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Overload Threshold')
            ax2.legend()
            bars3 = ax3.bar(servers, load_15min, color='steelblue', alpha=0.7)
            ax3.set_title('15-minute Load Average\n(Long-term CPU Baseline)', fontweight='bold', fontsize=12)
            ax3.set_ylabel('Load Average')
            ax3.tick_params(axis='x', rotation=45)
            for bar in bars3:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom', fontsize=9)
            ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Overload Threshold')
            ax3.legend()
            bars4 = ax4.bar(servers, memory_usage, color='lightcoral', alpha=0.7)
            ax4.set_title('Memory Usage Percentage', fontweight='bold', fontsize=12)
            ax4.set_ylabel('Usage (%)')
            ax4.tick_params(axis='x', rotation=45)
            for bar in bars4:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
            bars5 = ax5.bar(servers, disk_usage, color='lightgreen', alpha=0.7)
            ax5.set_title('Root Disk Usage Percentage', fontweight='bold', fontsize=12)
            ax5.set_ylabel('Usage (%)')
            ax5.tick_params(axis='x', rotation=45)
            for bar in bars5:
                height = bar.get_height()
                ax5.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
            colors = ['green' if s == 1 else 'red' for s in statuses]
            bars6 = ax6.bar(servers, statuses, color=colors, alpha=0.7)
            ax6.set_title('Server Connection Status', fontweight='bold', fontsize=12)
            ax6.set_ylabel('Status (1=Success, 0=Failed)')
            ax6.set_ylim(0, 1.2)
            ax6.tick_params(axis='x', rotation=45)
            for bar, status in zip(bars6, statuses):
                height = bar.get_height()
                status_text = 'ONLINE' if status == 1 else 'OFFLINE'
                ax6.text(bar.get_x() + bar.get_width()/2., height, status_text, ha='center', va='bottom', fontweight='bold', fontsize=10)
            plt.tight_layout()
            filepath = os.path.join(self.script_dir, output_file)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.main_logger.info(f"Visualization saved as {filepath}")
        except Exception as e:
            self.main_logger.error(f"Failed to create visualization: {e}")
    
    def generate_summary_report(self):
        successful = sum(1 for data in self.collected_data.values() if data["status"] == "success")
        total = len(self.servers)
        print("\n" + "="*70)
        print("                   SERVER HEALTH CHECK SUMMARY")
        print("="*70)
        print(f"Total servers checked: {total}")
        print(f"Successful connections: {successful}")
        print(f"Failed connections: {total - successful}")
        print(f"Success rate: {(successful/total)*100:.1f}%")
        print("\nDetailed Results:")
        print("-" * 70)
        for server_name, data in self.collected_data.items():
            status_icon = "✅" if data["status"] == "success" else "❌"
            print(f"{status_icon} {server_name} ({data['hostname']}): {data['status'].upper()}")
            if data["status"] == "success":
                load_1min = data["uptime"]["load_1min"]
                load_5min = data["uptime"]["load_5min"]
                load_15min = data["uptime"]["load_15min"]
                memory = data["memory"]
                mem_used = memory.get("memory_used", 0)
                mem_total = memory.get("memory_total", 0)
                mem_percent = memory.get("memory_usage_percent", 0)
                load_1min_status = "✅ Good" if load_1min < 1.0 else "⚠️ High" if load_1min < 2.0 else "❌ Critical"
                load_5min_status = "✅ Good" if load_5min < 1.0 else "⚠️ High" if load_5min < 2.0 else "❌ Critical"
                load_15min_status = "✅ Good" if load_15min < 1.0 else "⚠️ High" if load_15min < 2.0 else "❌ Critical"
                root_disk = next((disk for disk in data["disk_usage"] if disk["mounted_on"] == "/"), None)
                disk_percent = root_disk["use_percent"] if root_disk else "N/A"
                print(f"   📊 Load: 1min={load_1min:.2f} ({load_1min_status}), 5min={load_5min:.2f} ({load_5min_status}), 15min={load_15min:.2f} ({load_15min_status})")
                print(f"   🧠 Memory: {mem_used}/{mem_total} MB ({mem_percent}%) | 💾 Root Disk: {disk_percent}% used")
            else:
                print(f"   💥 Error: {data.get('error', 'Unknown error')}")
            print()
        print("="*70)
        print("LOAD INTERPRETATION GUIDE:")
        print("  ✅ Good: <1.0   ⚠️ High: 1.0-2.0   ❌ Critical: >2.0")
        print("  Load >1.0 means processes were waiting for CPU time")
        print("="*70)
    
    def run_health_check(self, enable_visualization: bool = True):
        self.main_logger.info("Starting server health check...")
        print("🚀 Starting Remote Server Health Dashboard...")
        print(f"📁 Output directory: {self.script_dir}")
        if not self.servers:
            self.main_logger.error("No servers configured!")
            print("❌ No servers configured. Please add servers to the configuration.")
            return {}
        print(f"🔍 Checking {len(self.servers)} server(s)...")
        for server in self.servers:
            print(f"   📡 Connecting to {server['name']}...")
            server_data = self.collect_server_data(server)
            self.collected_data[server["name"]] = server_data
        self.save_to_json()
        self.save_to_csv()
        self.generate_summary_report()
        if enable_visualization:
            successful_servers = sum(1 for data in self.collected_data.values() if data["status"] == "success")
            if successful_servers > 0:
                print("📊 Generating visualizations...")
                self.visualize_data()
                print(f"   ✅ Dashboard saved as 'server_health_dashboard.png'")
                print(f"   📊 Now tracking: 1-min, 5-min, and 15-min load averages separately")
            else:
                print("⚠️  No successful connections - skipping visualization")
        self.main_logger.info("Server health check completed")
        print("✅ Health check completed!")
        return self.collected_data

def create_sample_config():
    sample_config = [
        {
            "name": "ubuntu-vm",
            "hostname": "192.168.1.37",
            "username": "player01",
            "password": "123",
            "port": 22
        },
        {
            "name": "redhat-vm", 
            "hostname": "192.168.1.24",
            "username": "neon",
            "password": "neon",
            "port": 22
        }
    ]
    with open('servers_config.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    print("📝 Sample configuration file created: 'servers_config.json'")
    print("💡 Edit this file with your server details and use: --config servers_config.json")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Remote Server Health Dashboard')
    parser.add_argument('--config', type=str, help='Path to server configuration JSON file')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    parser.add_argument('--create-config', action='store_true', help='Create sample configuration file')
    args = parser.parse_args()
    if args.create_config:
        create_sample_config()
        return
    monitor = ServerHealthMonitor(config_file=args.config)
    enable_viz = not args.no_viz
    results = monitor.run_health_check(enable_visualization=enable_viz)
    successful = sum(1 for data in results.values() if data["status"] == "success")
    if successful == 0 and len(results) > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()