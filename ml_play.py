import os
import pickle
import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    last_ball_x = 0;
    filepath = os.path.join(os.path.dirname(__file__), "model.pickle")
    clf = pickle.load(open(filepath,'rb'))
    comm.ml_ready()

    while True:
        scene_info = comm.get_scene_info()

        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            comm.ml_ready()
            continue

        pred = clf.predict([[scene_info.ball[0], scene_info.ball[1], (scene_info.ball[0] - last_ball_x) > 0, scene_info.ball[1] > 100]])
        if pred == 1:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif pred == 2:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        
        last_ball_x = scene_info.ball[0]