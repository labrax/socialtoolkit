#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source file contains the convergence data for an execution.
"""

from .algorithm import Algorithm


class Convergence(Algorithm):
    """Class for checking for convergence conditions."""
    def __init__(self, max_number_iterations=0, steps_without_update=0):
        """Args:
            max_number_iterations (Optional[int]): the maximum number of iterations.
            steps_without_update (Optional[int]): the numbers of steps without updates to end the execution."""
        self._max_number_iterations = max_number_iterations
        self._steps_without_update = steps_without_update
        self._last_activity = 0
        self._is_done = False

    def update(self, step, activity):
        """Args:
            step (int): the current step on the execution.
            activity (bool): True if there has been a change on the graph or population information."""
        if activity is True:
            self._last_activity = step
        if self._max_number_iterations is not 0 and step >= self._max_number_iterations:
            self._is_done = True
        if self._steps_without_update is not 0 and self._last_activity + self._steps_without_update <= step:
            self._is_done = True

    def is_done(self):
        """Returns wheter the convergence conditions have been achieved."""
        return self._is_done
