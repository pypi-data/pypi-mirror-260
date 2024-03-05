# Camconnect

Simple interface for connect, display, and interaction with the camera.

## Installation

```bash
pip install camconnect
```

## How To Use

### Window for Capture Image
```python
from camconnect import CaptureImage
import cv2

CaptureImage(cv2.VideoCapture(0), 
             filename="output.jpg", 
             width=480, height=320, 
             window_name="Capture Image", 
             filename="captured_image.jpg").run()
```
### Window for Record Video
```python
from camconnect import RecordVideo
import cv2

RecordVideo(cv2.VideoCapture(0), 
            filename="output.jpg", 
            width=480, height=320, 
            window_name="Record Video", 
            filename="recorded_video.avi").run()
```
### Window for Predict Image
```python
from camconnect import PredictImage
import cv2

PredictImage(cv2.VideoCapture(0), 
             filename="output.jpg", 
             width=480, height=320,
             save_image=True,
             window_name="Predict Image", 
             inference_model=inference_model).run()
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Developed by Aimar Abimayu Pratama (c) 2024