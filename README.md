# Advanced File Search GUI for Windows

An intuitive desktop application built with Python and Tkinter that allows users to perform advanced searches for files within a selected directory on Windows. Search by filename or file content, filter by common file types, and export the results.

![File Search Main Window](https://github.com/user-attachments/assets/f9058f91-06bb-4a47-83a1-0b6a70d3750d)
*The main application interface.*

![File Search Results Example](https://github.com/user-attachments/assets/a0620300-5266-4b5c-87ce-c10314197ddc)
*The search results interface.*

---

## Key Features

*   **Flexible Search Modes:** Search for a keyword within file names or dive deep by searching within the text content of files.
*   **Content-Aware Searching:** Reads content from various file formats, including:
    *   Plain Text (`.txt`, `.log`, `.csv`, `.md`, etc.)
    *   PDF Files (`.pdf`)
    *   Microsoft Word Documents (`.docx`)
    *   Microsoft Excel Spreadsheets (`.xlsx`)
*   **Multi-Select File Filters:** Easily filter searches by checking categories like Office Documents, PDFs, Text Files, Images, and more.
*   **Responsive UI:** A background threading model ensures the application remains responsive, even during long searches on large directories.
*   **Cancel Functionality:** Abort a long-running search at any time with a dedicated "Cancel" button.
*   **Export Results:** Save your search results to a `.csv` or `.txt` file for later use.
*   **Live Results Counter:** See the number of files found in real-time as the search progresses.
*   **Windows Search Integration Awareness:** A status bar indicator shows whether the underlying Windows Search service is available, providing insight into system search performance.


---

## Technology Stack

*   **Platform:** Windows
*   **Language:** Python 3
*   **GUI Framework:** Tkinter (standard library)
*   **Core Libraries:**
    *   `PyPDF2`: For reading content from PDF files.
    *   `python-docx`: For reading content from `.docx` Word files.
    *   `openpyxl`: For reading content from `.xlsx` Excel files.
    *   `psutil`: For checking the status of the Windows Search service.

---

## Getting Started

Follow these instructions to set up and run the project on your Windows machine.

### Prerequisites

*   Developed and tested on **Python 3.12.10**.
    *   *Should be compatible with Python 3.8 or newer, but 3.12.10 is the confirmed version.*
*   An operating system with PowerShell (e.g., Windows 10, Windows 11).

### Installation & Setup

1.  **Clone the repository:**
    Open PowerShell or Windows Terminal and navigate to the directory where you want to store the project.
    ```bash
    git clone https://your-repository-url.git
    cd your-project-folder
    ```

2.  **Create and activate a virtual environment:**
    *   This keeps the project's dependencies isolated from your system. In the project folder, run:

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
    *   **Note:** If you get an error about script execution being disabled, run the following command first, then try activating again. This policy change only affects the current terminal session.
        ```powershell
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
        ```

3.  **Install the required packages:**
    *   With the virtual environment active, use the `requirements.txt` file to install all necessary libraries.
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run

With your virtual environment activated, run the `main.py` script to launch the application:

```bash
python main.py

## Project Structure

FileSearch/
|
├── .venv/                      # Python virtual environment
├── app/                        # Main application package
│   ├── ui/                     # GUI components
│   │   └── main_window.py
│   ├── search/                 # Search logic and workers
│   │   └── search_worker.py
│   └── utils/                  # Configuration and utilities
│       └── config.py
|
├── main.py                     # Main entry point to launch the app
├── requirements.txt            # Project dependencies
└── readme.md                   # This file
