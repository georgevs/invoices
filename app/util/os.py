import os


def scandir(folder_path, recursive=True):
  folder_paths = [folder_path]
  while folder_paths:
    folder_path = folder_paths.pop()
    with os.scandir(folder_path) as entries:
      for entry in entries:
        if entry.is_dir():
          if recursive:
            folder_paths.append(entry.path)
        else:
          yield entry.path 

def has_ext(*exts):
  return lambda file_path: os.path.splitext(file_path)[1] in exts