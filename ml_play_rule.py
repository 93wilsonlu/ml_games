
def get_next_ball_x(ball_x, ball_y, direction_right):
    now_ball_x, now_ball_y = ball_x, ball_y

    while 1:
        print(now_ball_x, now_ball_y)
        if direction_right:
            if 400 - now_ball_y <= 200 - now_ball_x:
                return now_ball_x + (400 - now_ball_y)
            now_ball_y += 200 - now_ball_x
            now_ball_x = 200
        else:
            if 400 - now_ball_y <= now_ball_x:
                return now_ball_x - (400 - now_ball_y)
            now_ball_y += now_ball_x
            now_ball_x = 0

        direction_right = not direction_right

def ml_loop():
    comm.ml_ready()

    last_ball_x = last_ball_y = 0;
    flag = 1
    while True:
        scene_info = comm.get_scene_info()

        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            comm.ml_ready()
            continue

        ball_x, ball_y = scene_info.ball[0], scene_info.ball[1]

        if ball_y > 100 and ball_y - last_ball_y > 0:
            if flag:
                next_ball_x = get_next_ball_x(ball_x, ball_y, (ball_x - last_ball_x) > 0)
                flag = 0
            if (scene_info.platform[0] + 20) - (next_ball_x + 2.5) > 5:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif (scene_info.platform[0] + 20) - (next_ball_x + 2.5) < -5:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        else:
            flag = 1
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        
        last_ball_x, last_ball_y = ball_x, ball_y
