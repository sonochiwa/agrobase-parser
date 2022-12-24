package main

import (
	"fmt"
	"github.com/gocolly/colly"
	"os"
	"time"
)

func getAllDistricts() []string {
	districts := []string{}
	c := colly.NewCollector()
	c.OnHTML("ul.sections > li > a", func(e *colly.HTMLElement) {
		districts = append(districts, "https://www.agrobase.ru"+e.Attr("href"))
	})
	c.Visit("https://www.agrobase.ru/selxozpredpriyatiya/rossiya")
	return districts
}

func getAllCities(districts []string) []string {
	cities := []string{}
	c := colly.NewCollector()
	for _, district := range districts {
		c.OnHTML("ul.sections > li > a", func(e *colly.HTMLElement) {
			cities = append(cities, "https://www.agrobase.ru"+e.Attr("href"))
		})
		c.Visit(district)
	}
	return cities
}

func getAllNumbers(cities []string) []string {
	numbers := []string{}
	c := colly.NewCollector()
	for _, city := range cities {
		c.OnHTML(".ac-company__details > dt", func(e *colly.HTMLElement) {
			if e.Text == "Телефон:" {
				numbers = append(numbers, e.DOM.Next().Text())
			}
		})
		c.Visit(city)
	}
	return numbers
}

func writeData(numbers []string) {
	file, _ := os.Create("agrobase.txt")
	for _, line := range numbers {
		file.WriteString(line + "\n")
	}
}

func main() {
	start := time.Now()
	districts := getAllDistricts()
	cities := getAllCities(districts)
	numbers := getAllNumbers(cities)
	writeData(numbers)
	fmt.Println(time.Since(start))
}
