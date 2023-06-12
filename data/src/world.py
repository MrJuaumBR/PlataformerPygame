import pygame as pyg
from pygame.locals import *
from .config import *

class World():
    def __init__(self):
        # General Time control
        self.Time = 0
        self.MaxTime = 24
        self.MinTime = 0
        self.TimeStyle = "HH:MM"
        self.currentTime = ""

        # Day Control
        self.maxDays = 30
        self.minDays = 1
        self.Day = 1

        # Month Control
        self.maxMonth = 12
        self.minMonth = 1
        self.Month = 1

        # Year Control
        self.minYear = 3073
        self.Year = self.minYear

        # Frames Control
        self.Frames = 0
        self.TickFrame = 290 # Time to walk 1 hour

    def CTL_Frames(self):
        """Frames Logic"""
        self.Frames += 1
        if self.Frames>= self.TickFrame:
            self.Frames = 0
            self.Time += 1

    def CTL_Time(self):
        """Time Control Logic"""
        # Time Limiters
        if self.Time > self.MaxTime:
            self.Time = self.MinTime
            self.Day += 1
        if self.Time < self.MinTime:
            self.Time = self.MaxTime

        # Time Detector
        if self.Time >= 18:
            self.currentTime = "evening"
        elif self.Time == 12:
            self.currentTime = "midday"
        elif self.Time == 24:
            self.currentTime = "midnight"
        elif self.Time < 12:
            self.currentTime = "morning"
        elif self.Time > 12:
            self.currentTime = "afternoon"

    def CTL_Day(self):
        """Day Control Logic"""
        # Day Limiters
        if self.Day > self.maxDays:
            self.Day = self.minDays
            self.Month += 1
        if self.Day < self.minDays:
            self.Day = self.maxDays
        
    def CTL_Month(self):
        """Month Control Logic"""
        if self.Month > self.maxMonth:
            self.Month = self.minMonth
            self.Year += 1
        if self.Month < self.minMonth:
            self.Month = self.maxMonth

    def CTL_Year(self):
        """Year Control Logic"""
        if self.Year < self.minYear:
            self.Year = 3073

    def update(self):
        # Time Update
        self.CTL_Frames()
        self.CTL_Time()
        self.CTL_Day()
        self.CTL_Month()
        self.CTL_Year()