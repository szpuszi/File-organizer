# File Organizer

Modern application for automatic file sorting with a graphical user interface.

## Features

- Automatic file sorting by extensions
- Modern graphical user interface (GUI)
- Support for multiple file categories:
  - Documents (PDF, DOC, TXT, etc.)
  - Images (JPG, PNG, GIF, etc.)
  - Audio (MP3, WAV, FLAC, etc.)
  - Video (MP4, AVI, MKV, etc.)
  - Archives (ZIP, RAR, 7Z, etc.)
  - Executables (EXE, MSI)
  - Programming files (PY, JAVA, CPP, etc.)
  - Other files
- Automatic category folder creation
- Duplicate file handling
- Empty folder cleanup
- Real-time operation status

## Requirements

- Python 3.8 or newer
- PySide6 (Qt for Python)

## Installation

1. Clone the repository
2. Install required libraries:
```bash
pip install PySide6
```

## Usage

1. Run the program:
```bash
python file_organizer.py
```

2. In the program interface:
   - Click "Browse" to select a folder to sort
   - Click "Sort Files" to start sorting
   - Monitor progress in the status window

## How It Works

1. Program scans the selected folder and its subfolders
2. Creates category folders (if they don't exist)
3. Moves files to appropriate folders based on extensions
4. Automatically resolves filename conflicts
5. Removes empty folders after completion

## Supported File Extensions

### Documents
- .pdf, .doc, .docx, .txt, .rtf, .odt

### Images
- .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp

### Audio
- .mp3, .wav, .flac, .m4a, .aac

### Video
- .mp4, .avi, .mkv, .mov, .wmv

### Archives
- .zip, .rar, .7z, .tar, .gz

### Executables
- .exe, .msi

### Programming Files
- .py, .java, .cpp, .c, .html, .css, .js

## Security Features

- Folder permission checking
- Error and exception handling
- Safe file moving
- Data loss prevention

## Contributing

Feel free to submit issues and enhancement requests!

## Credits

Created by [szpuszi](https://github.com/szpuszi)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
