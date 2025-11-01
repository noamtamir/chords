import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

def process_file(file_path):
    """
    Process a single .crd file to generate .musicxml and .pdf files.
    """
    # Convert to absolute path
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)
    
    # Get the directory and filename
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    
    crd_path = file_path
    musicxml_path = os.path.join(directory, f"{base_name}.musicxml")
    pdf_path = os.path.join(directory, f"{base_name}.pdf")

    # Check if .musicxml file exists, if not, create it
    if not os.path.exists(musicxml_path):
        print(f"Generating .musicxml for '{filename}'...")
        try:
            with open(musicxml_path, 'w') as musicxml_file:
                subprocess.run(["txt2musicxml"], stdin=open(crd_path), stdout=musicxml_file, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error generating .musicxml for '{filename}': {e}")
            return
    else:
        print(f".musicxml file for '{filename}' already exists. Skipping generation.")

    # Check if .pdf file exists, if not and .musicxml exists, create it
    if not os.path.exists(pdf_path) and os.path.exists(musicxml_path):
        print(f"Generating .pdf for '{filename}'...")
        try:
            subprocess.run(["mscore", musicxml_path, "-o", pdf_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error generating .pdf for '{filename}': {e}")
    elif os.path.exists(pdf_path):
        print(f".pdf file for '{filename}' already exists. Skipping generation.")
    else:
        print(f".musicxml file for '{filename}' was not created. Cannot generate .pdf.")

def generate_musicxml_and_pdf(path_arg=None):
    """
    Generate .musicxml and .pdf files for .crd files based on the provided path.
    
    Args:
        path_arg: Path to process. Can be:
            - "." or None: process all .crd files in current directory
            - A directory: process all .crd files in that directory (non-recursive)
            - A file: process that specific file
    """
    if path_arg is None or path_arg == ".":
        # Process all .crd files in current directory
        target_directory = os.getcwd()
        crd_files = [os.path.join(target_directory, f) 
                    for f in os.listdir(target_directory) 
                    if f.endswith('.crd') and os.path.isfile(os.path.join(target_directory, f))]
    else:
        # Convert to absolute path
        abs_path = os.path.abspath(path_arg)
        
        if os.path.isdir(abs_path):
            # Process all .crd files in the specified directory (non-recursive)
            crd_files = [os.path.join(abs_path, f) 
                        for f in os.listdir(abs_path) 
                        if f.endswith('.crd') and os.path.isfile(os.path.join(abs_path, f))]
        elif os.path.isfile(abs_path):
            # Process the single file
            if abs_path.endswith('.crd'):
                crd_files = [abs_path]
            else:
                print(f"Error: '{path_arg}' is not a .crd file.")
                return
        else:
            print(f"Error: '{path_arg}' does not exist.")
            return
    
    if not crd_files:
        print("No .crd files found to process.")
        return
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        executor.map(process_file, crd_files)

if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_musicxml_and_pdf(path_arg)
