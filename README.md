# Chords

This repository holds a bunch of .crd files of different songs, together with .musixml files generated with txt2musicxml, and .pdf files generated with mscore.

It includes a simple script to generate `.musicxml` and `.pdf` files from `.crd` chord files.

## Prerequisites

- Python 3
- `txt2musicxml` command-line tool
- `mscore` (MuseScore) command-line tool

## Usage

Run the script with:

```bash
python generate_files.py [path]
```

### Examples

```bash
# Process all .crd files in the current directory
python generate_files.py
python generate_files.py .

# Process all .crd files in a specific directory
python generate_files.py /path/to/directory

# Process a specific file
python generate_files.py song.crd
```

The script will generate `.musicxml` and `.pdf` files in the same directory as the input `.crd` files, skipping files that already have outputs.

