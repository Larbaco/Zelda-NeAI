class GameState:
    """Encapsulates all game state that was previously global."""
    
    def __init__(self):
        self.room_transition_pending = False  # Better name than MUDATELA
        self.movement_speed = 2
        self.current_room_x = 0
        self.current_room_y = 0
        # Future AI state can go here
        self.ai_controlled = False