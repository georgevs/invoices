import os


def scandir(folder_path):
  folder_paths = [folder_path]
  while folder_paths:
    folder_path = folder_paths.pop()
    with os.scandir(folder_path) as entries:
      for entry in entries:
        if entry.is_dir():
          folder_paths.append(entry.path)
        else:
          yield entry.path 
