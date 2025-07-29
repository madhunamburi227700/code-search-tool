# 🔍 Code Pattern Recognition and File Search Tool (Java / Gradle Projects)

This tool scans a given codebase and helps identify patterns like:
- Java classes, functions, imports, constructors
- Gradle dependencies and properties
- Annotations
- Specific file names or text content

You can also **ignore folders**, **reset the ignored list**, and see **file paths and line numbers**,and **GLOBALLY WE CAN IGNORE **, where matches are found.

## 🛠️ How to Run

### Requirements:
- Python 3.7+

### Steps:
```bash
# Clone the repository
https://github.com/madhunamburi227700/code-search-tool.git
cd <code-search-tool>
cd <my_app>
code .

# Run the script
python my_app\main.py
```

---
## 📥 Input You Can Give to Chatbot (When It Runs)

| Type                     | Example Input                              | What It Does                                     |
|--------------------------|--------------------------------------------|------------------------------------------------- |
| **File Name**            | `Main.java`                                | Finds the exact file and shows its full path     |
| **Java Import**          | `import java.util.List;`                   | Matches Java `import` statements                 |
| **Java Class**           | `public class`                             | Finds class definitions                          |
| **Java Constructor**     | `MyService(`                               | Matches constructor definitions                  |
| **Java Function**        | `public String getName()`                  | Matches function or method lines                 |
| **Gradle Dependency**    | `implementation 'org.apache.commons'`      | Finds Gradle dependencies in `build.gradle`      |
| **Gradle Property**      | `version=1.0.0`                            | Matches key-value settings in`gradle.properties` |
| **Annotation**           | `@SpringBootApplication`                   | Finds annotations starting with `@`              |
| **Ignore Folder**        | `ignore build`                             | Skips scanning that folder or any file within it |
| **Reset Ignore List**    | `reset`                                    | Clears the ignore list and re-indexes all folders|

---

## 🔁 Supported Operations

| Operation              | Description                                                             |
|------------------------|-------------------------------------------------------------------------|
| File name lookup       | Finds file by exact name and shows its location                         |
| Pattern recognition    | Classifies Java/Gradle lines as: `[Import]`, `[Class]`, `[Gradle]`, etc.|
| Keyword search         | Matches exact text inside any file line                                 |
| Folder exclusion       | Skip specific folders during scanning (`ignore <folder>`)               |
| Reset ignore list      | Remove all ignore rules (`reset`)                                       |

---

## 📤 Output Format

When a match is found, you’ll get output like:

```text
[<Type>] Found in <relative_path>, line <line_number>: <matched line>
```

Example:
```
[Gradle] Found in build.gradle, line 10: implementation 'org.apache.commons:commons-lang3:3.12.0'
```

If no match is found:
```
'input' not found as file or inside any file.
```

---

## 🧪 Example Use Cases

### 1. Search a file:
```
input: Main.java
output: 'Main.java' is a file located at: src/main/java/Main.java
```

### 2. Find a Gradle dependency:
```
input: implementation 'com.google.guava'
output: [Gradle] Found in build.gradle, line 14: implementation 'com.google.guava:guava:30.1.1-jre'
```

### 3. Search Java class:
```
input: public class
output: [Class] Found in src/UserService.java, line 3: public class UserService {
```

### 4. Match property:
```
input: minSdkVersion=21
output: [Property] Found in gradle.properties, line 2: minSdkVersion=21
```

### 5. Ignore a folder:
```
input: ignore build
output: Ignoring anything with: 'build'
```

### 6. Reset all ignore rules:
```
input: reset
output: Ignore list cleared.
```

---

## 🔍 Internally Recognized Patterns

| Pattern Type   | Regex Matching (Simplified)                          |
|----------------|------------------------------------------------------|
| Import         | `^import ...;`                                       |
| Class          | `class ClassName`                                    |
| Function       | `public String getName()`                            |
| Constructor    | `public ClassName(...) {`                            |
| Gradle         | `implementation 'group:name:version'`                |
| Property       | `key=value`                                          |
| Annotation     | `@Something`                                         |
| Generic        | Any other line not matching known patterns           |

---

## 📁 Example Folder Structure

```
project-root/
│
├── src/
│   └── Main.java
├── build.gradle
├── gradle.properties
└── my_app
     └── Main.py
```

---

## ✨ Example Interaction

```text
input: @Service
output: [Annotation] Found in service/UserService.java, line 1: @Service
```

```text
input: ignore build
output: Ignoring anything with: 'build'
```

---

## 🔁 Rebuilding Index

After adding/removing ignore folders or resetting, the tool rebuilds the file index for fast scanning.

---

## 📄 License

MIT License – Free for personal and commercial use.
