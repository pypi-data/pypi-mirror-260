# Timer Score

Timer Score is a timer library that provides a score from 0 to 1 for how well the timed code meets the expected target duration. The main driver for this library is the fact that most measurements of LLMs return a score from 0 to 1 (i.e. BLEU, ROUGE, etc). The Timer Score library enables you to similarly produce a score from 0 to 1 for performance.

## Features

__timer__ - Track time in milliseconds for any code or function  
__scoring__ - Calculate a score from 0 to 1 based on performance against a target duration  
__checkpoints__ - Capture multiple checkpoints during timing including individual targets for each checkpoint  
__timed functions__ - Time an entire function or method with a single call  
__reset__ - Reset the timer for multiple tests of the same code  
__sleep__ - Sleep the timer to allow for parallel code execution  

## Documentation

[Documentation on github](https://github.com/bbenedict/timer_score/tree/main/docs)

## Installation

First install the timer_score library.

```
pip install timer_score
```

Instantiate the timer with your target duration.  Use timer.stop() when the task is complete and timer.score() to get the final score.  

```
from timer_score import TSTimer

timer = TSTimer(2)
# The code you are timing goes here
timer.stop()

score, duration, target = timer.score()
# 0.53... 1.85... 2
```
