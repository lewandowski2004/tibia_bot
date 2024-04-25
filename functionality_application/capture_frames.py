def capture_frames(cap, frame_queue):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nie można odczytać obrazu z kamery")
            break

        if not frame_queue.full():
            frame_queue.put(frame)
        else:
            # Usuń najstarszą ramkę, jeśli kolejka jest pełna
            frame_queue.get()
            frame_queue.put(frame)