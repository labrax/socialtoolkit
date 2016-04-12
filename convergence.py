#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

class Convergence:
    def __init__(self, max_number_iterations=0, steps_without_update=0):
        self._max_number_iterations = max_number_iterations
        self._steps_without_update = steps_without_update
        self._last_activity = 0
        self._is_done = False
    def update(self, step, activity):
        if activity is True:
            self._last_activity = step
        if self._max_number_iterations is not 0 and step >= self._max_number_iterations:
            self._is_done = True
        if self._steps_without_update is not 0 and self._last_activity + self._steps_without_update <= step:
            self._is_done = True
    def is_done(self):
        return self._is_done
