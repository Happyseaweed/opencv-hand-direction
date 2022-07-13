# opencv-hand-direction

In order for program to work optimally, palm should be facing the camera. Computing power of machine greatly affects accuracy.

A simple (not yet super accurate) python program that detects which direction the hands move in after pinching/grabbing. Can be used for hands-free control.

Created this as I wanted to build a hands-free OS. There are a few problems I ran into: my camera does not capture fast enough so the hand_landmarks sort of jitter all over the place,
decreasing overall accuracy. The camera also does not auto focus.

## How it works (Roughly :P)
When the user pinches their hand and move it in any direction (up, down, left, right), the direction will be calculated and printed to the console/terminal.

If you have any feedback/suggestions please let me know! They would be greatly appreciated!
