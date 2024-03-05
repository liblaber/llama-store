package main

import (
	"fmt"
	"strings"

	"github.com/liblaber/llama-store-sdk-go/pkg/llama"
	"github.com/liblaber/llama-store-sdk-go/pkg/llamastore"
	"github.com/liblaber/llama-store-sdk-go/pkg/llamastoreconfig"
	"github.com/liblaber/llama-store-sdk-go/pkg/token"
	"github.com/liblaber/llama-store-sdk-go/pkg/user"
)

func main() {
	config := llamastoreconfig.NewConfig()
	config.SetBaseUrl("http://localhost:8000")

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

	// Create a new llama
	LlamaCreate := llama.LlamaCreate{}
	LlamaCreate.SetName("Llamapoleon Bonaparte")
	LlamaCreate.SetAge(5)
	LlamaCreate.SetColor(llama.LLAMA_COLOR_WHITE)
	LlamaCreate.SetRating(4)

	// Create the llama
	newLlama, err := llamaStore.Llama.CreateLlama(LlamaCreate)

	// Check if the llama was created
	if err != nil {
		fmt.Println("Failed to create llama")
		panic(err)
	}

	fmt.Println("Llama created: ", *newLlama.Data.Name, " with ID: ", *newLlama.Data.Id)
}
