class FileSystem:
    def __init__(self):
        self.files = {}
        self.directories = set()
        
    def create_file(self, path, content):
        if path in self.files:
            return "ERROR"
        else:
            self.files[path] = content
            pieces = path.split("/")
            rebuilt_path = ""
            for i in range(len(pieces) - 1):
                if pieces[i]:
                    rebuilt_path += "/" + pieces[i]
                if rebuilt_path and rebuilt_path not in self.directories:
                    self.directories.add(rebuilt_path)
            return "OK"
        
    def read_file(self, path):
        res = self.files.get(path)
        return "ERROR" if res is None else res
        
    def delete_file(self, path):
        res = self.files.pop(path, None)
        return "ERROR" if res is None else "OK"
        
    def list_files(self):
        sorted_files = sorted(self.files.keys())
        return sorted_files
    
    def create_dir(self, path):
        if path in self.directories:
            return "ERROR"
        else:
            self.directories.add(path)
            return "OK"
        
    def list(self, path):
        if path not in self.directories:
            return "ERROR"
        
        children = set()
        for file_path in self.files.keys():
            if file_path.startswith(path + "/"):
                trimmed = file_path[len(path):]
                if trimmed.count("/") == 1:
                    children.add(file_path)
            
        for directory_path in self.directories:
            if directory_path.startswith(path + "/"):
                trimmed = directory_path[len(path):]
                if trimmed.count("/") == 1:
                    children.add(directory_path)
        
        return sorted(children)
        
    def move(self, source, dest):
        if source not in self.files.keys() or dest in self.files.keys():
            return "ERROR"

        self.files[dest] = self.files.get(source)
        self.files.pop(source, None)
        return "OK"
    
    def execute(self, command):
        parts = command.split()
        cmd = parts[0]
        
        if cmd == "CREATE_FILE":
            return self.create_file(parts[1], parts[2])
        elif cmd == "READ_FILE":
            return self.read_file(parts[1])
        elif cmd == "DELETE_FILE":
            return self.delete_file(parts[1])
        elif cmd == "LIST_FILES":
            return self.list_files()
        elif cmd == "CREATE_DIR":
            return self.create_dir(parts[1])
        elif cmd == "LIST":
            return self.list(parts[1])
        elif cmd == "MOVE":
            return self.move(parts[1], parts[2])
        else:
            return "The command you entered does not exist."