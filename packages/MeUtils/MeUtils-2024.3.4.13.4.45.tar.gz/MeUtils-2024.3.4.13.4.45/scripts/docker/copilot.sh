#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2024/2/27 15:56
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : https://github.com/Yanyutin753/gpt4-copilot-java/tree/main

docker run -d --name copilot1 \
  -v ./copilot_config1.json:/config.json \
  -p 8881:8080 \
  --restart always \
  yangclivia/gpt4-copilot-java:latest

docker run -d --name copilot2 \
  -v ./copilot_config2.json:/config.json \
  -p 8882:8080 \
  --restart always \
  yangclivia/gpt4-copilot-java:latest

docker run -d --name copilot3 \
  -v ./copilot_config3.json:/config.json \
  -p 8883:8080 \
  --restart always \
  yangclivia/gpt4-copilot-java:latest
