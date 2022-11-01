#!/usr/bin/python
# -*- coding: utf-8 -*-s

class UserScore:
    def __init__(self, name: str, score: int, time: float):
        self.name = name
        self.score = score
        self.time = time

    def __str__(self):
        return f"{self.name},{self.score},{self.time}\n"
