#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/12/15 11:24
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : https://github.com/lobehub/lobe-chat?tab=readme-ov-file
#
#docker rm -f Lobe-Chat
#docker pull lobehub/lobe-chat
#docker run -d --network=host -e OPENAI_API_KEY=sk-XXXX -e ACCESS_CODE="" --name=Lobe-Chat --restart=always lobehub/lobe-chat
#docker images | grep 'lobehub/lobe-chat' | grep -v 'latest' | awk '{print $3}' | xargs docker rmi

docker run -d -p 39777:3210 \
  -e OPENAI_API_KEY=sk-xxxx \
  -e OPENAI_PROXY_URL=https://api.chatllm.vip/v1 \
  -e ACCESS_CODE=chatllm \
  lobehub/lobe-chat

# https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web
docker run --name chatgpt-next-web \
  --restart=always \
  -d -p 39771:3000 \
  -e BASE_URL=http://api.chatllm.vip \
  -e CUSTOM_MODELS=+gemini-pro,+kimi,+kimi-32k,+kimi-128k,+kimi-256k,+deepseek,-gpt-3.5-turbo-0301,-gpt-3.5-turbo-0613,-gpt-3.5-turbo-16k-0613,-gpt-4-0314,-gpt-4-0613,-gpt-4-32k-0314,-gpt-4-32k-0613 \
  yidadaa/chatgpt-next-web

# https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web
docker run --name chatgpt-next-web \
  --restart=always \
  -d -p 39771:3000 \
  -e BASE_URL=http://api.chatllm.vip \
  -e OPENAI_API_KEY=sk-xxxx \
  -e CODE=chatfire,chatllm \
  -e CUSTOM_MODELS=+gpt-4-all,+gemini-pro,+qwen,+glm,+baichuan,+kimi,+ERNIE-Bot-turbo,+deepseek,-gpt-3.5-turbo-0301,-gpt-3.5-turbo-0613,-gpt-3.5-turbo-16k-0613,-gpt-4-0314,-gpt-4-0613,-gpt-4-32k-0314,-gpt-4-32k-0613 \
  yidadaa/chatgpt-next-web

# https://github.com/Yanyutin753/ChatGPT-Next-Web-LangChain-Gpt-4-All?tab=readme-ov-file
# https://github.com/Hk-Gosuto/ChatGPT-Next-Web-LangChain
docker run --name nextchat \
  --restart=always \
  -d -p 39771:3000 \
  -e BASE_URL=http://api.chatllm.vip \
  -e R2_ACCOUNT_ID=d6746affe0c6f033dc6e8aa472d22d87 \
  -e R2_ACCESS_KEY_ID=9b87ee7be319fc4d1a8fe07881dccdbb \
  -e R2_SECRET_ACCESS_KEY=49b86992d3ab45a6eb538fc316fffee964c551f95c1a0a88576ef80b10e93863 \
  -e R2_BUCKET=chatfire \
  -e CUSTOM_MODELS=-all,+gpt-4-all,+dall-e-3,+gpt-4-vision-preview,+gpt-3.5-turbo,+gpt-4-turbo-preview,+deepseek-chat,+deepseek-coder,+kimi \
  gosuto/chatgpt-next-web-langchain


