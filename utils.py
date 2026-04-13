import pygame

def sleep(seconds):
    end_time = pygame.time.get_ticks() + (seconds * 1000)
    while pygame.time.get_ticks() < end_time:
        pygame.event.pump()
        pygame.time.delay(10)