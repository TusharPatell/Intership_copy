import cv2
import os
from ultralytics import YOLO
# from werkzeug.utils import secure_filename
from base import app

OUTPUT_PATH = 'base/static/outputs/'
app.config['OUTPUT_FOLDER'] = OUTPUT_PATH

def perform_inference(model_name, infer_file):
    try:
        get_file = os.path.join(app.config['UPLOAD_FOLDER'], infer_file)
        save_outputs = os.path.join(app.config['OUTPUT_FOLDER'], infer_file)
        print(save_outputs)
        
        model_path=f'base/static/models/{model_name}.pt'
        model = YOLO(model_path)
        print(model_path)
        print(model.names)
        
        if get_file.endswith(('.jpg', '.png', '.jpeg')):
            img = cv2.imread(get_file)
            results = model.predict(img)
            count = len(results[0])
            # pothole_count = 0
            annoted = results[0].plot()
            cv2.imwrite(save_outputs, annoted)
            # return garbage_count, pothole_count
            return count
            
        elif get_file.endswith(('.mp4', '.mov', '.avi')):
            cap = cv2.VideoCapture(get_file)
            # Get video properties (fps, width, height)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'avc1')  # You can change the codec based on your needs
            out = cv2.VideoWriter(save_outputs, fourcc, 1, (width, height))
            
            count = 0  # Total count across all frames
            # Calculate frame interval to achieve desired frame rate (1 frame per second)
            frame_interval = int(fps)  # Adjust if needed    
            frame_number = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                frame_number += 1
                # Skip frames if frame number is not multiple of frame interval
                if frame_number % frame_interval != 0:
                    continue
                
                # Prediction logic
                results = model.predict(frame)
                frame_count = len(results[0])
                count += frame_count
                annoted_frame = results[0].plot()
                
                out.write(annoted_frame) 
                
            cap.release()
            out.release()
            
            return count
        else:
            raise ValueError('Unsupported file.')  
        
    except Exception as e:
        print(f'An error occured: {e}')      
                
    
    
    
    