# FSCognitive

![image](https://a2ua.com/cognitive/cognitive-004.jpg)

FSCognitive is an IoT project which demonstrates how to use Microsoft Cognitive Services to make an IoT LED.
FSCognitive allows you to control a LED in real time using voice and secure with face recognition.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

1. A Raspberry Pi with Internet connection
2. Raspbian and python preinstalled on your Pi
3. Python 2.7 and OpenCV 2 pre-installed

### Getting started

First clone this project from github

```
git clone https://github.com/anhhoangiot/people_recognition_pi.git
```
Then run this command
```
pip install -U cognitive-face
```
Finally, create a new file named secret.json in core/cognitive. Content of newly created file looks like this:
```json
{
    "secret": "YOUR_API_TOKEN"
}
```

## Running the this project

On terminal / cmd type following command to create a group and train:
``` 
python app.py -d PATH_TO_TRAIN_FOLDER
```
On terminal / cmd type following command to start recognizing:
```
python app.py -i TIME_INTERVAL_BETWEEN_EACH_SESSION
```

## Authors

* **Anh Hoang** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
