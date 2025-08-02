import os
import re
import json

HISTORY_FILE = "update_history.json"
IGNORE_KEYWORDS = []

class FileIndexer:
    def __init__(self, root="."):
        self.root = root

    def build_index(self):
        index = {}
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if not self._is_ignored(os.path.join(root, d))]
            for file in files:
                full_path = os.path.join(root, file)
                if not self._is_ignored(full_path):
                    index[file] = full_path
        return index

    def _is_ignored(self, path):
        return any(keyword in path for keyword in IGNORE_KEYWORDS)

class LineClassifier:
    @staticmethod
    def classify(line):
        stripped = line.strip()
        if re.match(r'^@\w+', stripped):
            return "[Annotation]"
        if re.match(r'^import\s+[\w\.]+\s*;', stripped):
            return "[Import]"
        if re.match(r'^\s*(public\s+)?(final\s+)?(abstract\s+)?class\s+\w+', stripped):
            return "[Class]"
        if re.match(r'^\s*(public|protected|private)?\s+[A-Z]\w*\s*\(.*?\)\s*\{?', stripped):
            return "[Constructor]"
        if re.match(r'^\s*(public|private|protected)?\s*(static\s+)?[\w\<\>\[\]]+\s+\w+\s*\(.*?\)\s*\{?', stripped):
            return "[Function]"
        if re.match(r'^\s*(implementation|api|compile|runtimeOnly|testImplementation|testRuntimeOnly|compileOnly|annotationProcessor|kapt|ksp|provided|detektPlugins|androidTestImplementation|debugImplementation|releaseImplementation)\s+(platform|enforcedPlatform)?\s*[\(\'"]', stripped):
            return "[Gradle]"
        if re.match(r'^\s*[\w\.\-]+\s*=\s*.+', stripped):
            return "[Property]"
        return "[Generic]"

class UpdateLogger:
    def __init__(self, path=HISTORY_FILE):
        self.path = path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        return {"updated": [], "skipped": []}

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record(self, status, match_info):
        if status in self.data:
            self.data[status].append(match_info)
            self.save()

    def already_handled(self, file, line):
        return any(entry['file'] == file and entry['line_content'] == line for entry in self.data['updated'] + self.data['skipped'])

class DependencyManager:
    def __init__(self, file_index, logger):
        self.file_index = file_index
        self.logger = logger

    def search(self, pattern):
        matches = []
        for file, path in self.file_index.items():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines):
                        if pattern in line:
                            matches.append({
                                "file": path,
                                "line_number": idx,
                                "line_content": line.rstrip(),
                                "lines": lines
                            })
            except Exception:
                continue
        return matches

    def edit(self, pattern):
        matches = self.search(pattern)
        if not matches:
            print(f"No match found for '{pattern}'")
            return

        for match in matches:
            file = match["file"]
            idx = match["line_number"]
            line = match["line_content"]
            lines = match["lines"]

            if self.logger.already_handled(file, line):
                print(f"Already handled: {file}, line {idx + 1}")
                continue

            tag = LineClassifier.classify(line)
            print(f"\n{tag} Found in {file}, line {idx + 1}:\n{line}")
            new_line = input("Enter replacement (or press Enter to skip): ").strip()

            if new_line:
                if pattern in line:
                    updated_line = line.replace(pattern, new_line)
                    lines[idx] = updated_line + '\n'
                    with open(file, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    print(f"Updated line {idx + 1} in {file}")
                    self.logger.record("updated", {
                        "file": file,
                        "line_number": idx + 1,
                        "line_content": line,
                        "new_content": updated_line.strip()
                    })
                else:
                    print(f"Pattern '{pattern}' not found in line. Skipping...")
                    self.logger.record("skipped", {
                        "file": file,
                        "line_number": idx + 1,
                        "line_content": line
                    })
            else:
                print("Skipped")
                self.logger.record("skipped", {
                    "file": file,
                    "line_number": idx + 1,
                    "line_content": line
                })

class CLI:
    def __init__(self):
        self.ignore_keywords = set(IGNORE_KEYWORDS)
        self.indexer = FileIndexer()
        self.file_index = self.indexer.build_index()
        self.logger = UpdateLogger()
        self.manager = DependencyManager(self.file_index, self.logger)

    def run(self):
        print("Enter a pattern to search (or use 'edit <pattern>', 'ignore <folder_or_file>' to ignore):")
        while True:
            user_input = input("input: ").strip()
            if not user_input:
                break

            if user_input.startswith("edit "):
                pattern = user_input[len("edit "):].strip()
                self.edit_dependency(pattern)
            elif user_input.startswith("ignore "):
                pattern = user_input[len("ignore "):].strip()
                self.ignore(pattern)
            elif user_input == "reset":
                self.reset_ignore()
            else:
                self.search_only(user_input)

    def ignore(self, pattern):
        self.ignore_keywords.add(pattern)
        print(f"'{pattern}' added to ignore list.")
        IGNORE_KEYWORDS.clear()
        IGNORE_KEYWORDS.extend(self.ignore_keywords)
        self._refresh()

    def reset_ignore(self):
        self.ignore_keywords.clear()
        IGNORE_KEYWORDS.clear()
        print("Ignore list reset.")
        self._refresh()

    def _refresh(self):
        self.indexer = FileIndexer()
        self.file_index = self.indexer.build_index()
        self.manager = DependencyManager(self.file_index, self.logger)

    def search_only(self, pattern):
        if pattern in self.file_index and isinstance(self.file_index[pattern], str):
            print(f"'{pattern}' is a file located at: {self.file_index[pattern]}")
            return

        matches = self.manager.search(pattern)
        if not matches:
            print(f"'{pattern}' not found in any files.")
            return

        for match in matches:
            tag = LineClassifier.classify(match['line_content'])
            print(f" {tag} Found in {match['file']}, line {match['line_number'] + 1}")

    def edit_dependency(self, pattern):
        self.manager.edit(pattern)

if __name__ == "__main__":
    CLI().run()
