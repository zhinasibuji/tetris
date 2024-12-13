from scene_gameover import SceneGameover
from scene_title import SceneTitle
from scene_map import SceneMap

if __name__ == '__main__':
    scene = SceneTitle()
    scene.call()
    while True:
        if scene.next_scene == "scene_title":
            scene = SceneTitle()
            scene.call()
        elif scene.next_scene == "scene_map":
            scene = SceneMap()
            scene.call()
        elif scene.next_scene == "scene_gameover":
            scene = SceneGameover()
            scene.call()
