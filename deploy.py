import os
import paramiko
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def deploy():
    host = os.getenv("SFTP_HOST")
    user = os.getenv("SFTP_USER")
    password = os.getenv("SFTP_PASS")
    remote_path = os.getenv("SFTP_PATH")
    
    if not all([host, user, password, remote_path]):
        print("Missing SFTP credentials in .env file.")
        return

    # Files to upload
    files_to_upload = ["index.html", "style.css"]
    
    # Images (if they exist locally and need to be uploaded)
    # For now, we only upload the main files
    
    try:
        print(f"Connecting to {host} via SFTP...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password)
        
        sftp = ssh.open_sftp()
        print(f"Successfully connected. Uploading to {remote_path}...")
        
        # Change to remote directory
        try:
            sftp.chdir(remote_path)
        except IOError:
            print(f"Remote directory {remote_path} does not exist. Attempting to create it...")
            sftp.mkdir(remote_path)
            sftp.chdir(remote_path)

        for filename in files_to_upload:
            if os.path.exists(filename):
                print(f"Uploading {filename}...")
                sftp.put(filename, filename)
            else:
                print(f"Skipping {filename} (not found locally).")

        sftp.close()
        ssh.close()
        print("\nDeployment successful! Everything is live.")
        
    except Exception as e:
        print(f"\nDeployment failed: {str(e)}")

if __name__ == "__main__":
    deploy()
