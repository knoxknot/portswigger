import os
import platform
import subprocess
import sys

def check_binary(binary_name):
  if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    command = ['which', binary_name]
  elif sys.platform.startswith('win'):
    command = ['where', binary_name]
  else:
    print("Unsupported operating system")
    return

  try:
    subprocess.check_output(command)
    return True
  except subprocess.CalledProcessError:
    print(f"{binary_name} is not installed.")
    return False

def install_binary(binary_url, binary_name):
  os_name = platform.system().lower()
  binary_file = f"{binary_name}.zip" if os_name == 'windows' else f"{binary_name}.tar.gz"
  
  # Check if binary exists
  if not check_binary(binary_name):
    # Download Binary File if not exist
    if not os.path.exists(binary_file):
      if os_name == 'linux':
        download_command = f"curl -L {binary_url}/x86_64-linux-{binary_name}.tar.gz -o {binary_file}"
      elif os_name == 'darwin':
        download_command = f"curl -L {binary_url}/x86_64-macos-{binary_name}.tar.gz -o {binary_file}"
      elif sys.platform.startswith('win'):
        download_command = f"powershell -Command 'Invoke-WebRequest {binary_url}/x86_64-windows-{binary_name}.exe.zip -OutFile {binary_file}'"
      else:
        print("Unsupported operating system")
        return

      try:
        subprocess.run(download_command, shell=True, check=True)
        print(f"{binary_name} downloaded successfully")
      except subprocess.CalledProcessError as e:
        print(f"Failed to download {binary_name}: {e}")

    # Install Binary
    if os.path.exists(binary_file):
      if os_name in ['linux', 'darwin']:
        extract_command = f"sudo tar -C /usr/local/bin/ -xzf {binary_file} {binary_name} && sudo chmod 775 /usr/local/bin/{binary_name}"
      elif sys.platform.startswith('win'):
        extract_command = f"Powershell -Command \"Expand-Archive -Path {binary_file} -DestinationPath . ; Move-Item -Path .\\{binary_name}.exe -Destination 'C:\\Windows\\'\""
      else:
        print("Unsupported operating system")
        return

      try:
        subprocess.run(extract_command, shell=True, check=True)
        print(f"{binary_name} installed successfully")
      except subprocess.CalledProcessError as e:
        print(f"Failed to install {binary_name}: {e}")

      # Clean up downloaded binary file
      try:
        cleanup_command = f"rm {binary_file}" if os_name != 'windows' else f"del {binary_file}"
        subprocess.run(cleanup_command, shell=True, check=True)
        print(f"Cleaned up {binary_file}")
      except subprocess.CalledProcessError as e:
        print(f"Failed to clean up {binary_file}: {e}")
  else:
    print(f"{binary_name} is already installed.")

def enumerate_path(endpoint, wordlist_path):
  print("Enumerating paths...")
  fuzz_command = f"feroxbuster -u {endpoint} -w {wordlist_path} -C 404 --proxy http://127.0.0.1:8080 --insecure --quiet --no-state --auto-tune"
  process = subprocess.Popen(fuzz_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  for line in process.stdout:
    print(line.strip())

def main():
  binary_url = "https://github.com/epi052/feroxbuster/releases/download/v2.10.2"
  binary_name = "feroxbuster"
  endpoint = "https://0a3900c2044cf17781f1123e00480036.web-security-academy.net/"
  wordlist_path = "wordlist.txt"
  install_binary(binary_url, binary_name)
  enumerate_path(endpoint, wordlist_path)

if __name__ == "__main__":
  main()
