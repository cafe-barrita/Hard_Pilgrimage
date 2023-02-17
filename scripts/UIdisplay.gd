extends ViewportContainer


# Declare member variables here. Examples:
var game_data = null


# Called when the node enters the scene tree for the first time.
func _ready():
	game_data = get_node("/root/GameData")
	
	$Lifebar.rect_position.x = 10
	$Lifebar.rect_position.y = 10
	
	$Stones.rect_position.x = 15
	$Stones.rect_position.y = 35
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	$Stones/Label.text = str(game_data.number_of_stones)
	$Stones/Label.rect_position.x = 30
	
	$Lifebar/Healthbar.max_value = game_data.max_health
	$Lifebar/Healthbar.rect_size.x = game_data.max_health
	$Lifebar/Healthbar.value = game_data.current_health
	$Lifebar/Healthbar.update()
	
