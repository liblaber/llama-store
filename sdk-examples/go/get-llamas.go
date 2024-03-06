package main

import (
	"fmt"
	"strings"

	"github.com/liblaber/llama-store-sdk-go/pkg/llamastore"
	"github.com/liblaber/llama-store-sdk-go/pkg/llamastoreconfig"
	"github.com/liblaber/llama-store-sdk-go/pkg/token"
	"github.com/liblaber/llama-store-sdk-go/pkg/user"
)

func main() {
	config := llamastoreconfig.NewConfig()
	config.SetBaseUrl("http://localhost:8080")

	llamaStore := llamastore.NewLlamaStore(config)

	// Create a new user
	userRegistration := user.UserRegistration{}
	userRegistration.SetEmail("noone@example.com")
	userRegistration.SetPassword("Password123!")

	// Register the user
	_, err := llamaStore.User.RegisterUser(userRegistration)

	// Check if the user was created - a 400 status code means the user already exists, so do nothing
	if err != nil {
		// check for 400 in the error message
		if strings.Contains(err.Error(), "400") {
			fmt.Println("User already exists")
		} else {
			panic(err)
		}
	}

	// Create an access token request
	tokenRequest := token.ApiTokenRequest{}
	tokenRequest.SetEmail(*userRegistration.Email)
	tokenRequest.SetPassword(*userRegistration.Password)

	// // Get the access token
	tokenResponse, err := llamaStore.Token.CreateApiToken(tokenRequest)

	// Check if the access token was created
	if err != nil {
		fmt.Println("Failed to get access token")
		panic(err)
	}

	// Set the access token on the llama store
	llamaStore.SetAccessToken(*tokenResponse.Data.AccessToken)

	// Get the llamas
	llamas, err := llamaStore.Llama.GetLlamas()

	// Check if the llamas were retrieved
	if err != nil {
		fmt.Println("Failed to get llamas")
		panic(err)
	}

	// Print the llama names
	fmt.Println("Llama names:")
	for _, llama := range llamas.Data {
		fmt.Println(*llama.Name)
	}
}
