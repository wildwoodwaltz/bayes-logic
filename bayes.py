import sys
import random
import itertools
import numpy as np
import cv2 as cv


MAP_FILE = 'cape_python.png'

SA1_CORNERS = (130, 265, 180, 315) # (UL-X, UL-Y, LR-X, LR-Y)
SA2_CORNERS = (80, 255, 130, 305) # (UL-X, UL-Y, LR-X, LR-Y)
SA3_CORNERS = (105, 205, 155, 255) # (UL-X, UL-Y, LR-X, LR-Y)

class Search():
    """Simple Bayesian Search and Rescue Game with 3 search areas."""

    def __init__(self,name):
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print("Map file not found or could not be loaded {}".format(MAP_FILE, file=sys.stderr))
            sys.exit(1)
        
        self.area_actual = 0
        self.sailor_actual = [0,0] 

        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3], SA1_CORNERS[0] : SA1_CORNERS[2]]
        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3], SA2_CORNERS[0] : SA2_CORNERS[2]]
        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3], SA3_CORNERS[0] : SA3_CORNERS[2]]

        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0
        
    def draw_map(self, last_pos):
        """Displays Map with Legend, last known pos, and search areas"""
        cv.line(self.img, (20,370),(70,370), (0,0,0), 2)
        cv.putText(self.img, '0', (8,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.putText(self.img, '50 Nautical Miles', (71,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))

        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]),(SA1_CORNERS[2], SA1_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '1',(SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15),cv.FONT_HERSHEY_PLAIN, 1, 0)
        
        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]),(SA2_CORNERS[2], SA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '2',(SA2_CORNERS[0] + 3, SA2_CORNERS[1] + 15),cv.FONT_HERSHEY_PLAIN, 1, 0)
        
        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]),(SA3_CORNERS[2], SA3_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '3',(SA3_CORNERS[0] + 3, SA3_CORNERS[1] + 15),cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.putText(self.img, '+' (last_pos), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))
        cv.putText(self.img, '+ = Last Known Position')

        cv.putText(self.img, '* = Actual Position', (275,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))

        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area', 750,10)
        cv.waitKey(500)

    def sailor_final_location(self, num_search_areas):
        """Return the actual x,y co-ords of the missing sailor"""
        # Find sailor coordinates with respect to any Search Array subarray
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1],1)
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0],1)

        area = int(random.triangular(1, num_search_areas + 1))

        if area == 1:
            x = self.sailor_actual[0] + SA1_CORNERS[0]
            y = self.sailor_actual[1] + SA1_CORNERS[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SA2_CORNERS[0]
            y = self.sailor_actual[1] + SA2_CORNERS[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SA3_CORNERS[0]
            y = self.sailor_actual[1] + SA3_CORNERS[1]
            self.area_actual = 3
        return x,y

    def calc_search_effectiveness(self):
        """Setting decimal search effectiveness value per search area."""
        self.sep1 = random.uniform(0.2, 0.9)
        self.sep2 = random.uniform(0.2, 0.9)
        self.sep3 = random.uniform(0.2, 0.9)

    def conduct_search(sef, area_num, area_array, effectiveness_prob):
        """Return search results and list searched coordinates"""

        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])

        coords = list(itertools.product(local_x_range,local_y_range))
        
        random.shuffle(coords)
        
        coords = coords[:int((len(coords) * effectiveness_prob))]

        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])

        if area_num == self.area_actual and loc_actual in coords:
            return "Found Sailor in Area {}.".format(area_num), coords
        else:
            return "Not found", coords
    
    def revise_target_probs(self):
        """Update area target probablilities based on search effectiveness"""
        denom = self.p1 * (1 - self.sep1) + self.p2 * (1 - self.sep2) + self.p3 * (1 - self.sep3)

        self.p1 = self.p1 * (1 - self.sep1) / denom
        self.p2 = self.p2 * (1 - self.sep2) / denom
        self.p3 = self.p3 * (1 - self.sep3) / denom


def draw_menu(search_num):
    """Print Menu of Choices for Conducting Search"""
    print("\nSearch {}".format(search_num))
    print(
        """
        Choose next areas to search:

        0 - Quit
        1 - Search Area 1 twice
        2 - Search Area 2 twice
        3 - Search Area 3 twice
        4 - Search Areas 1 & 2
        5 - Search Areas 1 & 3
        6 - Search Areas 2 & 3
        7 - Start Over
        """
    )

def main():
    app.Search('Cape_Python')
    app.draw_map(last_known(160,290))
    sailor_x, sailor_y = app.sailor_final_location(num_search_areas = 3)
    print ("-" * 65)
    print("\nInitial Target (P) Probabilities:")
    print("P1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}".format(app.p1, app.p2, app.p3))
    search_num = 1

    while True:
        app.calc_search_effectiveness()
        draw_menu(search_num)
        choice = input("Choice: ")

        if choice == "0"
            sys.exit