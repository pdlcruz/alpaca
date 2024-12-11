# Alpaca

Welcome to the Alpaca project! This README provides an overview and setup instructions to get you started with our application.

## Overview

Our application is currently designed to run locally, with future plans to host it as a service. It integrates text extraction from images and interfaces with various Large Language Models (LLMs), including custom models hosted on Hugging Face.

## Prerequisites

Before running the application, ensure the following:
- You are connected to the same WiFi network for proper communication between services.
- You have a Hugging Face account with a Pro subscription to access custom models.

## Installation

1. **Node.js Setup:**
   - Start by running the backend servers:
     ```bash
     node server_huggingface.js
     node server_textapi.js
     ```
   - These servers handle image text extraction and LLM interactions.
   - Ensure you have all the necessary Node.js packages installed. Commonly required packages include `cors` and `express`, which can be installed via npm:
     ```bash
     npm install cors express
     ```

2. **Expo App Setup:**
   - Initialize the Expo application:
     ```bash
     npx expo start
     ```
   - Install all required npm packages if you haven't already:
     ```bash
     npm install
     ```
   - Make sure Expo is installed on your system:
     ```bash
     npm install -g expo-cli
     ```

3. **Configuration:**
   - Determine your computer's IP address within your WiFi settings to ensure the Expo app can communicate with your local servers.
   - Update the `sendImageUrlToServer` and `query` configurations in the Expo app to reflect your local network settings.

## Running the Application

Once all setups are complete, your app should be ready to run. Enjoy using Alpaca and exploring its capabilities!

Thank you for trying out our project!
