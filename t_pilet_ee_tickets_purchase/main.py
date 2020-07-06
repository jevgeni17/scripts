#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'jevgeni17'


from selenium import webdriver
import time
from recursive_json import extract_values
import requests
import re
from termcolor import colored
import colorama
colorama.init()


class Journey: 

    def __init__(self):
        self.__browser = webdriver.Chrome()
        self.__departure = 'tallinn'
        self.__destination = 'parnu'
        self.date = input('Type date'+ '\n') # format example '2020-03-02' year/month/day
        self.__returningTrip = '0' 
        self.__route = None
        self.__ticket = None
        self.__seat = None
        self.__TALLINN_ID = '17028'
        self.__PARNU_ID = '8723'

    def link(self):
        link = ('https://www.tpilet.ee/travel?departureStop=' + self.__departure + '&destinationStop=' + self.__destination + '&departureDate=' + self.date + '&returnDate=' + self.date + '&returningTrip=' + self.__returningTrip + '&price=-1&duration=-1')
        self.__browser.get(link)
        time.sleep(3)
    
    def getRoutes(self):
        js_times="""
            var times = document.getElementsByClassName('vqA6QljR2KNt8yw9PHk9C');
            let time = [];
            for (var i = 0; i < times.length; i++){
                time.push(times[i].innerText);
                console.log(time);
            } return time;
        """

        js_company="""
            var company = document.getElementsByClassName('lvCBxuihqm3iUoMcebtd4');
            let companys = [];
            for (var i = 0; i < company.length; i++){
                companys.push(company[i].innerText);
                console.log(companys);
            } return companys;
        """
        
        self.__js_tickets="""
            var ticket = document.getElementsByClassName('_3TJaMCIiSE5gyvUGhXPJ_f');
            let tickets = [];
            for (var i = 0; i < ticket.length; i++){
                tickets.push(ticket[i].innerText);
                console.log(tickets);
            } return tickets;
        """

        self.__js_seats="""
            var seat = document.getElementsByClassName('_1bELoiN2P2KjAtnIfRarX-');
            let seats = [];
            for (var i = 0; i < seat.length; i++){
                seats.push(seat[i].innerText);
                console.log(seats);
            } return seats;
        """

        """Scrap some data from tpilet """

        times = self.__browser.execute_script(js_times)
        company = self.__browser.execute_script(js_company)
        
        """link to get json web-api"""

        link = ('https://www.tpilet.ee/webapi/et/journeys/search?departureStop=tallinn&destinationStop=parnu&departureDate=' + self.date + '&returnDate=&price=-1&duration=-1&includeConnections=false&departureBusStopId=' + self.__TALLINN_ID +'&destinationBusStopId=' + self.__PARNU_ID)
        r = requests.get(link)

        """Scrap some data from json web-api"""

        fullPrice = extract_values(r.json(), 'FullPrice') # from recursive_json import extract_values
        salePrice = extract_values(r.json(), 'CampaignPrice')
        self.__tripId = extract_values(r.json(), 'TripId')
        self.__DEP_ID = extract_values(r.json(), 'DepartureRouteStopId')
        self.__DEST_ID = extract_values(r.json(), 'DestinationRouteStopId')

        """Convert lists to dictionaries"""

        times_dict = { i : times[i] for i in range(0, len(times) ) }
        company_dict = { i : company[i] for i in range(0, len(company) ) }
        full_dict = { i : fullPrice[i] for i in range(0, len(fullPrice) ) }
        sale_dict = { i : salePrice[i] for i in range(0, len(salePrice) ) }
        

        for key in times_dict and company_dict and full_dict and sale_dict:
            print(key, '--->>>', times_dict[key], '   ', company[key], '    FULL PRICE',fullPrice[key],'    WITH DISCOUNT',salePrice[key],)
        

    def getTickets(self):

        num = int(input('Type route' + '\n'))
    
        """link to get json web-api"""

        linkk = ('https://www.tpilet.ee/webapi/et/trips/prices?tripId='+ str(self.__tripId[num])+ '&departureRouteStopId='+str(self.__DEP_ID[num])+'&destinationRouteStopId='+str(self.__DEST_ID[num]))
        rr = requests.get(linkk)

        num+-1
        time.sleep(3)
        q = self.__browser.execute_script("document.getElementsByClassName('OxitbZN0S38kKLBZlAssO')[" + str(num) +"].click()")
        time.sleep(3)
        ticket = self.__browser.execute_script(self.__js_tickets)
        q = [re.sub(r'\n', ' ', i) for i in ticket]
        newtest = [x[:-1] for x in q] 
        #print(newtest)
        tickets_dict = { i : newtest[i] for i in range(0, len(newtest) ) }

        for key in tickets_dict:
            print(key, '--->>>', tickets_dict[key])
    
    def getSeats(self):
        inp = str(input())

        q = self.__browser.execute_script("document.getElementsByClassName('_3mbZTemfn3cnxwKkLHZs-m')[" + str(inp) +"].click()")
        time.sleep(3)
        seat = self.__browser.execute_script(self.__js_seats)
        w = [re.sub(r'\n', ' ', i) for i in seat]
        #print(w)

        a = [['1', '2', '3', '4'], ['5', '6', '7', '8'], # list of all seats
            ['9', '10','11', '12'], ['13', '14', '15', '16'],
            ['17', '18', '19', '20'], ['21', '22', '23', '24'],
            ['25', '26', '27', '28'], ['29', '30','31','32'],
                                        ['33','34','35','36']]
        a = sum(a, [])
        result = []
        for elem in a:
            if not str(elem).isdigit():
                continue
            if elem in w:
                result.append((colored(elem, 'green'))) # available seats
            else:
                result.append((colored(elem, 'red'))) # occupied seats

            if len(result) % 4 == 0:
                print('  '.join(result))
                result = []

        inpp = input()
        q = self.__browser.execute_script("document.getElementById('web-tickets-busseat-" + inpp +"').click()")
        time.sleep(100)

if __name__ == "__main__":
    x = Journey()
    x.link()
    x.getRoutes()
    x.getTickets()
    x.getSeats()


    

