# docker-rotating-proxy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/787e065d562a4c499eda6655812cab72)](https://www.codacy.com/app/whiteviel/docker-rotating-proxy)


Inspired by [https://github.com/mattes/rotating-proxy](https://github.com/mattes/rotating-proxy)


## Create the application
Start a proxy server using http proxy

### start the application
1. get the image

     ```bash
      docker pull brianstech/docker-rotating-proxy
     ```

1. run the proxy

     ```bash
        docker run -d -p 8080:8080 -p 4444:4444 brianstech/docker-rotating-proxy
     ```

1. access the proxy stats at

        [http://localhost:4444](http://localhost:4444)

1. set you client to use

        - http proxy: http://localhost:8080
        - https proxy: https://localhost:8080
