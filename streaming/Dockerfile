FROM node:14
WORKDIR /usr/app/streaming

COPY ./package.json ./
COPY ./package-lock.json ./

RUN npm install --quiet

COPY . .

# ENV TZ=Asia/Ho_Chi_Minh
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone