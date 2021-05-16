FROM node:14.15.0

COPY . .
COPY package.json .
COPY yarn.lock .

RUN npm install -g yarn --force
RUN yarn install --force


CMD [ "yarn", "start" ]

EXPOSE 3000

EXPOSE 3625
