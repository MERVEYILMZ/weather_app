# InfoTech Weather Application

## Project Overview
This project is a Weather Application with a graphical user interface designed to provide real-time weather information. The application covers weather details for at least three countries: the Netherlands, Germany, and the USA.

### Features
- **Country Selection:** Upon starting the application, users are prompted to select a country.
- **Province/Region Listing:** Post country selection, provinces or regions within the selected country are listed, sorted based on population.
- **Detailed Weather Information:** For the chosen province or region, the application displays:
  - The name of the province/region
  - The state it belongs to
  - The population
  - Current weather (represented as an icon)
  - Temperature
- **City Search Functionality:** Users can search for a city to view its detailed information and current weather conditions.

## Tools and Technologies
- **Graphical User Interface (GUI):** PyQT5
- **Web Scraping:** Scrapy
- **Networking:** HTTP-Request and APIs for fetching real-time weather data
- **Database Management System (DBMS):** MongoDB

## Meeting Schedule
- **Project Kick-off / Sprint Planning Meeting:** 27-01-2024
- **Daily Scrum Meeting:** Every day
- **Retrospective Meeting / Sprint Planning Meeting:** 01-02-2024
- **Sprint Review:** 08-01-2024

## SPRINT-1
1. **Design GUI for App**
   - Consider Web Scraping Data Visualization
   - Consider Web API Data Visualization
2. **UML Diagrams and Database Structure**
   - Use Case Diagram
   - Class Diagram
   - MongoDB
3. **Scrapy**
   - Extract city, state, and population information from websites with Scrapy.
   - Display the name, region/state, and population of the selected city in the program.
   - Organize and store all information in the database.
   - Relevant URLs:
     - [US Cities by Population](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population)
     - [Municipalities of the Netherlands](https://en.wikipedia.org/wiki/Municipalities_of_the_Netherlands)
     - [Most Populous Municipalities in Belgium](https://en.wikipedia.org/wiki/List_of_most_populous_municipalities_in_Belgium)

## SPRINT-2
4. **HTTP Requests and API**
   - Use HTTP-Request and API to fetch real-time weather information.
   - Display temperature and weather icons for the selected cities, pulling data from [OpenWeatherMap API](https://openweathermap.org/api).
   - Store all information in the database.
   - [Weather Conditions and Icons](https://openweathermap.org/weather-conditions)
5. **Main Page Components**
   - Countries
   - Selected Country, Cities, Regions, Populations ordered by Population
   - City Search Bar
   - Selected City Name, Region, Population
   - Selected City Temperature (Celsius)
   - Selected City Weather Condition Icon (online from the given API) and icon Description
   - Selected City Humidity
   - Selected City Wind
   - Selected City 12-hour forecast every 3 hours
   - Selected City Next 3 days forecast

## Program/Output
- Finalize the application to run on Windows.
- Generate a “.EXE” file and share it.
- Follow the instructions in the provided video to make the application work like a normal program without Python.

## Installation
(Provide detailed step-by-step installation instructions here. Include how to set up PyQT5, Scrapy, MongoDB, and any other necessary tools or dependencies.)
