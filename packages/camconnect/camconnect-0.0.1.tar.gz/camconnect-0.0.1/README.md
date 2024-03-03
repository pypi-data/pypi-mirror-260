# Camconnect

Simple interface for connect and display the video stream from a camera.

Developed by Aimar Abimayu Pratama (c) 2024

## Installation

```bash
pip install camconnect
```

## How To Use

```python
from camconnect import WindowCamera
import cv2

WindowCamera(cv2.VideoCapture(0), filename="output.jpg", width=640, height=480)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.