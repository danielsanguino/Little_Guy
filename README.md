# Little_Guy
Advanced ML Final Project

My final project group, consisting of myself (Ben Annicelli), Daniel Sanguino, and Ben Blechman, will be working on a model that will recognize if there is a fish in a live video (first phase), and eventually recognize a specific species of fish (final phase). The model will be uploaded to a ground robot (no underwater robot is available). Once the onboard camera recognizes a fish in the frame (we'll likely use a picture of a fish on an iPad or something similar) the motors will be activated and the robot will follow the fish.

Using a pretrained YOLOV11, we created an autonomous ground robot that correctly recognizes fish through a webcam. This webcam sends a feed through our model hosted on a Raspberry Pi which then makes inferences on the images it's fed. If a fish is located, the pi signals the Elegoo Uno R3 to send power to the motors on our robot, in order to track towards the fish it sees. If a fish is not found, the pi will send "no fish" to the console and wait until a fish is found within the view of the camera. Using this model, we were able to complete the first phase of this project and encourage others to attempt to improve our model in order to complete the final phase above.

The model was trained on the DeepFish dataset, which includes 40,000 RGB images of fish in various habitats around coastal Australia.
