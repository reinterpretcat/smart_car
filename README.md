# Description

This repo contains refined code for server to control [Freenove 4WD Smart Car Kit for Raspberry Pi](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi).

![Freenove 4WD Smart Car](resources/icon.png "Freenove 4WD Smart Car")


## How to use

Install all dependencies according to original tutorial, then connect to your Raspberry Pi and run in terminal:

```shell
cd server
sudo python main.py
```

To exit, press `Ctrl+C`.

## Additional scripts

There are some additional scripts which can be used for experimentation:

- __pan_tilt_camera__: play with a better camera and Pan Tilt HAT (see dedicated README.md)

- __playground__: a jupyter notebook to experiment with hardware controlling scripts in isolation


## Motivation

I'm planning to play a bit with extra capabilities just for fun, so would need to adjust server/client code a bit, but found original quite difficult to extend. Also refactoring helps to understand code and logic a bit more.

The code in the repo is not very idiomatic too, I'm planning to address this later (maybe).


# Status

Experimental. No warranty.