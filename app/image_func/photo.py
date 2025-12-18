import os 
import uuid

def save_image(file):
  ext = file.filename.split(".")[-1]
  filename = f"{uuid.uuid4()}.{ext}"
  mkdir = 'uploads'
  os.makedirs(mkdir, exist_ok=True)
  path = os.path.join(mkdir, filename)

  file.save(path)
  return f"/uploads/{filename}"
