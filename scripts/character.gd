extends KinematicBody


# Declare member variables here. Examples:
var movement = 0.5
var game_data = null

# Called when the node enters the scene tree for the first time.
func _ready():
	game_data = get_node("/root/GameData")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var direction = Vector3.ZERO
	var walk = true
	
	if Input.is_key_pressed(KEY_RIGHT):
		direction.x += movement
		game_data.facing = 2
	elif Input.is_key_pressed(KEY_LEFT):
		direction.x -= movement
		game_data.facing = 1
	elif Input.is_key_pressed(KEY_DOWN):
		direction.z += movement
		game_data.facing = 0
	elif Input.is_key_pressed(KEY_UP):
		direction.z -= movement
		game_data.facing = 3
	else:
		walk = false
	
	$Sprite3D.frame_coords.y = game_data.facing
	if walk:
		$AnimationPlayer.get_animation("Walk").loop = true
		$AnimationPlayer.play("Walk")
	else:
		$AnimationPlayer.get_animation("Walk").loop = false
		$Sprite3D.frame_coords.x = 1
	
	var collision = move_and_collide(direction)
	
	if collision:
		if 'Stone' in collision.collider.name:
			game_data.number_of_stones += 5
			collision.collider.queue_free()
		elif 'Enemy' in collision.collider.name:
			game_data.current_health -= collision.collider.attack
			if game_data.current_health <= 0:
				get_tree().quit()
