from deepface import DeepFace


img_path = "sampe.png"

result = DeepFace.analyze(img_path, actions=['emotion'])
print("Detected Emotions:")
print(result["emotion"])
