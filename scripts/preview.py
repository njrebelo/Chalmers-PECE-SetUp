import picamera

input("You're about to initiate Picam preview, press Enter to contiue")

#Camera Recording
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate=60
camera.start_preview()
input("Press Enter to Stop preview")
camera.stop_preview()

