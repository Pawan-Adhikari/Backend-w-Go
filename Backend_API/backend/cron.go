package main
import (
	"github.com/robfig/cron"
	"fmt"
	"os/exec"
	"path/filepath"
)

func runScript() {
	scriptPath := filepath.Join("scripts" , "tshoRolpa.py")
	cmd := exec.Command("python3", scriptPath)
	fmt.Println("Running the script at:",scriptPath, "now!")
	output, err := cmd.CombinedOutput()

	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			switch exitErr.ExitCode() {
			case 2:
				fmt.Println("Scanned just today!")
			case 3:
				fmt.Println("No new data yet!")
			default:
				fmt.Println("Unknown error occured in script!")
			}
		} else {
			fmt.Println("Unkown error occured in script!")
		}
	} else {
		fmt.Println("Script ran without any error!")
	}
	//_ = output
	fmt.Println("Output:", string(output))
	
}

func main(){
	c := cron.New()
	c.AddFunc("@every 30s", runScript)
	c.Start()
	fmt.Println("Cronjob initialised, will start job periodically!")
	select {} //Block the program forever
}
