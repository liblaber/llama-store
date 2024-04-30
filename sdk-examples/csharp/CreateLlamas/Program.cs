// This script creates a new llama in the llama store.

// It starts by creating a user and then creating an access token for that user. It then uses the access token to
// create the llama.

using System.Net;
using LlamaStore;
using LlamaStore.Models;

// Create an instance of the llama store SDK
var client = new LlamaStoreClient();

// Create a user

// Create the registration object
var userRegistration = new UserRegistration("noone@example.com", "Password123!");

// Try to register the user. If the user already exists, a 400 will be thrown
try
{
    var user = await client.User.RegisterUserAsync(userRegistration);
    Console.WriteLine("User created");
}
catch (HttpRequestException e)
{
    if (e.StatusCode == HttpStatusCode.BadRequest)
    {
        Console.WriteLine("User already exists - user won't be created");
    }
    else
    {
        throw e;
    }
}

// Create an access token

// Create the token request using the same credentials as the user registration
var tokenRequest = new ApiTokenRequest(userRegistration.Email, userRegistration.Password);

// Create the token
var token = await client.Token.CreateApiTokenAsync(tokenRequest);
Console.WriteLine("Token created");

// Now we have the token we can set it at the SDK level so we never have to worry about it again
client.SetAccessToken(token.AccessToken);

// Create a new llama

// Define the create llama request
var newLlamaRequest = new LlamaCreate("Llamapoleon Bonaparte", 5, LlamaColor.White, 4);

// Create the llama
var newLlama = await client.Llama.CreateLlamaAsync(newLlamaRequest);
Console.WriteLine($"Created llama {newLlama.Name} with ID {newLlama.LlamaId}");
