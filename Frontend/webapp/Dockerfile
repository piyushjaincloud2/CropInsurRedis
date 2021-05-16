FROM node:latest
COPY app .
RUN cd app & npm install
RUN npm install -g next
EXPOSE 3000
ENTRYPOINT ["npm", "run", "dev"]