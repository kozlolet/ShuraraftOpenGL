from src.physics.aabb import global_aabb, get_blocks_overlapping_aabb, intersects

def entity_collides_with_world(entity, new_pos):  # проверяет столкновение сущности с блоками мира вокруг него
    for local_box in entity.hitboxes:
        entity_box = global_aabb(local_box, new_pos)

        for block_box in get_blocks_overlapping_aabb(entity.play_scene.world, entity_box):
            if intersects(entity_box, block_box):
                return True

    return False

def move_entity(entity, movement_delta):
    new_pos = entity.pos.copy()
    new_pos[0] += movement_delta[0]
    if not entity_collides_with_world(entity, new_pos):
        entity.pos[0] = new_pos[0]

    new_pos = entity.pos.copy()
    new_pos[1] += movement_delta[1]
    if not entity_collides_with_world(entity, new_pos):
        entity.pos[1] = new_pos[1]
    else:
        entity.vertical_speed = 0
        if movement_delta[1] < 0:
            entity.onGround = True
        else:
            entity.onGround = False

    new_pos = entity.pos.copy()
    new_pos[2] += movement_delta[2]
    if not entity_collides_with_world(entity, new_pos):
        entity.pos[2] = new_pos[2]
