import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Não foi possível abrir a câmera.")
    exit()

print("✅ Câmera aberta. Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Falha ao capturar o frame.")
        break

    cv2.imshow("Câmera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
