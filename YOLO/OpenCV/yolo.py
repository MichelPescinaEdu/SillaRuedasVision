import cv2

img = cv2.imread('Images/kite.jpg')

with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

net = cv2.dnn.readNetFromDarknet('yolov4-tiny.cfg', 'yolov4-tiny.weights')

model = cv2.dnn_DetectionModel(net)
model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
videoFlag = True


def imagen():
    classIds, scores, boxes = model.detect(img, confThreshold=0.6, nmsThreshold=0.4)

    for (classId, score, box) in zip(classIds, scores, boxes):
        cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                    color=(0, 0, 255), thickness=2)

        text = '%s: %.2f' % (classes[classId], score)
        cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color=(0, 0, 255), thickness=2)

    height, width, nchannels = img.shape
    if height > 800 or width > 800:
        image = cv2.resize(img, (width//2, height//2), interpolation = cv2.INTER_LINEAR)
        cv2.imshow('Image', image)
    else:
        cv2.imshow('Image', img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def video():
    # capture the video
    cap = cv2.VideoCapture(0)
    # get the video frames' width and height for proper saving of videos
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # create the `VideoWriter()` object
    # out = cv2.VideoWriter('video_result.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

    # detect objects in each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            img = frame
            classIds, scores, boxes = model.detect(img, confThreshold=0.6, nmsThreshold=0.4)
            for (classId, score, box) in zip(classIds, scores, boxes):
                cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                    color=(0, 0, 255), thickness=2)

                text = '%s: %.2f' % (classes[classId], score)
                cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                color=(0, 0, 255), thickness=2)

                height, width, nchannels = img.shape
                image = img
            # out.write(image)
            if height > 800 or width > 800:
                image = cv2.resize(img, (width//2, height//2), interpolation = cv2.INTER_LINEAR)
                cv2.imshow('Image', image)
            else:
                cv2.imshow('Image', img)
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break   
    cap.release()
    cv2.destroyAllWindows()


if videoFlag == True:
    video()
else:
    imagen()