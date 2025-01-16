import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

def process_file(filename):
    """
    Process a single .crd file to generate .musicxml and .pdf files.
    """
    base_name = os.path.splitext(filename)[0]
    crd_path = os.path.join(os.getcwd(), filename)
    musicxml_path = os.path.join(os.getcwd(), f"{base_name}.musicxml")
    pdf_path = os.path.join(os.getcwd(), f"{base_name}.pdf")

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

def generate_musicxml_and_pdf():
    """
    Generate .musicxml and .pdf files for all .crd files in the current directory,
    skipping files for which these outputs already exist.
    """
    current_directory = os.getcwd()

    # Get all .crd files in the current directory
    crd_files = [f for f in os.listdir(current_directory) if f.endswith('.crd')]

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        executor.map(process_file, crd_files)

if __name__ == "__main__":
    generate_musicxml_and_pdf()
