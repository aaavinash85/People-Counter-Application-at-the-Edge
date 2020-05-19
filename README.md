# Deploying a People Counter Application at the Edge

The people counter application demonstrates how to create a smart video IoT solution using Intel® hardware and software tools. The app will detect people in a designated area, providing the number of people in the frame, average duration of people in frame, and total count. This project is a part of Intel Edge AI for IOT Developers Nanodegree program by udacity.


![screenshot_1](https://user-images.githubusercontent.com/34116562/80679006-ab9dc000-8ad9-11ea-9756-1fdb898276b2.png)


### How it works?

The counter will use the Inference Engine included in the Intel® Distribution of OpenVINO™ Toolkit. The model used should be able to identify people in a video frame. The application should count the number of people in the current frame, the duration that a person is in the frame (time elapsed between entering and exiting a frame) and the total count of people. It then sends the data to a local web server using the Paho MQTT Python package.


![architectural diagram](./images/arch_diagram.png)


## Requirements

#### Hardware

* 6th to 10th generation Intel® Core™ processor with Iris® Pro graphics or Intel® HD Graphics.
* OR use of Intel® Neural Compute Stick 2 (NCS2)

#### Software

*   Intel® Distribution of OpenVINO™ toolkit 2019 R3 release
*   Node v6.17.1
*   Npm v3.10.10
*   CMake
*   MQTT Mosca server
*   Python 3.5 or 3.6
  
  
### Explaining Model Selection & Custom Layers
 
TensorFlow Object Detection Model Zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) contains many pre-trained models on the coco dataset. Ssd_inception_v2_coco and faster_rcnn_inception_v2_coco performed good as compared to rest of the models, but, in this project, faster_rcnn_inception_v2_coco is used which is fast in detecting people with less errors. Intel openVINO already contains extensions for custom layers used in TensorFlow Object Detection Model Zoo.

Downloading the model from the GitHub repository of Tensorflow Object Detection Model Zoo by the following command:

```
wget http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
```
Extracting the tar.gz file by the following command:

```
tar -xvf faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
```
Changing the directory to the extracted folder of the downloaded model:

```
cd faster_rcnn_inception_v2_coco_2018_01_28
```
The model can't be the existing models provided by Intel. So, converting the TensorFlow model to Intermediate Representation (IR) or OpenVINO IR format. The command used is given below:

```
python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json
```

## Comparing Model Performance
   There is huge difference on running Plain model and on OpenVino

### Model-1: Ssd_inception_v2_coco_2018_01_28(OpenVINO)          |  Ssd_inception_v2_coco_2018_01_28(Tensorflow)
                                                                 |
#### Latency(microseconds) = 115                                 |  Latency(microseconds) = 222
#### Memory(mb) = 329                                            |  Memory(mb) = 538
	                                                             |
### Model-2: Faster_rcnn_inception_v2_coco_2018_01_289(OpenVINO) |  Faster_rcnn_inception_v2_coco_2018_01_289(Tensorflow)
                                                                 |
#### Latency(microseconds) = 889                                 |  Latency(microseconds) = 1281
#### Memory(mb) = 281                                            |  Memory(mb) = 562


##### Differences in Edge and Cloud computing

Edge Computing is regarded as ideal for operations with extreme latency concerns. Thus, medium scale companies that have budget limitations can use edge computing to save financial resources. Cloud Computing is more suitable for projects and organizations which deal with massive data storage. 

### Model Use Cases

This application could keep a check on the number of people in a particular area and could be helpful where there is restriction on the number of people present in a particular area. Further, with some updations, this could also prove helpful in the current COVID-19 scenario i.e. to keep a check on the number of people in the frame.

### Effects on End user needs

Various insights could be drawn on the model by testing it with different videos and analyzing the model performance on low light input videos. This would be an important factor in determining the best model for the given scenario.

### Running the Main Application

After converting the downloaded model to the OpenVINO IR, all the three servers can be started on separate terminals i.e. 

-   MQTT Mosca server 
-   Node.js* Web server
-   FFmpeg server


#### Setting up the environment

Configuring the environment to use the Intel® Distribution of OpenVINO™ toolkit one time per session by running the following command:
```
source /opt/intel/openvino/bin/setupvars.sh -pyver 3.5
```

Further, from the main directory:

#### Step 1 - Start the Mosca server

```
cd webservice/server/node-server
node ./server.js
```

The following message is displayed, if successful:
```
Mosca server started.
```

#### Step 2 - Start the GUI

Opening new terminal and executing below commands:
```
cd webservice/ui
npm run dev
```

The following message is displayed, if successful:
```
webpack: Compiled successfully
```

#### Step 3 - FFmpeg Server

Opening new terminal and executing below command:
```
sudo ffserver -f ./ffmpeg/server.conf
```

#### Step 4 - Run the code

Opening new terminal and executing below command:
```
python main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
```
