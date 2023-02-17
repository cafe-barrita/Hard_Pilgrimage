extends KinematicBody


# Declare member variables here. Examples:
var attack = 2
var movement = 0.1
var facing = 3
var remaining_movement = 1
var rng = null


# Called when the node enters the scene tree for the first time.
func _ready():
	rng = RandomNumberGenerator.new()
	$AnimationPlayer.get_animation("Move").loop = true


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var direction = Vector3.ZERO
	
	if facing == 0:
		direction.x -= movement
	elif facing == 1:
		direction.x += movement
	elif facing == 2:
		direction.z -= movement
	elif facing == 3:
		direction.z += movement
	
	move_and_collide(direction)
	$Sprite3D.frame_coords.y = facing
	$AnimationPlayer.play("Move")
	
	remaining_movement -= 1
	
	if remaining_movement == 0:
		remaining_movement = rng.randi_range(12, 20)
		if facing == 0:
			facing = 2
		elif facing == 1:
			facing = 3
		elif facing == 2:
			facing = 1
		elif facing == 3:
			facing = 0
