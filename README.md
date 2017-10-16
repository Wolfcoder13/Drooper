# Drooper

Drooper is going to be a device that has a drum machine and a looper, that you can make music with. We will use Raspberry pi as our microcontroller. It will take input from various sensors, such as knobs and force sensitive resistors. These sensors will control volume and pan, audio effects, control digital interface on DLC screen. It will be possible to record audio as well. The device will detect the BPM (beats per minute) of the first recorded clip so it can clip all audio clips with great detail. When it comes to music, precision is very important regarding timing.

## How the device will look

![Image of the interface](./Interface.png?raw=true "The Interface")

## The circuit diagram for our 4x4 drum machine. This is before anything else has been made so, the pins on the raspberry pi havent been expanded.

![Circuit schematic for 4x4 pads](./4x4Connection_schem.jpg?raw=true "The Interface")

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to install : https://github.com/adafruit/Adafruit_Python_MCP3008
libav-tools is neccesary to be able to use pydub on raspbian
It is neccesary to install pyaudio correctly.

```
sudo pip install adafruit-mcp3008
sudo pip install pydub
sudo pip install pyaudio
sudo apt-get install libav-tools
```

### Setup USB sound driver

type in ``sudo nano /usr/share/alsa/alsa.conf`` , scroll down and find these lines
```
defaults.ctl.card 0
defaults.pcm.card 0
```
and change them into 
```
defaults.ctl.card 1
defaults.pcm.card 1
```
Then type in ``sudo nano ~/.asoundrc`` and change it so it reads
```
pcm.!default {
    type hw
    card 1
}

ctl.!default {
    type hw
    card 1
}
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
