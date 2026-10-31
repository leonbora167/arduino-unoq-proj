# arduino-unoq-proj
Projects on the arudino Uno - Q 

[![wakatime](https://wakatime.com/badge/user/23cfbce7-d612-40f6-82c3-807d45099810/project/606af97f-f978-407a-bfc3-9077c29b80b2.svg)](https://wakatime.com/badge/user/23cfbce7-d612-40f6-82c3-807d45099810/project/606af97f-f978-407a-bfc3-9077c29b80b2)

## Headless
```bash
ssh ssh arduino@<your device name>.local
```

## General commands to run the Arduino App Lab

* List custom apps 
```bash
arduino-app-cli app list
```

* Check which apps are running currently
```bash
arduino-app-cli app ps
```

* Launch an app
```bash
arduino-app-cli app start <app id>
```

* Stop an app
```bash
arduino-app-cli app stop <app id>
```

* Monitor an app through ssh
```bash
arduino-app-cli app logs <app id> --follow
```

* Create a new app through terminal only
```bash
arduino-app-cli app new "my-app"
```