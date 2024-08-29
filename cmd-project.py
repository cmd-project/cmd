from datetime import datetime, timezone
import os
import socket
import requests
from bs4 import BeautifulSoup
import subprocess
import random
import sys
import shutil
import time  # اضافه کردن ماژول time

def change_directory(folder):
    try:
        os.chdir(folder)
        print(f"Current directory changed to {os.getcwd()}")
    except FileNotFoundError:
        print(f"Directory not found: {folder}")
    except Exception as e:
        print(f"Error changing directory: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File deleted: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

def delete_directory(dir_path):
    try:
        shutil.rmtree(dir_path)
        print(f"Directory deleted: {dir_path}")
    except FileNotFoundError:
        print(f"Directory not found: {dir_path}")
    except Exception as e:
        print(f"Error deleting directory: {e}")

def delete_path(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"File deleted: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Directory deleted: {path}")
        else:
            print(f"Path not found: {path}")
    except Exception as e:
        print(f"Error deleting path: {e}")

def simulate_requests(url):
    try:
        num_requests = 50
        num_devices = 999999
        
        user_ip = get_public_ip()
        if user_ip is None:
            return

        for device in range(num_devices):
            user_agent = f"Device-{device + 1}/1.0 (Random-UserAgent; {random.randint(1000, 9999)})"
            headers = {"User-Agent": user_agent}

            print(f"Simulating device {device + 1} with User-Agent: {user_agent}")
            for _ in range(num_requests):
                response = requests.get(url, headers=headers)
                print(f"Request sent with User-Agent: {user_agent}, Status Code: {response.status_code}")
                time.sleep(random.uniform(1, 3))
    
    except requests.RequestException as e:
        print(f"Error simulating requests: {e}")

def get_ip_details():
    try:
        hostname = socket.gethostname()
        ipv4 = socket.gethostbyname(hostname)
        ipv6 = socket.getaddrinfo(hostname, None, socket.AF_INET6)[0][4][0]
        print(f"IPv4 address: {ipv4}")
        print(f"IPv6 address: {ipv6}")
    except Exception as e:
        print(f"Error retrieving IP details: {e}")

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        data = response.json()
        ip = data.get('ip')
        return ip
    except requests.RequestException as e:
        print(f"Error retrieving public IP: {e}")
        return None

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        response.raise_for_status()
        data = response.json()
        location = data.get('city', 'Unknown city') + ', ' + data.get('region', 'Unknown region') + ', ' + data.get('country', 'Unknown country')
        print(f"Location for IP {ip}: {location}")
    except requests.RequestException as e:
        print(f"Error retrieving location: {e}")

def get_public_ip_location():
    ip = get_public_ip()
    if ip:
        get_location(ip)

def start_html_server(file_path):
    try:
        directory = os.path.dirname(file_path)
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return
        subprocess.run(["python3", "-m", "http.server", "--directory", directory, "8000"], check=True)
        print(f"Serving {file_path} on http://127.0.0.1:8000")
    except Exception as e:
        print(f"Error starting HTML server: {e}")

def install_file(url):
    try:
        install_dir = 'files_cmd_install'
        os.makedirs(install_dir, exist_ok=True)
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filename = url.split('/')[-1]
        file_path = os.path.join(install_dir, filename)
        
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"File downloaded and saved to {file_path}")
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")

def list_web_pages(url):
    try:
        response = requests.get(f"http://{url}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/'):
                links.add(f"http://{url}{href}")
        if links:
            print("Found pages:")
            for link in links:
                print(link)
        else:
            print(f"No pages found for {url}.")
    except requests.RequestException as e:
        print(f"Error fetching pages: {e}")

def get_ip_address(url):
    try:
        hostname = socket.gethostbyname(url)
        print(f"IP address of {url} is: {hostname}")
    except socket.gaierror as e:
        print(f"Error resolving IP address: {e}")

def scan_ports(url):
    try:
        hostname = socket.gethostbyname(url)
        common_ports = [22, 80, 443, 8080]
        open_ports = []
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((hostname, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        if open_ports:
            print(f"Open ports for {url}: {', '.join(map(str, open_ports))}")
        else:
            print(f"No open ports found for {url}.")
    except socket.gaierror as e:
        print(f"Error resolving hostname: {e}")

def list_files():
    files = os.listdir('.')
    if files:
        print("Files in the current directory:")
        for file in files:
            print(file)

def show_utc_time():
    utc_time = datetime.now(timezone.utc)
    print(f"Current UTC time: {utc_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    print("hello user")
    while True:
        user_input = input("CMD:\cmd.sh ~* ")
        if user_input.lower() == "time":
            show_utc_time()
        elif user_input.lower().startswith("delete -fr "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, dir_path = parts
                if flag == "-fr":
                    delete_directory(dir_path)
        elif user_input.lower().startswith("cd -f "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, folder = parts
                if flag == "-f":
                    change_directory(folder)
        elif user_input.lower().startswith("delete -file "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, file_path = parts
                if flag == "-file":
                    delete_file(file_path)
        elif user_input.lower().startswith("delete -rf "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, path = parts
                if flag == "-rf":
                    delete_path(path)
        elif user_input == "errors":
            print(""" 
            error-1 = There is no order
            error-2 = null
            """)
        elif user_input == "help":
            print("""
            cmd = version cmd
            time = times
            exit = exit
            """)
        elif user_input == "cmd":
            print("version: 5.1")
        elif user_input.lower() == "ip -me":
            ip = get_public_ip()
            if ip:
                print(f"Public IP address: {ip}")
        elif user_input.lower() == "ip -me -map":
            get_public_ip_location()
        elif user_input.lower().startswith("ip -s "):
            parts = user_input.split()
            if len(parts) == 4:
                cmd, flag, ip, map_flag = parts
                if flag == "-s" and map_flag == "-map":
                    get_location(ip)
        elif user_input.lower().startswith("html -file "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, file_name = parts
                if flag == "-file":
                    start_html_server(file_name)
        elif user_input.lower().startswith("install -wab -file "):
            parts = user_input.split()
            if len(parts) == 4:
                cmd, flag, file_cmd, file_url = parts
                if flag == "-wab" and file_cmd == "-file":
                    install_file(file_url)
        elif user_input.lower() == "exit":
            print("Exiting the program.")
            break
        elif user_input.lower().startswith("wab -m "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, url = parts
                if flag == "-m":
                    list_web_pages(url)
        elif user_input.lower() == "ls":
            list_files()
        elif user_input.lower().startswith("port -wab "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, url = parts
                if flag == "-wab":
                    scan_ports(url)
                else:
                    print("Invalid command format. Use 'port -wab <url>'.")
            else:
                print("Invalid command format. Use 'port -wab <url>'.")
        elif user_input.lower().startswith("-dd "):
            parts = user_input.split()
            if len(parts) == 2:
                cmd, url = parts
                simulate_requests(url)
        elif user_input.lower().startswith("ping -wab "):
            parts = user_input.split()
            if len(parts) == 3:
                cmd, flag, url = parts
                if flag == "-wab":
                    get_ip_address(url)
                else:
                    print("Invalid command format. Use 'ping -wab <url>'.")
            else:
                print("Invalid command format. Use 'ping -wab <url>'.")
        else:
            print("""
            There is no order
            error1
            """)
            