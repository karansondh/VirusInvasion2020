import sys
from time import sleep
import pygame
from gameset import Settings
from ship import Shooter
from bullet import Bullet
from Virus import Virus
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class CoronaVirus:
    """manage the game assets and behaviour"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(" COVID-19 Invasion on World")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Shooter(self)
        self.bullets = pygame.sprite.Group()
        self.virus = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Start Game!")

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_virus()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_shooters()
            self.virus.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key== pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RSHIFT:
            self._fire_bullet()
        elif event.key == pygame.K_LSHIFT:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_fleet_edges(self):
        for virus in self.virus.sprites():
            if virus.check_edges():
                self._change_fleet_direction()
                break

    def _check_bullet_virus_collisions(self):
        collisons = pygame.sprite.groupcollide(self.bullets, self.virus, True, True)
        if collisons:
            for virus in collisons.values():
                self.stats.score += self.settings.virus_points * len(virus)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.virus:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _change_fleet_direction(self):
        for virus in self.virus.sprites():
            virus.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_virus_bottom(self):
        screen_rect = self.screen.get_rect()
        for virus in self.virus.sprites():
            if virus.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        virus = Virus(self)
        virus_width, virus_height = virus.rect.size
        available_space_x = self.settings.screen_width - (2 * virus_width)
        number_virus_x = available_space_x // (2 * virus_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * virus_height) - ship_height)
        number_rows = available_space_y // (2 * virus_height)
        for row_number in range(number_rows):
            for virus_number in range(number_virus_x):
                self._create_virus(virus_number, row_number)

    def _create_virus(self, virus_number, row_number):
        virus = Virus(self)
        virus_width, virus_height = virus.rect.size
        virus.x = virus_width + 2 * virus_width * virus_number
        virus.rect.x = virus.x
        virus.rect.y = virus.rect.height + 2 * virus.rect.height * row_number
        self.virus.add(virus)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_shooters()
            self.virus.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_virus_collisions()

    def _update_virus(self):
        self._check_fleet_edges()
        self.virus.update()
        if pygame.sprite.spritecollideany(self.ship, self.virus):
            self._ship_hit()
        self._check_virus_bottom()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.virus.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    ai = CoronaVirus()
    ai.run_game()
