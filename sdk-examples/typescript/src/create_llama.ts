// This script creates a new llama in the llama store, then sets its picture.

// It starts by creating a user and then creating an access token for that user. It then uses the access token to
// create the llama and upload the picture.

// You will need to install the built llama store SDK to run this script.

// - Generate the SDK by running liblab build. If you don't have liblab installed, you can install by following
//   the instructions in the docs at https://developers.liblab.com
// - Ensure the llama store is running
// - Run this script using npm run create-llama

// This script will upload a llama picture called llamapoleon-bonaparte.png. This file needs to
// be in the same directory as this script.

import { Llamastore, CreateLlamaRequest, RegisterUserRequest, CreateApiTokenRequest } from 'llamastore';
var fs = require('fs/promises');

(async () => {

    // Create an instance of the llama store SDK
    const llamaStore = new Llamastore({});

    // Create a user
    // For this we can use the user service
    const userService = llamaStore.user;

    // Create the registration object
    const userRegistration: RegisterUserRequest = { email: 'noone@example.com', password: 'Password123!' };
    let user: any = null;

    // Try to register the user. If the user already exists, a 400 will be thrown
    try {
        user = await userService.registerUser(userRegistration);
        console.log('User created');
    } catch (e) {
        console.log('User already exists - user won\'t be created');
    }

    // Create an access token
    // For this we can use the token service
    const tokenService = llamaStore.token;

    // Create the token request using the same credentials as the user registration
    const tokenRequest: CreateApiTokenRequest = { email: userRegistration.email, password: userRegistration.password };

    // Create the token
    const token = await tokenService.createApiToken(tokenRequest);
    console.log('Token created');

    llamaStore.setAccessToken(token.access_token);

    // Define the create llama request
    const newLlamaRequest: CreateLlamaRequest = {
        "name": "Llamapoleon Bonaparte",
        "age": 5,
        "color": "white",
        "rating": 4
    }

    // Create the llama
    const newLlama = await llamaStore.llama.createLlama(newLlamaRequest);
    console.log(`Created llama ${newLlama.name} with ID ${newLlama.id}`);
})();
