import matplotlib.pyplot as plt
import pandas as pd

# Change this for each mAP directory
mAPdir = ['Yolo_V4/Yolo_V4_mAP', 'Yolo_V7/Yolo_V7_mAP', 'ResNet/ResNet_mAP']
models = ['Yolo V4', 'Yolo V7', 'ResNet']

cameras = ['iDS', 'PerfectChoice', 'Realsense']
linestyles = [
    {'iDS':'o-b', 'PerfectChoice':'o:b', 'Realsense':'o--b'},
    {'iDS':'o-m', 'PerfectChoice':'o:m', 'Realsense':'o--m'},
    {'iDS':'o-g', 'PerfectChoice':'o:g', 'Realsense':'o--g'}
              ]
all_linestyles = {
    'Yolo V4 iDS':'o-b', 'Yolo V4 PerfectChoice':'o:b', 'Yolo V4 Realsense':'o--b',
    'Yolo V7 iDS':'o-m', 'Yolo V7 PerfectChoice':'o:m', 'Yolo V7 Realsense':'o--m',
    'ResNet iDS':'o-g', 'ResNet PerfectChoice':'o:g', 'ResNet Realsense':'o--g'
    }
data = {'IoU Threshold':[0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]}

mAP = pd.DataFrame(data)
all_mAP = pd.DataFrame(data)

# Draws mAP plots for each model individually and all of them at the same time.
for i in range(0, len(mAPdir)):
    mAP = pd.DataFrame(data)
    for camera in cameras:
        path = mAPdir[i] + '/' + camera + ".txt"
        current_mAP = pd.read_csv(path, header=None, names=['IoU Threshold',camera])
        extract = current_mAP[camera]
        mAP.insert(1, camera, extract)
        all_mAP.insert(1, models[i]+" "+camera, extract)
    mAP.plot(x="IoU Threshold", ylabel="mAP",xlim=(0.5, 1.0), ylim=(0.0,1.0), title=models[i], style=linestyles[i])
    plt.show()
all_mAP.plot(x="IoU Threshold", ylabel="mAP",xlim=(0.5, 1.0), ylim=(0.0,1.0), title="Todos los modelos", style=all_linestyles)
plt.show()
print(all_mAP.sum()/len(all_mAP.index))