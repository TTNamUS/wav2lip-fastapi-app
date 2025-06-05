import base64
import tempfile
import os
import shutil

def save_temp_file(base64_data, file_type):
    if file_type == "img":
        ext = "png" if "png" in base64_data else "jpg"
    else:
        ext = "wav" if "wav" in base64_data else "mp3"
    _, encoded = base64_data.split(",", 1)
    file_bytes = base64.b64decode(encoded)
    fd, path = tempfile.mkstemp(suffix=f".{ext}")
    with os.fdopen(fd, "wb") as f:
        f.write(file_bytes)
    return path

def remove_files(paths, remove_dirs=False): 
    for p in paths:
        try:
            if remove_dirs:
                output_dir = os.path.dirname(p)
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
            else:
                if os.path.isfile(p):
                    os.remove(p)
        except Exception:
            pass