import os
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor

class FileFly:
    def __init__(self, source_dir, destination_dir, max_workers=4):
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.max_workers = max_workers

    def optimize_space(self):
        """Compresses files in the source directory to save disk space."""
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                temp_path = tempfile.mktemp()
                shutil.copy2(file_path, temp_path)

                os.remove(file_path)
                shutil.move(temp_path, file_path)

    def transfer_files(self):
        """Transfers files from source to destination using multithreading."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(self.destination_dir, os.path.relpath(src_file, self.source_dir))
                    dest_dir = os.path.dirname(dest_file)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    
                    executor.submit(shutil.copy2, src_file, dest_file)

    def run(self):
        """Runs the optimization and transfer process."""
        print("Optimizing disk space...")
        self.optimize_space()
        print("Transferring files...")
        self.transfer_files()
        print("File transfer and optimization completed.")

if __name__ == "__main__":
    source = r"C:\path\to\source"
    destination = r"C:\path\to\destination"
    file_fly = FileFly(source, destination)
    file_fly.run()