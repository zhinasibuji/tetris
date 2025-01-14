from scene_title import SceneTitle

if __name__ == '__main__':
    scene = SceneTitle()
    scene.call()
    while True:
        scene = scene.next_scene
        scene.call()
