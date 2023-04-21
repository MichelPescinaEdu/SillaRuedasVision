clear
clc

IoUthresh = 0.5;
minConf = 0.3;

count = 1;
mAP = 0;
directory = 'Yolo_V7_IoU'
mAPdirectory = 'Yolo_V7_mAP'
cameras = [
  'Realsense',
  'iDS',
  'PerfectChoice'
  ];
extension = '.csv';
total_classes = 0;

%Matriz de objetos
objects = [
    'person',
    'bicycle',
    'car',
    'motorbike',
    'aeroplane',
    'bus',
    'train',
    'truck',
    'boat',
    'traffic light',
    'fire hydrant',
    'stop sign',
    'parking meter',
    'bench',
    'bird',
    'cat',
    'dog',
    'horse',
    'sheep',
    'cow',
    'elephant',
    'bear',
    'zebra',
    'giraffe',
    'backpack',
    'umbrella',
    'handbag',
    'tie',
    'suitcase',
    'frisbee',
    'skis',
    'snowboard',
    'sports ball',
    'kite',
    'baseball bat',
    'baseball glove',
    'skateboard',
    'surfboard',
    'tennis racket',
    'bottle',
    'wine glass',
    'cup',
    'fork',
    'knife',
    'spoon',
    'bowl',
    'banana',
    'apple',
    'sandwich',
    'orange',
    'broccoli',
    'carrot',
    'hot dog',
    'pizza',
    'donut',
    'cake',
    'chair',
    'sofa',
    'pottedplant',
    'bed',
    'diningtable',
    'toilet',
    'tvmonitor',
    'laptop',
    'mouse',
    'remote',
    'keyboard',
    'cell phone',
    'microwave',
    'oven',
    'toaster',
    'sink',
    'refrigerator',
    'book',
    'clock',
    'vase',
    'scissors',
    'teddy bear',
    'hair drier',
    'toothbrush'
          ];         

mAPaccum=0; 

for camIndex = 1 : 3
  mAPfile = strcat(mAPdirectory,'\',cameras(camIndex,:),'.txt');
  fid = fopen (mAPfile, "w");
  printf("\n\n\n ---------%s------------", mAPfile);
  for threshIndex = 0 : 9
    mAPaccum=0; 
    total_classes = 0;
    IoUthresh = 0.5 + (threshIndex * 0.05);
    printf("THRESHOLD: %f\n\n", IoUthresh);
    for i = 1 : 80
      direccion = strcat(directory,'\',cameras(camIndex,:),'\',objects(i,:),extension);
      disp(direccion);
      if isfile(direccion)
        fprintf('Object: %s\n',objects(i,:));
        total_classes += 1;
        data = csvread(direccion);
        data = data(1:end,:)';
        AP = averagePrec(data, IoUthresh, minConf)
        mAPaccum = mAPaccum + AP;
        disp(' ');
        disp(' ');
        disp(' ');
      end
    endfor
    mAP = mAPaccum/total_classes
    fprintf(fid,"%f,%f\n", IoUthresh, mAP);
    disp(' ');
    disp(' ');
    disp(' ');
  endfor
  fclose(fid);
endfor



%{
  direccion = strcat(camera,'\',objects(6,:),extension)
  data = csvread(direccion);
  data = data(2:end,:)';
  AP = averagePrec(data, IoUthresh, minConf)
  
  %}