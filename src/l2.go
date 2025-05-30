package main
import "fmt"
import "sort"
import "strconv"

func main() {
	int_slice := make([]int, 3)
	var input_str string
	var input_int int
	for (input_str != "X") {
		fmt.Println("Enter an integer to append (or 'X' to exit): ")
		fmt.Scan(&input_str)
		input_int, _ = strconv.Atoi(input_str)
		int_slice = append(int_slice, input_int)
	}
	
	sort.Ints(int_slice)

    fmt.Printf("Sorted slice: %v\n", int_slice)
}
