package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Name struct {
	fname string
	lname string
}

func constructor_name(fname string, lname string) Name {
	return Name{fname: fname, lname: lname}
}

func main() {

	var file_name string
	var name_arr []Name

	fmt.Println("Enter file name: ")
	fmt.Scan(&file_name)

	file, err := os.Open(file_name)

	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.SplitN(line, " ", 2)

		name_arr = append(name_arr, constructor_name(parts[0], parts[1]))
	}

	for i, temp_name := range name_arr {
		fmt.Printf("Name %d: %s %s\n", i+1, temp_name.fname, temp_name.lname)
	}
}
