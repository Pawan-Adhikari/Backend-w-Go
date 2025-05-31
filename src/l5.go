//lab5.go
//Bubble sort with functions

package main

import (
	"fmt"
)

func takeInput(input_slice []int){

	fmt.Printf("Enter 10 integers to sort: ")
	for i :=0 ; i<10; i++{
		fmt.Scan(&input_slice[i])
	}

}

func swap(x,y *int){
	var temp_int int
	temp_int = *y
	*y = *x
	*x = temp_int
}


func sortSlice(input_slice []int){
	for i := 0 ; i<10; i++{
		for j := i+1 ; j<10;j++{
			if (input_slice[j] < input_slice[i]){
				swap(&input_slice[j],&input_slice[i])
			}
		}
	}
}


func printSlice(sorted_slice []int){
	fmt.Printf("The sorted slice is: ")
	for i := 0 ; i<10; i++{
		fmt.Printf("%d",sorted_slice[i])
	}
}


func main (){

	input_slice := make([]int, 10) // Initialize with length 10

	takeInput(input_slice)

	sortSlice(input_slice)

	printSlice(input_slice)
	
}