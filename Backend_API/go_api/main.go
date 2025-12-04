package main

import (
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"log"
)

const Port = "8080" 
const ImageDirectory = "public/data/TshoRolpa/"
const APIPath = "/image/latest"

func latestPNGHandler(w http.ResponseWriter, r *http.Request){
	//Check if the request is of valid method.
	//Write error with an error code and status code to responsewriter.
	//Then return NIL to terminate the function body
	if r.Method != http.MethodGet{
		log.Printf("Received %s request on %s. Only GET is allowed.", r.Method, r.URL.Path)
		http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
		return
	}

	bytes, err := os.ReadFile(filepath.Join(ImageDirectory , "date.txt"))
	if err != nil {
		log.Println("Error: date.txt missing or content is empty.")
		http.Error(w, "Internal Server Error : (Config not found or empty)", http.StatusInternalServerError)
		return
	}

	date := strings.TrimSpace(string(bytes))
	latestFilePNG := filepath.Join(ImageDirectory, fmt.Sprintf("%s.png", date))
	_,err = os.Stat(latestFilePNG)
	if os.IsNotExist(err){
		log.Printf("Error: Latest file (%s) referenced in config not found on disk.", latestFilePNG)
		http.Error(w, "Internal Server Error: (Latest file as per config not found)", http.StatusInternalServerError)
		return
	}

	log.Printf("Serving image: %s based on date: %s", latestFilePNG, date)
	w.Header().Set("Content-Type", "image/png")
	w.Header().Set("Cache-Control", "no-cache, no-store, must-revalidate")

	http.ServeFile(w, r, latestFilePNG)
}

func main(){
	if _, err := os.Stat(ImageDirectory); os.IsNotExist(err) {
		log.Printf("WARNING: The directory %s does not exist. Ensure it is mounted as a volume when running via Docker.", ImageDirectory)
	}

	http.HandleFunc(APIPath, latestPNGHandler)
	fmt.Printf("Sever starting on http://localhost:%s%s\n ", Port, APIPath)
	err := http.ListenAndServe(":"+Port, nil)
	if err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}

}