import os 
import uuid

def save_image(file):
  ext = file.filename.split(".")[-1]
  filename = f"{uuid.uuid4()}.{ext}"
  mkdir = 'uploads'
  path = os.path.join(f'/{mkdir}', filename)

  file.save(path)
  return f"/uploads/{filename}"
