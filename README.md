# Little_Guy
Advanced ML Final Project

My final project group, consisting of myself (Ben Annicelli), Daniel Sanguino, and Ben Blechman, will be working on a model that will recognize if there is a fish in a live video (first phase), and eventually recognize a specific species of fish (final phase). The model will be uploaded to a ground robot (no underwater robot is available). Once the onboard camera recognizes a fish in the frame (we'll likely use a picture of a fish on an iPad or something similar) the motors will be activated and the robot will follow the fish.

Using a pretrained YOLOV11, we created an autonomous ground robot that correctly recognizes fish through a webcam. This webcam sends a feed through our model hosted on a Raspberry Pi which then makes inferences on the images it's fed. If a fish is located, the pi signals the Elegoo Uno R3 to send power to the motors on our robot, in order to track towards the fish it sees. If a fish is not found, the pi will send "no fish" to the console and wait until a fish is found within the view of the camera. Using this model, we were able to complete the first phase of this project and encourage others to attempt to improve our model in order to complete the final phase above.

The model was trained on the DeepFish dataset, which includes 40,000 RGB images of fish in various habitats around coastal Australia.


Hardware requirement:
  1.) Raspberry Pi 4B and SD card
  2.) ELEGOO UNO R3 (or Arduino UNO R3)
  3.) Standard Dc-Dc motor (two)
  4.) USB Webcam
  5.) ELEGOO Battery pack or equivilent
  6.) Portable battery pack with 5v, 3A output
  7.) ELEGOO Conquerer Tank
  8.) Cables:
        a.) USB - USB B
        b.) USB - Micro HDMI
        c.) USB - USB C


Pi 4B set-up:
  1.) Download Raspberry Pi Imager and follow directions. This will allow easy download for R-Pi operating system
        a.) follow this link: https://www.raspberrypi.com/software/
  2.) Insert SD with operating system into Pi
  3.) Plug Pi into power
  4.) Attach mouse, keyboard, and micro HDMI cable
  5.) Follow built in set up instructions
  6.) Upload Little_Vision.py and best.pt (I reccomend emailing them to yourself)
  7.) Open Pi terminal and navigate to location where you stored Little_Vision.py and best.pt
  8.) Create virtual enviroment using this command: python3 -m venv venv
  9.) Activate enviroment with command: source venv/bin/activate
  10.) pip install requirements found in requirements.txt
  11.) Select Raspberry Pi logo in top left corner, select program, select Thonny
  12.) Make sure you're in regular mode in Thonny
  13.) Select Tools in toolbar, navigate to options, Interpreter, browse, navigate to your venv folder, select bin, select Python3 and continue
  14.) Save!
  15.) Create a Pi connect account
  16.) Open Pi options and enable Pi connect
  17.) Log in on the Pi and add to your devices
  18.) Ensure all dependencies are installed and run once in Thonny as a test

Arduino set-up:
  1.) Download Arduino IDE
        a.) follow this link: https://www.arduino.cc/en/software/
  2.) Open Arduino IE and create a new script
  3.) Paste attached Arduion code / open project in Arduion IDE
  4.) Attach USB-USB B cable into board
  5.) Navigate to board select, select the com port taken by Arduino board and slect board type: Arduino UNO
  6.) Compile and upload code
  7.) Attach USB-USB B cable to Pi 4B USB slot (any)

Data Processing:
  1.) Obtain the DeepFish Dataset or a comparable dataset of labeled fish images.
  2.) Organzie the dataset into a YOLO-compatable directory structure:
      a.) Create images/train, images/val, and images/test folders for the image data
      b.) Create corresponding labels/train, labels/val, and labels/test folders for the annotation files.
  3.) Ensure each image has a matching .txt label file with YOLO-format annotation.
      Each line in a label file should follow the format:
      (class_id, x_center, y_center, width, height) -- all normalized between 0 and 1.
  4.) Resize all image files 416x416 pixels to match the YOLOv11 model's input requirement
  5.) Split the dataset into approximately 80% training, 10% validation, and 10% testing subsets.

Model Training:
  1.) Clone the YOLOv11 repository from the official GitHub source.
  2.) Create a data.yaml file describing the dataset. This file should include:
      a.) The paths to the training and validation image folders.
      b.)The number of object classes (nc) in the dataset.
      c.)A list of class names, in this case: ['fish'].

  3.) Select or customize the YOLOv11 configuration file. The Tiny variant of YOLOv11 is recommended for low-power devices like the Raspberry Pi.
  4.) Set up a Python virtual environment and install all required dependencies as specified in the project's requirements.txt file.
  5.) Launch the training process using the YOLOv11 training script with specified parameters such as input size, batch size, number of epochs, dataset config file, and model config file.
  6.) Upon completion, the trained model weights, including the best-performing checkpoint, will be saved in the runs/train/ directory.
  7.) Transfer the final best.pt model file to the Raspberry Pi to enable live inference on the robot.

Test Process:
  1.) Connect Pi to ELEGOO using USB-USB B
  2.) Connect Pi to battery pack using USB C - USB
  3.) Connect ELEGOO to battery pack using supplied connector
  4.) Connect Webcam to Pi USB port
  5.) Place Robot on ground (or in water)
  6.) Ensure Pi 4B is connected to internet
  7.) Connect to Pi using Raspberry Pi Connect and select connect over shell
  8.) Navigate to folder containing Little_Vision.py and best.pt
  9.) Activate virtual enviroment with this command: source venv/bin/activate
  10.) Activate code using this command: python3 Little_Vision.py
  11.) Watch your bot follow fish
