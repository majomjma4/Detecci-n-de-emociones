import cv2
from hsemotion_onnx.facial_emotions import HSEmotionRecognizer

recognizer = HSEmotionRecognizer(model_name="enet_b0_8_best_afew")

def detectar_emocion(rostro):
    rostro_rgb = cv2.cvtColor(rostro, cv2.COLOR_BGR2RGB)
    emotion, scores = recognizer.predict_emotions(rostro_rgb, logits=False)
    
    # Retornar solo la emoción principal como string
    if isinstance(emotion, (list, tuple)):
        return emotion[0]
    return emotion
