# code-search-tool
A Python-based file and code search tool with support for recognizing Java annotations, classes, methods, Gradle dependencies, and property-style configurations

# Code Search Tool

This is a lightweight Python tool that recursively scans project directories and lets you search for:
- Java class definitions
- Imports
- Annotations
- Constructors and methods
- Gradle-style dependencies
- Property-style configurations

## 🔍 Features
- Classifies lines by type (e.g., `[Class]`, `[Import]`, `[Gradle]`)
- Ignores directories or files using keywords (`ignore <keyword>`)
- Supports Java and Gradle-specific syntax
- Easy terminal interface

## 🧪 Usage

```bash
python main.py
