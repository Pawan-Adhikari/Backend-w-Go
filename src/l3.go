package main

import (
	"encoding/json" // Correct path for json package
	"fmt"
)

func main() {

	db_map := map[string]string{"name": "", "address": ""}

	var temp_name string
	var temp_address string

	fmt.Println("Enter your name: ")
	fmt.Scan(&temp_name)
	fmt.Println("Enter your address: ")
	fmt.Scan(&temp_address)

	db_map["name"] = temp_name
	db_map["address"] = temp_address

	fmt.Println("Your name is:", db_map["name"])	
	fmt.Println("Your address is:", db_map["address"])

	var json_data []byte
	json_data, err := json.Marshal(db_map)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	fmt.Println("JSON data:", string(json_data))
}