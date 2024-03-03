from loader import LocalUploader
import time
uploader = LocalUploader()

start = time.time()
for _ in range(2):
    uploader.copy_files(force_copy=False)
end = time.time()
duration = end - start
print(f"Temps d'exécution avec full Threading : {duration} secondes")

