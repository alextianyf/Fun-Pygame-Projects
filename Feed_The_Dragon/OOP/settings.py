class Settings():
    def __init__(self):
        # Set display window dimension
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 400

        # Set display FPS and limits FPS to 60
        self.FPS = 60

        # Set game title
        self.game_title = "Feed the Dragon"

        # Set dragon position
        self.dragon_x_position = 32
        self.dragon_y_position = (self.WINDOW_HEIGHT)//2

game_settings = Settings()