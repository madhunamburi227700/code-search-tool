import os
import re


ignore_keywords = []

def build_file_index(root_dir="."):
    file_index = {}
    for root, dirs, files in os.walk(root_dir):

        dirs[:] = [d for d in dirs if not any(kw in os.path.join(root, d) for kw in ignore_keywords)]
        for file in files:
            full_path = os.path.join(root, file)
            if not any(kw in full_path for kw in ignore_keywords):
                file_index[file] = full_path
    return file_index

def classify_line(line):
    stripped = line.strip()

    # Java annotation
    if re.match(r'^@\w+', stripped):
        return "[Annotation]"

    # Java import
    if re.match(r'^import\s+[\w\.]+\s*;', stripped):
        return "[Import]"

    # Java class
    if re.match(r'^\s*(public\s+)?(final\s+)?(abstract\s+)?class\s+\w+', stripped):
        return "[Class]"

    # Java constructor (no return type, name starts with uppercase letter)
    if re.match(r'^\s*(public|protected|private)?\s+[A-Z]\w*\s*\(.*?\)\s*\{?', stripped):
        return "[Constructor]"

    # Java method/function with return type
    if re.match(r'^\s*(public|private|protected)?\s*(static\s+)?[\w\<\>\[\]]+\s+\w+\s*\(.*?\)\s*\{?', stripped):
        return "[Function]"

    # Gradle-style dependency
    if re.match(r'^\s*(implementation|api|compile|runtimeOnly|testImplementation|testRuntimeOnly|compileOnly|annotationProcessor|kapt|ksp|provided|detektPlugins|androidTestImplementation|debugImplementation|releaseImplementation)\s+(platform|enforcedPlatform)?\s*[\(\'"]', stripped):
        return "[Gradle]"

    # Property-style (like gradle.properties)
    if re.match(r'^\s*[\w\.\-]+\s*=\s*.+', stripped):
        return "[Property]"

    return "[Generic]"

def search_in_files(query, file_index):
    # Direct file match
    if query in file_index:
        return f"'{query}' is a file located at: {file_index[query]}"

    matches = []
    for file_name, path in file_index.items():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for idx, line in enumerate(f, start=1):
                    if query in line:
                        tag = classify_line(line)
                        rel_path = os.path.relpath(path)
                        matches.append(f" {tag} Found in {rel_path}, line {idx}: {line.strip()}")
        except Exception:
            continue

    return "\n".join(matches) if matches else f"'{query}' not found as file or inside any file."

def main():
    global ignore_keywords
    file_index = build_file_index(".")

    print("Enter search pattern (e.g., import java.util.Map;):")

    while True:
        query = input("input: ").strip()
        if not query:
            break

        if query.startswith("ignore "):
            keyword = query[len("ignore "):].strip()
            if keyword:
                ignore_keywords.append(keyword)
                print(f"Ignoring anything with: '{keyword}'")
                file_index = build_file_index(".")
            else:
                print("No keyword provided to ignore.")
            continue

        if query == "reset":
            ignore_keywords = []
            print("Ignore list cleared.")
            file_index = build_file_index(".")
            continue

        result = search_in_files(query, file_index)
        print("output:", result)

if __name__ == "__main__":
    main()
