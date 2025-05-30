package main
import "fmt"

func truncate() {
	var x float32
	var y int
	fmt.Println("Enter a float number:")
	fmt.Scanf("%f", &x)
	fmt.Printf("You entered: %f\n", x)
	fmt.Println("Enter an integer:")
	y = int(x)
	fmt.Printf("Converted to integer: %d\n", y)

}