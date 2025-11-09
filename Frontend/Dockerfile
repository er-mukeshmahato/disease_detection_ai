# Stage 1: Build the React app
FROM node:alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . ./

# Expose port 3000 for the development server
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
