# DocsToNotebookLLM

[![GitHub](https://img.shields.io/github/license/AMTilts/docsToNotebookLM)](https://github.com/AMTilts/docsToNotebookLM/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/AMTilts/docsToNotebookLM)](https://github.com/AMTilts/docsToNotebookLM/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/AMTilts/docsToNotebookLM)](https://github.com/AMTilts/docsToNotebookLM/issues)

---

## Overview

**DocsToNotebookLLM** is a **Work-In-Progress** Python project aimed at facilitating seamless conversion of `.com` files into a format accepted by [Notebook LLM](https://github.com/AMTilts/notebookLLM), such as PDFs. 

This tool automates the process of scraping `.com` files, converting them into structured documents, and formatting them for consumption by Notebook LLM. Although still in development, the project holds significant potential for improving workflow efficiency for users of large language models and AI-driven notebooks.

---

## Features (Planned & Implemented)

- 🚀 **Scrape `.com` Files**: Extract structured content from `.com` files.
- 📄 **PDF Conversion**: Automatically generate PDF documents from the scraped content.
- 🤖 **Notebook LLM Compatibility**: Ensure the output meets Notebook LLM's formatting requirements.
- ⚙️ **Extensibility**: Modular design for future enhancements and integrations.

---

## Current Status

This project is currently on hold as I am focused on completing another AI-related project. The implementation of core features is incomplete, and there are known issues that need to be addressed before achieving full functionality.

Planned updates and fixes will resume after the completion of my primary project.

---

## Issues & Challenges

### Known Issues
1. ❌ **Incomplete PDF Formatting**: PDF output does not fully meet Notebook LLM's requirements.
2. ❌ **Error Handling**: Limited error handling during the scraping and conversion process.
3. ❌ **Code Optimizations**: Refactoring and performance tuning are needed.

### Future Enhancements
- ✅ Improve error handling and logging.
- ✅ Add support for more file formats beyond `.com`.
- ✅ Develop a user-friendly CLI or GUI.
- ✅ Optimize scraping algorithms for large datasets.

---

## Installation (Coming Soon)

A detailed installation guide will be provided once the project is ready for release.

---

## Usage (Planned)

```bash
# Clone the repository
git clone https://github.com/AMTilts/docsToNotebookLM.git

# Navigate to the project directory
cd docsToNotebookLM

# Run the script (example)
python scrape_convert.py input_file.com output.pdf
