class Settings:
    """ All Game Settings """

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (180, 255, 255)
        self.ship_speed = 1.25
        self.ship_limit = 3
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 4
        self.virus_speed = 0.50
        self.fleet_drop_speed = 5
        self.speed_upscale = 1.20
        self.score_upscale = 1.25
        self.initialize_dynamic_settings()
        self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.25
        self.bullet_speed = 1
        self.virus_speed = 0.50
        self.fleet_direction = 1
        self.virus_points = 50

    def increase_speed(self):
        #self.ship_speed *= self.speed_upscale
        self.bullet_speed *= self.speed_upscale
        self.virus_speed *= self.speed_upscale
        self.virus_points = int(self.virus_points * self.score_upscale)
