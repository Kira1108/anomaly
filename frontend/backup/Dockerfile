FROM node:14

# Set the working directory in the container to /app
WORKDIR /app
#
# # Copy only package.json and package-lock.json first
COPY package*.json /app
#
# # Install any needed packages specified in package.json
RUN npm cache clean -f 
RUN npm install
#
# # Copy the rest of your application code
COPY . /app 
#
# # Make port 8080 available to the world outside this container
EXPOSE 8080
#
# # Specify a non-root user
#
# # Run the application when the container launches
CMD ["npm", "run", "serve"]
